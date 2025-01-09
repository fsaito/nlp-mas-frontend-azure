import subprocess
import logging

# Configuração do ACI
RESOURCE_GROUP = ""
ACI_NAME = ""
ACI_IMAGE = "mcr.microsoft.com/azure-cli:latest"
ACI_LOCATION = ""

# Configurar logging
logging.basicConfig(level=logging.INFO)

def criar_aci_com_identity():
    """
    Cria o Azure Container Instance (ACI) com Managed Identity.
    """
    try:
        subprocess.run(
            [
                "az", "container", "create",
                "--resource-group", RESOURCE_GROUP,
                "--name", ACI_NAME,
                "--image", ACI_IMAGE,
                "--location", ACI_LOCATION,
                "--command-line", "tail -f /dev/null",
                "--restart-policy", "Never",
                "--assign-identity"
            ],
            check=True
        )
        logging.info(f"ACI '{ACI_NAME}' criado com Managed Identity.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao criar o ACI: {e}")
        raise

def executar_comando_no_aci(comando: str) -> str:
    """
    Executa um comando no Azure Container Instance (ACI) usando Managed Identity.

    Parameters:
    - comando (str): Comando a ser executado.

    Returns:
    - str: Resultado da execução do comando.
    """
    try:
        # Verifica se o ACI está em execução
        status = subprocess.check_output(
            [
                "az", "container", "show",
                "--resource-group", RESOURCE_GROUP,
                "--name", ACI_NAME,
                "--query", "instanceView.state",
                "-o", "tsv"
            ],
            text=True
        ).strip()

        if status != "Running":
            logging.warning(f"ACI '{ACI_NAME}' não está em execução. Criando novamente...")
            criar_aci_com_identity()

        # Executa o comando no ACI
        result = subprocess.check_output(
            [
                "az", "container", "exec",
                "--resource-group", RESOURCE_GROUP,
                "--name", ACI_NAME,
                "--exec-command", comando
            ],
            text=True
        )
        logging.info(f"Comando executado com sucesso no ACI '{ACI_NAME}'.")
        return result.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar o comando no ACI: {e}")
        return f"Erro ao executar comando no ACI: {e}"
