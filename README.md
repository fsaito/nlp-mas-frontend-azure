# NLP Frontend for Azure Automation

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/fsaito/nlp-mas-frontend-azure.git
   cd nlp-mas-frontend-azure

2. Atualize o OAI_CONFIG_LIST com suas configurações

3. Atualize o agents/_azure_aci_agent.py com suas configurações
    # Configuração do ACI
    RESOURCE_GROUP = "your RG"
    ACI_NAME = "your ACI name"
    ACI_IMAGE = "mcr.microsoft.com/azure-cli:latest"
    ACI_LOCATION = "your location"

