# azure-synapse-analytics



## Setup sample database in local

1. Install ruby

```bash
sudo apt-get install ruby-full
```

2. Download the [Adventure Works 2014 OLTP Script](https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks-oltp-install-script.zip) and extract files to the sample-database folder

3. Update the extracted csv file

```bash
ruby update_csvs.rb
```

4. Initialize database


# Reference Documents

- https://medium.com/@attila_toth/set-up-sample-database-for-postgresql-4c03b7502a7a


Install PowerShell Core in Linux
https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-linux?view=powershell-7.4&viewFallbackFrom=powershell-6


## Validate template

### Start PowerShell

``` bash
pwsh
```


``` PowerShell

$PackgeDir  = "~/azure-synapse-analytics/azure-marketplace/"
Import-Module .\arm-ttk.psd1
Test-AzTemplate -TemplatePath $PackgeDir

```

### Install Azure CLI
https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt


### Deploy

``` bash
az deployment group create \
  --name ExampleDeployment \
  --resource-group local-deployment \
  --template-file azure-marketplace/mainTemplate.json \
  --parameters azure-marketplace/mainTemplate.parameters.json

```