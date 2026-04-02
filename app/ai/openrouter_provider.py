import os
import requests
import time

from .base import AIProvider
from .utils import extract_json, validate_response
from app.db.ai_logs import insert_ai_log


class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "qwen/qwen2.5-7b-instruct"
        )
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def classify_lead(self, message: str, lead_id: str = None):
        prompt = self._build_prompt(message)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "temperature": 0.4,
            "messages": [
                {
                    "role": "system",
                    "content": self._system_prompt(),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        }

        start = time.time()
        response = requests.post(self.base_url, json=payload, headers=headers)
        latency_ms = int((time.time() - start) * 1000)

        response.raise_for_status()

        raw_text = response.json()["choices"][0]["message"]["content"].strip()

        data = extract_json(raw_text)
        validated = validate_response(data)

        if lead_id:
            insert_ai_log(
                lead_id=lead_id,
                provider="openrouter",
                model=self.model,
                prompt=prompt,
                raw_response=raw_text,
                latency_ms=latency_ms,
            )

        return validated

    def _system_prompt(self) -> str:
        return """
You are a professional, polite, and helpful sales assistant.

Your responsibilities:
- Understand the user's requirement clearly
- Classify their intent accurately
- Respond like a human, not a machine

Guidelines for response:
- Always be polite and professional
- Acknowledge the user’s request
- Provide helpful next steps
- Ask relevant follow-up questions when needed
- Keep the tone natural and conversational
- Avoid robotic or instruction-style language

Do NOT:
- Give internal instructions (e.g., "schedule immediately", "prioritize")
- Use bullet-point commands
- Sound like a system or backend process

Your response must feel like a real human replying to an email.
"""

    def _build_prompt(self, message: str):
        return f"""
Analyze the following customer inquiry.

Return ONLY valid JSON in this format:
{{
  "summary": "short summary of requirement",
  "intent": "hot|medium|low",
  "followup": "natural human reply message"
}}

Important:
- The "followup" must be a well-written email response
- It should sound like a human sales assistant
- It should NOT contain instructions or internal notes

Customer Message:
\"\"\"{message}\"\"\"
"""