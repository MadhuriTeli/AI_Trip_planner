import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: str | None = os.getenv("TAVILY_API_KEY")
    GPLACES_API_KEY: str | None = os.getenv("GPLACES_API_KEY")


settings = Settings()
