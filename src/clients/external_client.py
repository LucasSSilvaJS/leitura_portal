import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import requests
from config.config import Config
from typing import Dict, Any

class ExternalClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or Config.EXTERNAL_API_URL

    def send_question(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends data to external API. Returns external API response (json or text).
        """
        # A API externa espera 'texto' como query parameter
        params = {"texto": payload.get("texto", "")}
        
        resp = requests.post(self.base_url, params=params, json=payload, timeout=10)
        try:
            return resp.json()
        except ValueError:
            return {"status_code": resp.status_code, "text": resp.text}
