az deployment group create \
  --name ExampleDeployment \
  --resource-group ExampleGroup \
  --template-file azure-marketplace/mainTemplate.json \
  --parameters @azure-marketplace/mainTemplate.parameters.json