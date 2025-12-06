import requests
from typing import List, Dict

class OllamaClient:
    """
    A client for local Ollama API.
    """
    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://192.168.101.100:11434"):
        """
        Initialize the Ollama client.
        Args:
            model: The model name (must be pulled in Ollama first)
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{self.base_url}/api/chat"
        
        # Verify Ollama is running
        self._check_connection()
        
    def _check_connection(self):
        """Check if Ollama server is accessible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            print(f"Connected to Ollama at {self.base_url}")
        except requests.exceptions.RequestException as e:
            print(f"Cannot connect to Ollama at {self.base_url}")
            print(f"Make sure Ollama is running: ollama serve")
            raise ConnectionError(f"Ollama connection failed: {e}")
        
    
    def generate(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response from the LLM.
        Args:
            system_prompt: System instructions for the LLM
            messages: List of conversation messages (role + content)
        Returns:
            The LLM's response text
        """
        # Build the full message list with system prompt
        full_messages = [
            {"role": "system", "content": system_prompt}
        ] + messages
        
        # Prepare the request payload
        payload = {
            "model": self.model,
            "messages": full_messages,
            "stream": False,  # Get complete response at once
            "options": {
                "temperature": 0.1,  # Low temperature for more deterministic output
            }
        }
        
        try:
            # Make the API request
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60  # LLMs can take time to respond
            )
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            return result["message"]["content"]
            
        except requests.exceptions.Timeout:
            raise TimeoutError("LLM request timed out after 60 seconds")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"LLM request failed: {e}")
        except (KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid response format from LLM: {e}")
        