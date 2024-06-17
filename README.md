# Azure-synapse-analytics

## Overview

This reposistory provide the synapse build package for Azure MarketPlace. There are 2 options

- The first option is deploy a Synapse workspace by ARM template and then execute a container to create azure synapse studio resources such as: Linked Service, NoteBook, pipeline.
- The second option is deploy a Synapse workspace by ARM template and then execute a container to push code from Azure Synapse template repository to the tenant repository, then point the new Synapse studio to the new git repo.


## Prerequisite

### Install Azure CLI
https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt

### Install Azure Resource Manager Template Toolkit (arm-ttk)

This is the tool for ARM template validation.

``` bash
git clone git@github.com:Azure/arm-ttk.git
```


## Option #1

Check out the azure-marketplace/option1 for the template

## Option #2

Check out the azure-marketplace/option2 for the template

## Deploy the template for local for debugging and testing before bring it to Azure Marketplace

``` bash
az deployment group create \
  --name ExampleDeployment40 \
  --resource-group local-deployment \
  --template-file azure-marketplace/mainTemplate.json \
  --parameters azure-marketplace/mainTemplate.parameters.json

```

## Verify the package before push to Azure MarketPlace

### 1. Navigate to Azure Resource Manager Template Toolkit (arm-ttk)

```bash
cd ~/arm-ttk/arm-ttk/
```

### 2. Start PowerShell
``` bash
pwsh
```

### 3.Validate template
``` PowerShell
$PackgeDir  = "~/azure-synapse-analytics/azure-marketplace/"
Import-Module .\arm-ttk.psd1
Test-AzTemplate -TemplatePath $PackgeDir
```
