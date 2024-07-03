# Azure-synapse-analytics

## Overview

This project aims to create a marketplace solution for Azure Synapse. The solution includes the deployment of a data pipeline that reads data from a public SQL Server, performs necessary transformations, and then pushes the transformed data to Azure Blob Storage.

![](images/data-pipeline.png?raw=true)

### Features

- **Automated Data Ingestion**: Seamlessly read data from a public SQL Server.
- **Data Transformation**: Perform required transformations on the data.
- **Data Storage**: Push transformed data to Azure Blob Storage for further use or analysis.


## Solution

There are 2 solution options

### Option  #1

- The first option is deploy a Synapse workspace by ARM template and then execute a container to create azure synapse studio resources such as: Linked Service, NoteBook, pipeline. This container contains a python script to create necessary resources for the Synapse Studio.

- Check out the azure-marketplace/option1 for the template package and container source code in containers/option1

#### Pros

- By using Azure SDK and CLI  inside the container, the developer can setup the pipeline steps with dynamic parameters value which can be entered by user in the MarketPlace GUI.

####  Cons

- It consumes a lot of effort to implement the pipeline by code/cli.
- There is potential for errors during pipeline implementation due to mismatches between the original pipeline provided by the client and the developer's source code. Ensure thorough testing and validation to mitigate these issues.


### Option #2

- The second option is to deploy a Synapse workspace using an ARM template, execute a container to push code from the Azure Synapse template repository to the tenant repository, and then point the new Synapse Studio to the new Git repository

- Check out the azure-marketplace/option2 for the template package and container source code in containers/option2

#### Pros

- The effort to implement the pipeline is minimum as developer just need to pull to source code from a private Azure Container Registries to tenant's git repository.

####  Cons

- Some manually steps that requires tenant's user to setup
  
  - Update the parameters's values in the pipeline such as login credential to the data source.

  - Although the Synapse git configuration is configed automatically during the deployment process by tentan's user has to manually authentication to the git repository.

  - In order to push code the tenant git repository, end-user has to assign the managed identity that created during the setup permission  to read the Azure Key Vault secret which contains the deploy key to push code. We can't make this process automatically as there is an issue describle in the known issues #1


## Known Issues

### Issue 1

Following the option #2, There is an existing Azure Key Vault Secret key which contains the github deploy key to push code to tenant github. We tried to assign the managed identity the permission to access that key vault but the ARM template doesn't work in Azure MarketPlace. We run into the error

```
The client 'f69239b5-b939-4020-bbd3-e5c76dc9a077' with object id 'f69239b5-b939-4020-bbd3-e5c76dc9a077' does not have authorization to perform action 'Microsoft.Resources/deployments/write' over scope '/subscriptions/efdd28a3-55e6-4711-a58b-ab398c259094/resourcegroups/local-deployment/providers/Microsoft.Resources/deployments/pid-db2da1e4-f0fd-4f31-b488-f2266a0084e9-partnercenter' or the scope is invalid. If access was recently granted, please refresh your credentials. (Code: AuthorizationFailed)
```
The demo error template is allocated at: debug/issue1

## Prerequisite

### Install Azure CLI
https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt

### Install Azure Resource Manager Template Toolkit (arm-ttk)

This is the tool for ARM template validation.

``` bash
git clone git@github.com:Azure/arm-ttk.git
```

### Install python 3

## Pubish to Azure Step by Step

An Azure Market deployment is a zip file contains createUiDefinition.json and mainTemplate.json

### 1. Update and test the createUiDefinition.json interface

Update the option1/createUiDefinition.json or option2/createUiDefinition.json in the [Create UI Sandbox](https://portal.azure.com/#view/Microsoft_Azure_CreateUIDef/SandboxBlade)

### 2. Update the ARM template in option1 or option2

### 3. Validate the Azure marketplace package

Using the Azure Resource Manager Template Toolkit (arm-ttk) to validate the package.

#### 1. Navigate to Azure Resource Manager Template Toolkit (arm-ttk)

```bash
cd ~/arm-ttk/arm-ttk/
```

#### 2. Start PowerShell
``` bash
pwsh
```

#### 3.Validate template in option1 or option2
``` PowerShell
$PackgeDir  = "~/azure-synapse-analytics/azure-marketplace/option1"
Import-Module .\arm-ttk.psd1
Test-AzTemplate -TemplatePath $PackgeDir
```

###  4. Update the docker in containers folder if needed.

### 5. Deploy the template for local for debugging and testing before bring it to Azure Marketplace

``` bash
az deployment group create \
  --name ExampleDeployment1 \
  --resource-group marketplace-deployment \
  --template-file azure-marketplace/option1/mainTemplate.json \
  --parameters azure-marketplace/option1/mainTemplate.parameters.json

```


## Some Azure Deployment Errors


### Error #1
```
AzureAppCannotAddTrackingId The package you have uploaded utilizes resources of type Microsoft.Resources/deployments for purposes other than customer usage attribution. Partner Center will be unable to add a customer usage attribution id on your behalf in this case. Please add a new resource of type Microsoft.Resources/deployments and add the tracking ID visible in Partner Center on your plan's Technical Configuration page. To learn more about tracking customer usage attribution please see https://aka.ms/aboutinfluencedrevenuetracking. Error code: PAC-AzureAppCannotAddTrackingId
```

https://learn.microsoft.com/en-us/partner-center/marketplace-offers/azure-partner-customer-usage-attribution#verify-deployments-tracked-with-a-guid


### Error #2 - Enable and request just-in-time access for Azure Managed Applications
https://learn.microsoft.com/en-us/azure/azure-resource-manager/managed-applications/request-just-in-time-access
