"""
LLM Module - Ollama Client

Handles communication with the local Ollama server.
Ollama must be installed and running for this to work.
"""

import requests
from typing import List, Dict
import os
import json
import time

class OllamaClient:
    """
    A client for local Ollama API. Uses Docker service name 'ollama' by default.
    """
    def __init__(self, model: str = "llama3.2:3b", base_url: str = None):
        """
        Initialize the Ollama client.
        Args:
            model: The model name (must be pulled in Ollama first)
            base_url: Ollama server URL (defaults to OLLAMA_HOST env var or Docker service name)
        """
        self.model = model

        # Use environment variable OLLAMA_HOST if provided, else default to Docker service name
        self.base_url = (base_url or os.getenv("OLLAMA_HOST", "http://ollama:11434")).rstrip("/")
        self.api_url = f"{self.base_url}/api/chat"

        # Try to verify connection but do not crash container
        self._check_connection()

    def _check_connection(self):
        """Check if Ollama server is accessible, retry until success."""
        for attempt in range(10):  # Try 10 times
            try:
                response = requests.get(f"{self.base_url}/api/tags", timeout=5)
                response.raise_for_status()
                print(f"Connected to Ollama at {self.base_url}")
                return
            except requests.exceptions.RequestException as e:
                print(f"Cannot connect to Ollama at {self.base_url}, attempt {attempt+1}/10")
                time.sleep(2)
        print(f"Warning: Could not connect to Ollama at {self.base_url}. The container will stay alive for debugging.")

    def generate(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response from the LLM.
        Args:
            system_prompt: System instructions for the LLM
            messages: List of conversation messages (role + content)
        Returns:
            The LLM's response text
        """
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        payload = {
            "model": self.model,
            "messages": full_messages,
            "stream": False,
            "options": {
                "temperature": 0.1,
            }
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "Error: LLM request failed"
