import requests
from typing import List, Dict

class OllamaClient:
    """
    A client for local Ollama API.
    """
    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://192.168.101.100:11434"):
        self.model = model
        self.base_url = base_url
        self.api_url = f"{self.base_url}/api/chat"
        self._check_connection()
        
    def _check_connection(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            print("Connected to Ollama API successfully.")
        except Exception as e:
            raise ConnectionError(f"Cannot connect to Ollama: {e}")
        
    def generate(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "stream": False,
            "options": {"temperature": 0.1},
        }
        response = requests.post(self.api_url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["message"]["content"]
        