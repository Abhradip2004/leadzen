# app/ai/factory.py

import os
# from .openai_provider import OpenAIProvider
from .openrouter_provider import OpenRouterProvider

def get_provider():
    provider_name = os.getenv("AI_PROVIDER", "openai").lower()

    if provider_name == "openai":
        # return OpenAIProvider()
        pass
    elif provider_name == "openrouter":
        return OpenRouterProvider()
    else:
        raise ValueError("Unsupported AI provider")