from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    redis_url: str = "redis://redis:6379/0"
    model: str = "gpt-4.1-mini"

    class Config:
        env_file = ".env"


settings = Settings()
