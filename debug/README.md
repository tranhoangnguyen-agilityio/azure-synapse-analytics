## Run a specific ARM resource template to make sure it works

```bash
az deployment group create \
  --name DebugDeployment5 \
  --resource-group local-deployment \
  --template-file template.json
```