"""
LLM Module - Ollama Client
Uses the Ollama HTTP API to interact with local LLM models.
"""

import requests
from typing import List, Dict
import os
import json

class OllamaClient:
    def __init__(self, model: str = "llama3.2:3b", base_url: str = None):
        self.model = model
        if base_url is None:
            base_url = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/chat"

        # Check if Ollama server is accessible
        self._check_connection()

    def _check_connection(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            print(f"Connected to Ollama at {self.base_url}")
        except requests.exceptions.RequestException as e:
            print(f"Cannot connect to Ollama at {self.base_url}")
            raise ConnectionError(f"Ollama connection failed: {e}")

    def generate(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response from the LLM using the HTTP API.
        """
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        payload = {
            "model": self.model,
            "messages": full_messages,
            "stream": False,
            "options": {"temperature": 0.1},
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            # Ollama 0.13.1 returns content under ["message"]["content"]
            return result["message"]["content"]
        except requests.exceptions.Timeout:
            raise TimeoutError("LLM request timed out after 60 seconds")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"LLM request failed: {e}")
        except (KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid response format from LLM: {e}")
