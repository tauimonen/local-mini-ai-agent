"""
Simple Local AI Agent - Main Entry Point

This is a learning project demonstrating a basic ReAct (Reasoning + Acting) agent
that uses a local LLM (via Ollama) and can use tools to accomplish tasks.

Requirements:
- Ollama installed and running (https://ollama.ai)
- Model downloaded: ollama pull llama3.2:3b
"""

from agent import Agent


def main():
    """Run the agent with example queries."""
    
    print("=== Simple Local AI Agent ===")
    print("Using Ollama with llama3.2:3b model\n")
    
    # Initialize the agent
    agent = Agent(model="llama3.2:3b", max_iterations=5)
    
    # Example queries to demonstrate different tools
    # queries = [
    #     "What is 25 multiplied by 47?",
    #     "Read the file example.txt and tell me what it contains",
    #     "Calculate the result of (15 + 23) * 2, then save it to result.txt"
    # ]
    
    query = "Read the file example.txt and tell me what it contains"
    
    # Run query
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print("Thinking... please wait."))
        
    try:
        result = agent.run(query)
        print(f"\n✓ Final Answer: {result}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        
    print("\n\nAgent session completed!")


if __name__ == "__main__":
    main()
