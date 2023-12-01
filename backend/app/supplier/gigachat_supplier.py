from dataclasses import dataclass

from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage
from shared.settings import app_settings


@dataclass
class GigachatSupplier:
    def __post_init__(self) -> None:
        self.gigachat = GigaChat(
            credentials=app_settings.gigachat_credentials,
            verify_ssl_certs=False,
        )

    def single_message(self, prompt: str) -> str:
        messages = [HumanMessage(content=prompt)]
        res = self.gigachat(messages)

        return res.content
