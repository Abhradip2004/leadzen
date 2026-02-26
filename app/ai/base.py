from abc import ABC, abstractmethod
from typing import Dict

class AIProvider(ABC):
    @abstractmethod
    def classify_lead(self, message: str) -> Dict:
        """
        Must return:
        {
            "summary": str,
            "intent": "hot" | "medium" | "low",
            "followup": str
        }
        """
        pass