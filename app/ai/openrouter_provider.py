

import os
import requests
from .base import AIProvider
from .utils import extract_json, validate_response

import time
from app.db.ai_logs import insert_ai_log

class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "qwen/qwen3-vl-30b-a3b-thinking"
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
            "temperature": 0,
            "messages": [
                {"role": "system", "content": "You are a lead qualification AI."},
                {"role": "user", "content": prompt},
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

    def _build_prompt(self, message: str):
        return f"""
                Analyze the following incoming lead message from any industry.

                Classify buying intent as:
                - hot (ready to act soon)
                - medium (interested but not urgent)
                - low (just exploring)

                Return ONLY valid JSON:
                {{
                "summary": "...",
                "intent": "hot|medium|low",
                "followup": "..."
                }}

                Message:
                \"\"\"{message}\"\"\"
                """