#!/bin/bash

# Variáveis
RESOURCE_GROUP="mas"
ACI_NAME="aci-mas"
LOCATION="eastus"

# Criação do Resource Group
echo "Criando Resource Group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Criação do ACI com Managed Identity
echo "Criando ACI com Managed Identity..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $ACI_NAME \
  --image mcr.microsoft.com/azure-cli:latest \
  --location $LOCATION \
  --command-line "tail -f /dev/null" \
  --restart-policy Never \
  --assign-identity

# Atribuição de Permissões
echo "Atribuindo permissões à Identidade Gerenciada..."
IDENTITY_PRINCIPAL=$(az container show --resource-group $RESOURCE_GROUP --name $ACI_NAME --query identity.principalId -o tsv)
az role assignment create --assignee $IDENTITY_PRINCIPAL --role "Storage Account Contributor" --scope "/subscriptions/<subscription-id>"

echo "Configuração concluída com sucesso!"
