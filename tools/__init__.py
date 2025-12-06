"""
Tools Package

This package contains all available tools that the agent can use.
Each tool is a simple function that takes a string input and returns a string output.
"""

from .file_tool import read_file, write_file
from .calculator import calculate


def get_all_tools():
    """
    Get a dictionary of all available tools.
    Returns:
        Dict mapping tool names to their functions and descriptions
    """
    return {
        "read_file": {
            "func": read_file,
            "description": "Read contents of a text file. Input: filepath"
        },
        "write_file": {
            "func": write_file,
            "description": "Write text to a file. Input: 'filepath|content' separated by pipe"
        },
        "calculate": {
            "func": calculate,
            "description": "Perform mathematical calculations. Input: mathematical expression like '2+2' or '10*5'"
        }
    }