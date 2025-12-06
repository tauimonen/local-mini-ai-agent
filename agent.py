"""
Agent Core Module

Implements the ReAct (Reasoning + Acting) pattern for an AI agent.
The agent can reason about tasks and use tools to accomplish them.
"""

import json
import re
from typing import Dict, List, Optional
from llm import OllamaClient
from tools import get_all_tools


# System prompt that instructs the LLM how to use tools
SYSTEM_PROMPT = """You are a helpful AI agent that can use tools to accomplish tasks.

When you need to use a tool, respond with JSON in this exact format:
{{ "thought": "your reasoning about what to do",
   "action": "tool_name",
   "action_input": "input for the tool" }}

When you have the final answer, respond with JSON in this format:
{{ "thought": "summary of what you found",
   "final_answer": "your complete answer to the user" }}

Available tools:
{tools_description}

Important rules:
- Always respond with valid JSON only
- Use tools when you need to perform actions or get information
- Think step by step
- When you have all the information needed, provide the final_answer
"""


class Agent:
    """
    A simple ReAct agent that can reason and act using tools.
    
    The agent follows this loop:
    1. Receive a query
    2. Think about what to do (using LLM)
    3. Either use a tool or provide final answer
    4. Repeat until done or max iterations reached
    """
    
    def __init__(self, model: str = "llama3.2:3b", max_iterations: int = 2):
        """
        Initialize the agent.
        Args:
            model: The Ollama model to use
            max_iterations: Maximum number of reasoning steps to prevent infinite loops
        """
        self.llm = OllamaClient(model=model)
        self.tools = get_all_tools()
        self.max_iterations = max_iterations
        
        # Build tools description for the system prompt
        tools_desc = self._build_tools_description()
        self.system_prompt = SYSTEM_PROMPT.format(tools_description=tools_desc)
    
    def _build_tools_description(self) -> str:
        """Build a formatted description of all available tools."""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool['description']}")
        return "\n".join(descriptions)
    
    def _parse_llm_response(self, response: str) -> Optional[Dict]:
        """
        Parse the LLM's JSON response.
        Args:
            response: Raw response from LLM
        Returns:
            Parsed JSON dict or None if parsing fails
        """
        # Try to extract JSON from the response (LLMs sometimes add extra text)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                return None
        return None
    
    def _execute_tool(self, action: str, action_input: str) -> str:
        """
        Execute a tool with the given input.
        Args:
            action: Name of the tool to execute
            action_input: Input parameter for the tool
        Returns:
            Result from the tool execution
        """
        if action not in self.tools:
            return f"Error: Tool '{action}' not found. Available tools: {list(self.tools.keys())}"
        
        try:
            tool_func = self.tools[action]['func']
            result = tool_func(action_input)
            return str(result)
        except Exception as e:
            return f"Error executing tool: {str(e)}"
    
    def run(self, query: str) -> str:
        """
        Run the agent on a query.
        This is the main agent loop that implements the ReAct pattern:
        - Think (reason about what to do)
        - Act (use a tool if needed)
        - Observe (see the result)
        - Repeat until done
        Args:
            query: The user's question or task
        Returns:
            The final answer from the agent
        """
        conversation_history = []
        
        # Add the user's query
        conversation_history.append({
            "role": "user",
            "content": query
        })
        
        print(f"\nStarting agent loop...")
        
        # Agent reasoning loop
        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1}/{self.max_iterations} ---")
            
            # Get LLM's response
            response = self.llm.generate(
                system_prompt=self.system_prompt,
                messages=conversation_history
            )
            
            print(f"LLM Response: {response[:200]}...")
            
            # Parse the response
            parsed = self._parse_llm_response(response)
            
            if not parsed:
                # If we can't parse JSON, ask LLM to retry
                error_msg = "Please respond with valid JSON only."
                conversation_history.append({"role": "assistant", "content": response})
                conversation_history.append({"role": "user", "content": error_msg})
                continue
            
            # Check if we have a final answer
            if "final_answer" in parsed:
                print(f"\nAgent reached final answer")
                return parsed["final_answer"]
            
            # Check if we have an action to execute
            if "action" in parsed and "action_input" in parsed:
                thought = parsed.get("thought", "")
                action = parsed["action"]
                action_input = parsed["action_input"]
                
                print(f"Thought: {thought}")
                print(f"Action: {action}({action_input})")
                
                # Execute the tool
                observation = self._execute_tool(action, action_input)
                print(f"Observation: {observation}")
                
                # Add to conversation history
                conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                conversation_history.append({
                    "role": "user",
                    "content": f"Observation: {observation}"
                })
            else:
                # Malformed response
                error_msg = "Please provide either 'final_answer' or both 'action' and 'action_input'."
                conversation_history.append({"role": "assistant", "content": response})
                conversation_history.append({"role": "user", "content": error_msg})
        
        # Max iterations reached
        return f"Agent stopped after {self.max_iterations} iterations without finding an answer."