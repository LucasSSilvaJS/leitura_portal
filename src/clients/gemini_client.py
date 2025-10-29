"""
Gemini client placeholder.

Two common options:
 - Use a simple API key via "requests" if your environment allows.
 - Use google-auth + official client library for service accounts.

Here we provide a simple HTTP wrapper for a generic Gemini-like endpoint.
Replace the URL and auth flow according to your Google setup.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests
from config.config import Config
from typing import Optional


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        # NOTE: you may want to perform OAuth2/service-account flows here.

    def reformulate_to_question(self, text: str, max_chars: int = 96) -> str:
        """
        Sends a request to the generative model asking for a question-format title, <= max_chars.
        The prompt is explicit and enforces the constraint. We also fallback to programmatic truncation.
        """
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY not configured")

        prompt = (
            f"Transforme o título abaixo em uma PERGUNTA de SIM ou NÃO (em português), com no máximo {max_chars} "
            "caracteres incluindo espaços. A pergunta deve soar natural e engajadora, como se fosse feita para "
            "consultar a opinião pública sobre o tema — usando expressões como 'você concorda', 'você conhece', "
            "'acha importante', etc. Retorne apenas a pergunta, sem pontuação extra antes ou depois.\n\n"
            f"Título: {text}\n\nPergunta:"
        )

        # URL correta da API do Google Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 60, "temperature": 0.7},
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        # Parsing da resposta da API do Google Gemini
        text_out = None
        try:
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0 and "text" in parts[0]:
                        text_out = parts[0]["text"]
        except Exception as e:
            logger.warning(f"Erro ao processar resposta do Gemini: {e}")

        if not text_out:
            text_out = data.get("text", "") or ""
        question = text_out.strip()

        # Safety net: trim and ensure max_chars. Try to keep whole words.
        if len(question) > max_chars:
            # try to cut at last space before limit
            short = question[:max_chars]
            if " " in short:
                short = short.rsplit(" ", 1)[0]
            question = short.rstrip(" ?!.;:,") + "?"
        # Guarantee ends with question mark
        if not question.endswith("?"):
            question = question.rstrip(".!;:,") + "?"
        if len(question) > max_chars:
            question = question[:max_chars].rstrip()  # final fallback
            if not question.endswith("?"):
                # replace last char with '?'
                if len(question) >= 1:
                    question = question[:-1] + "?"
        return question
