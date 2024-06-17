# Docker Image for deploy Synapse Studio Resource

## Overview

This docker image will execute during the Azure MarketPlace deployment to setup necessary resources such as: Linked Services, NoteBook, Pipeline, etc.

## Build and push Docker Image

``` bash
docker build . -t tranhoang/azure-marketplace:latest
docker push tranhoang/azure-marketplace:latest
```

``` bash
docker run -it collectiv-azure-marketplace:latest
```


## Common commands

### View log streams in Azure Container Apps

``` bash
az container attach --resource-group local-deployment --name localworkspace-aci
```

### Start Azure container group from local to debug

``` bash
RESOURCE_ID=/subscriptions/efdd28a3-55e6-4711-a58b-ab398c259094/resourcegroups/local-deployment/providers/Microsoft.ManagedIdentity/userAssignedIdentities/containerIdentity

az container create \
    --resource-group local-deployment \
    --name test-image \
    --image tranhoang/azure-marketplace:latest \
    --restart-policy Never \
    --environment-variables AZURE_SUBSCRIPTION_ID=efdd28a3-55e6-4711-a58b-ab398c259094 DATA_SOURCE=localworkspace-ondemand.sql.azuresynapse.net INIT_DATABASE_NAME=localworkspace-gold-db SYNAPSE_WORKSPACE_ENDPOINT=https://localworkspace.dev.azuresynapse.net SYNAPSE_DATASOURCE=localworkspace-ondemand.sql.azuresynapse.net SYNAPSE_DATABASE_NAME=localworkspace-gold-db SOURCE_DATA_SOURCE=sqlservercentralpublic.database.windows.net SOURCE_DATABASE_NAME=AdventureWorks SOURCE_DATABASE_USER_NAME=sqlfamily SOURCE_DATABASE_PASSWORD=TBD SYNAPSE_WORKSPACE_NAME=localworkspace CONTAINER_IDENITY_PRINCIPAL_ID=4ef37297-5c83-40ff-8df3-2a8807b3fde5 \
    --assign-identity $RESOURCE_ID \
    --command-line "python src/script.py"
```

## References

https://learn.microsoft.com/en-us/cli/azure/run-azure-cli-docker
