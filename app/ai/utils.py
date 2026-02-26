import json
import re

VALID_INTENTS = {"hot", "medium", "low"}

def extract_json(text: str):
    """
    Attempts to extract JSON object from raw model response.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try extracting JSON block using regex
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise

def validate_response(data: dict):
    if not isinstance(data, dict):
        raise ValueError("AI response is not a dictionary")

    if "summary" not in data:
        raise ValueError("Missing summary")

    if "intent" not in data:
        raise ValueError("Missing intent")

    if data["intent"] not in VALID_INTENTS:
        raise ValueError("Invalid intent value")

    if "followup" not in data:
        raise ValueError("Missing followup")

    return data