from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeminiConfig(BaseSettings):
    api_key: str = Field(default=None, alias="GEMINI_API_KEY")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class OpenRouterConfig(BaseSettings):
    api_key: str = Field(default=None, alias="OPENROUTER_API_KEY")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class SecretKeyConfig(BaseSettings):
    key: str = Field(default=None, alias="SECRET_KEY")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini: GeminiConfig = Field(default_factory=GeminiConfig)
    openrouter: OpenRouterConfig = Field(default_factory=OpenRouterConfig)
    secrets: SecretKeyConfig = Field(default_factory=SecretKeyConfig)


settings = Config()
