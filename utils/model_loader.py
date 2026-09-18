import logging
from typing import Any, Literal

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field, SecretStr

from config.settings import settings
from utils.config_loader import load_config

logger = logging.getLogger(__name__)


class ConfigLoader:
    def __init__(self) -> None:
        logger.info("Loading application configuration")
        self.config = load_config()

    def __getitem__(self, key: str) -> Any:
        return self.config[key]


class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: ConfigLoader | None = Field(default=None, exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def model_post_init(self, __context: Any, /) -> None:
        self.config = ConfigLoader()

    def load_llm(self) -> Any:
        if self.config is None:
            raise RuntimeError("Model configuration is not initialized")

        logger.info("Loading LLM from provider: %s", self.model_provider)

        if self.model_provider == "groq":
            model_name = self.config["llm"]["groq"]["model_name"]

            if not settings.GROQ_API_KEY:
                raise RuntimeError("GROQ_API_KEY is not configured")

            return ChatGroq(
                model=model_name,
                api_key=SecretStr(settings.GROQ_API_KEY),
            )

        if self.model_provider == "openai":
            model_name = self.config["llm"]["openai"]["model_name"]

            if not settings.OPENAI_API_KEY:
                raise RuntimeError("OPENAI_API_KEY is not configured")

            return ChatOpenAI(
                model=model_name,
                api_key=SecretStr(settings.OPENAI_API_KEY),
            )
        raise ValueError(f"Unsupported model provider: {self.model_provider}")
