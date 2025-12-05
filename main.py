from llm import OllamaClient

def main():
    client = OllamaClient(model="llama3.2:3b")
    
    system_prompt = "You are a helpful assistant."
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "user", "content": "What is the latest version of Python?"}
    ]
    
    response = client.generate(system_prompt, messages)
    print("Response from Ollama:")
    print(response)

if __name__ == "__main__":
    main()
