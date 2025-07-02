from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


# pydantic implementation of secrets manage
class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file=r".env")


config = Settings()
