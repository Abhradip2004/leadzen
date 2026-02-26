from .factory import get_provider

_provider = get_provider()

def classify_lead(message: str, lead_id: str = None):
    return _provider.classify_lead(message, lead_id)