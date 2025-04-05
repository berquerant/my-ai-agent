from dataclasses import dataclass

from agents import ModelProvider, Model, OpenAIChatCompletionsModel, OpenAIProvider
from openai import AsyncOpenAI

from .log import log


@dataclass
class Setting:
    model_name: str
    api_key: str
    base_url: str | None = None

    @property
    def client(self) -> AsyncOpenAI:
        return AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    @property
    def provider(self) -> ModelProvider:
        if self.base_url is None:
            log().debug("provider: use default provider")
            return OpenAIProvider()
        log().debug("provider: use custom model provider, base_url=%s", self.base_url)
        return CustomModelProvider(self)


class CustomModelProvider(OpenAIProvider):
    setting: Setting

    def __init__(self, setting: Setting):
        self.setting = setting

    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(
            model=self.setting.model_name,  # override model_name
            openai_client=self.setting.client,
        )
