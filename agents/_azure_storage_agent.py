from autogen import ConversableAgent, register_function, config_list_from_json
from ._azure_aci_agent import executar_comando_no_aci
import logging
import json

# Carregar configurações do LLM a partir do JSON
config_list = config_list_from_json("OAI_CONFIG_LIST")
llm_config = {"config_list": config_list}

# Classe AzureStorageAgent
class AzureStorageAgent:
    def __init__(self):
        """
        Inicializa o agente Azure Storage.
        """
        self.assistant = ConversableAgent(
            name="AzureStorageAssistant",
            llm_config=llm_config,
            system_message=(
                "Você é um assistente especializado em Azure Storage Accounts. "
                "Transforme qualquer solicitação do usuário em comandos Azure CLI válidos e execute-os remotamente no servidor configurado. "
                "Aproveite as credenciais já configuradas no servidor remoto para garantir a execução bem-sucedida. "
                "Se informações estiverem faltando, pergunte ao usuário com sugestões claras. "
                "Resolva dependências automaticamente, se necessário. "
                "Se a solicitação não estiver no escopo, explique ao usuário e finalize com TERMINATE."
            ),
        )
        self.user_proxy = ConversableAgent(
            name="UserProxy",
            llm_config=False,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            human_input_mode="NEVER",  # Permitir input do usuário caso mais informações sejam necessárias.
        )

        # Registrar a função para executar comandos
        register_function(
            executar_comando_no_aci,
            caller=self.assistant,
            executor=self.user_proxy,
            name="executar_comando_remoto",
            description="Executa comandos Azure CLI em um Azure Container Instance.",
        )

    logging.basicConfig(level=logging.DEBUG)




    def handle_prompt(self, prompt: str) -> str:
        """
        Processa a solicitação do usuário e retorna todas as respostas do agente.

        Parameters:
        - prompt (str): Mensagem do usuário.

        Returns:
        - str: Todas as respostas geradas pelo agente.
        """
        try:
            response = self.assistant.initiate_chat(
                recipient=self.user_proxy,
                message={"content": prompt, "role": "user"}
            )

            chat_history = getattr(response, "chat_history", [])
            logging.debug(f"Histórico de mensagens: {chat_history}")

            assistant_responses = [
                message.get("content", "")
                for message in chat_history
                if message.get("role") == "assistant" and message.get("content") is not None
            ]

            return "\n\n".join(assistant_responses)

        except Exception as e:
            logging.error(f"Erro ao processar o prompt: {e}")
            return f"Erro ao processar o prompt: {e}"  # Certifique-se de que a f-string está fechada
