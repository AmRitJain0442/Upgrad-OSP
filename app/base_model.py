import logging

from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider

from app.core.config import settings


logger = logging.getLogger(__name__)


def get_google_model(model_name: str, thinking_enabled: bool = True):
    provider = GoogleProvider(
        api_key=settings.gemini.api_key,
    )
    return GoogleModel(
        model_name=model_name,
        provider=provider,
        settings=GoogleModelSettings(google_thinking_config={"thinking_budget": 0})
        if thinking_enabled
        else None,
    )


def get_openrouter_model(model_name: str):
    provider = OpenRouterProvider(api_key=settings.secrets.key)
    return OpenAIChatModel(
        model_name=model_name,
        provider=provider,
    )


def get_model(model_name: str, provider: str = "google"):
    """
    Get a model instance based on provider and model name

    Args:
        model_name: Name of the model (e.g., "gemini-2.0-flash-exp")
        provider: Provider to use ("google" or "openrouter")

    Returns:
        Model instance configured with the appropriate provider
    """
    if provider == "google":
        return get_google_model(model_name)
    elif provider == "openrouter":
        return get_openrouter_model(model_name)
    else:
        raise ValueError(
            f"Invalid provider: {provider}. Must be 'google' or 'openrouter'"
        )
