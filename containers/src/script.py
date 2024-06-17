import os
import subprocess
import shlex
import uuid
import time

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.synapse import SynapseManagementClient
from azure.synapse.artifacts import ArtifactsClient
from azure.synapse.accesscontrol import AccessControlClient
from azure.synapse.artifacts.models import (
    AzureSqlDatabaseLinkedService, SqlServerLinkedService, IntegrationRuntimeReference, AzureBlobFSDataset,
    BinaryDataset,
    AzureBlobStorageLocation,
    LinkedServiceReference,
    ParquetDataset,
    ParameterSpecification,
    SqlServerTableDataset,
    NotebookResource,
)
from azure.core.exceptions import ResourceExistsError


def demo(prefix: str):
    """
    Create a linked service to connect to built-in serverless SQL
    """

    credential = DefaultAzureCredential()
    
    # Retrieve subscription ID from environment variable.
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

    # Obtain the management object for resources.
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Retrieve the list of resource groups
    group_list = resource_client.resource_groups.list()

    for group in list(group_list):
        print(f"{group.name}")



def create_serverless_database_link_service(synapse_workspace_endpoint: str, data_source: str, database_name: str):
    """
    Create a linked service to connect to built-in serverless SQL
    https://github.com/Azure/azure-sdk-for-python/tree/610da5d1b5ed19106fa2225866371d7fb30908dd/sdk/synapse/azure-synapse-artifacts
    """

    credential = DefaultAzureCredential()
    
    # Obtain the management object for resources.
    resource_client = ArtifactsClient(credential, synapse_workspace_endpoint)
    
    connection_string = 'Integrated Security=False;Encrypt=True;Connection Timeout=30;Data Source={data_source};Initial Catalog={database_name}'.format(data_source=data_source, database_name=database_name)
    linked_service = AzureSqlDatabaseLinkedService(connection_string=connection_string, connect_via=IntegrationRuntimeReference, description="Test update")
    linked_service_name =  "serverlessSQLdb"

    resource_client.linked_service.begin_create_or_update_linked_service(linked_service_name=linked_service_name, properties=linked_service)
    print('Created link service for serverless database')


def create_sql_server_database_link_service(synapse_workspace_endpoint: str, data_source: str, database_name: str, user_name: str, password: str):
    credential = DefaultAzureCredential()
    
    # Obtain the management object for resources.
    
    resource_client = ArtifactsClient(credential, synapse_workspace_endpoint)

    connection_string = 'integrated security=False;data source={data_source};initial catalog={database_name};user id={user_name};password={password}'.format(data_source=data_source, database_name=database_name, user_name=user_name, password=password)
    linked_service = SqlServerLinkedService(connection_string=connection_string, connect_via=IntegrationRuntimeReference)
    linked_service_name =  "FreeAzureAdventureWorksSqlServer1"
    resource_client.linked_service.begin_create_or_update_linked_service(linked_service_name=linked_service_name, properties=linked_service)
    print('Created link service for Free SQL Server database')


def create_gold_table_dataset(workspace_name: str, synapse_workspace_endpoint: str):
    credential = DefaultAzureCredential()

    resource_client = ArtifactsClient(credential, synapse_workspace_endpoint)


    dataset_name = "goldtables"

    # Init link service ref
    linked_service_name = f"{workspace_name}-WorkspaceDefaultStorage"
    linked_service_ref = LinkedServiceReference(reference_name=linked_service_name, type="LinkedServiceReference")

    # Init BinaryDataSet
    location = AzureBlobStorageLocation(container="gold", folder_path="SalesLT")
    dataset = BinaryDataset(linked_service_name=linked_service_ref, location=location)

    resource_client.dataset.begin_create_or_update_dataset(dataset_name=dataset_name, properties=dataset)
    print('Created goldtables dataset')


def create_parquet_dataset(workspace_name: str, synapse_workspace_endpoint: str):
    credential = DefaultAzureCredential()
    resource_client = ArtifactsClient(credential, synapse_workspace_endpoint)

    dataset_name = "parquetTables"

    # Init link service ref
    linked_service_name = f"{workspace_name}-WorkspaceDefaultStorage"
    linked_service_ref = LinkedServiceReference(reference_name=linked_service_name, type="LinkedServiceReference")

    # Init BinaryDataSet
    location = AzureBlobStorageLocation(container="bronze", folder_path="@concat(dataset().schemaname, '/', dataset().tablename)", file_name="@concat(dataset().tablename, '.parquet')")
    ParameterSpecification(type=str)
    parameters = {
        "schemaname": ParameterSpecification(type="String"),
        "tablename": ParameterSpecification(type="String")
    }
    dataset = ParquetDataset(linked_service_name=linked_service_ref, location=location, parameters=parameters)

    resource_client.dataset.begin_create_or_update_dataset(dataset_name=dataset_name, properties=dataset)
    print('Created parquet dataset')


def create_sql_server_dataset(synapse_workspace_endpoint: str):
    credential = DefaultAzureCredential()
    resource_client = ArtifactsClient(credential, synapse_workspace_endpoint)
    dataset_name = "SqlDBTables"

    linked_service_name = "FreeAzureAdventureWorksSqlServer1"
    linked_service_ref = LinkedServiceReference(reference_name=linked_service_name, type="LinkedServiceReference")

    dataset = SqlServerTableDataset(linked_service_name=linked_service_ref)
    resource_client.dataset.begin_create_or_update_dataset(dataset_name=dataset_name, properties=dataset)
    print('Created Sql server dataset')


def create_pipeline_create_view(synapse_workspace_endpoint: str):
    credential = DefaultAzureCredential()
    resource_client = ArtifactsClient(credential, synapse_workspace_endpoint)

    with open("./src/pipelines/create_view_pipeline.json") as pipeline_file:
        operation = resource_client.pipeline.begin_create_or_update_pipeline("Create view", pipeline_file)

    print('Created create view pipeline')


def create_note_books(workspace_name: str, container_identity_principal_id: str):
    """
    Run az cli to import notebook
    """
    login_command = """az login --identity --username {container_identity_principal_id}""".format(container_identity_principal_id=container_identity_principal_id)
    result = subprocess.run(shlex.split(login_command))

    command = """az synapse notebook import --file "@src/notebooks/bronze-to-silver.ipynb" \
        --name bronze-to-silver \
        --workspace-name {workspace_name} \
        --executor-count 2  \
        --executor-size Small \
        --spark-pool-name collectivspark""".format(workspace_name=workspace_name)
    result = subprocess.run(shlex.split(command))

    if result.returncode != 0:
        raise Exception("Error while importing notebook")
    else:
        print('Imported notebook.')


def create_pipeline_copy_all_tables(synapse_workspace_endpoint: str):
    credential = DefaultAzureCredential()
    resource_client = ArtifactsClient(credential, synapse_workspace_endpoint)

    with open("./src/pipelines/copy_all_tables_pipeline.json") as pipeline_file:
        operation = resource_client.pipeline.begin_create_or_update_pipeline("copy_all_tables", pipeline_file)

    print('Created create view pipeline')


def create_synapse_database(synapse_workspace_name: str):
    pass


def assign_synapse_studio_role(workspace_name: str, synapse_workspace_endpoint: str, container_identity_principal_id: str):

    credential = DefaultAzureCredential()

    acc = AccessControlClient(
        credential=credential,
        endpoint=synapse_workspace_endpoint
    )

    SYNAPSE_STUDIO_ADMINISTRATOR_ROLE_ID = "6e4bf58a-b8e1-4cc3-bbf9-d73143322b78"

    try:
        acc.role_assignments.create_role_assignment(
            role_assignment_id=str(uuid.uuid4()),
            principal_id=container_identity_principal_id,
            role_id=SYNAPSE_STUDIO_ADMINISTRATOR_ROLE_ID,
            scope="workspaces/%s" % workspace_name
        )
        print(f'Created role assignment: principal_id = {container_identity_principal_id} and role_id = {SYNAPSE_STUDIO_ADMINISTRATOR_ROLE_ID}')
    except ResourceExistsError:
        print(f'The role assignment is already created: principal_id = {container_identity_principal_id} and role_id = {SYNAPSE_STUDIO_ADMINISTRATOR_ROLE_ID}')
    except Exception as error:
        raise error

def sleep(message: str):
    for i in range(6):
        print(message)
        time.sleep(10) # Makes Python wait for 10 seconds
    print('Finished waiting.')


synapse_workspace_name = os.environ["SYNAPSE_WORKSPACE_NAME"] 
synapse_workspace_endpoint = os.environ["SYNAPSE_WORKSPACE_ENDPOINT"] 
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
data_source = os.environ["SYNAPSE_DATASOURCE"]
database_name = os.environ["SYNAPSE_DATABASE_NAME"]

source_data_source = os.environ["SOURCE_DATA_SOURCE"]
source_database_name = os.environ["SOURCE_DATABASE_NAME"]
source_db_user_name = os.environ["SOURCE_DATABASE_USER_NAME"]
source_db_password = os.environ["SOURCE_DATABASE_PASSWORD"]

container_identity_principal_id = os.environ["CONTAINER_IDENITY_PRINCIPAL_ID"]

assign_synapse_studio_role(workspace_name=synapse_workspace_name, synapse_workspace_endpoint=synapse_workspace_endpoint, container_identity_principal_id=container_identity_principal_id)
sleep('Waiting for the new role assignment got affected.')
create_serverless_database_link_service(synapse_workspace_endpoint, data_source, database_name)
create_sql_server_database_link_service(synapse_workspace_endpoint, source_data_source, source_database_name, source_db_user_name, source_db_password)
create_gold_table_dataset(workspace_name=synapse_workspace_name, synapse_workspace_endpoint=synapse_workspace_endpoint)
create_parquet_dataset(workspace_name=synapse_workspace_name, synapse_workspace_endpoint=synapse_workspace_endpoint)
create_sql_server_dataset(synapse_workspace_endpoint=synapse_workspace_endpoint)
create_note_books(workspace_name=synapse_workspace_name, container_identity_principal_id=container_identity_principal_id)
create_pipeline_create_view(synapse_workspace_endpoint=synapse_workspace_endpoint)
create_pipeline_copy_all_tables(synapse_workspace_endpoint=synapse_workspace_endpoint)
