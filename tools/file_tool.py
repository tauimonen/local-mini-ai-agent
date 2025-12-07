"""
File Tool

Provides file reading and writing capabilities to the agent.
Docker version: Works with /app/data directory.
"""

import os

# Docker-aware data directory
DATA_DIR = "/app/data" if os.path.exists("/app/data") else "."


def read_file(filepath: str) -> str:
    """
    Read the contents of a text file.
    Args:
        filepath: Path to the file to read
    Returns:
        Contents of the file or error message
    """
    try:
        # Security: Prevent reading files outside data directory
        filepath = os.path.basename(filepath)
        full_path = os.path.join(DATA_DIR, filepath)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"File '{filepath}' contents:\n{content}"
    
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found in {DATA_DIR}"
    except PermissionError:
        return f"Error: No permission to read '{filepath}'"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(input_str: str) -> str:
    """
    Write content to a text file.
    Args:
        input_str: String in format "filepath|content" where | separates path and content
    Returns:
        Success message or error
    """
    try:
        # Parse the input
        if '|' not in input_str:
            return "Error: Input must be in format 'filepath|content'"
        
        filepath, content = input_str.split('|', 1)
        filepath = filepath.strip()
        content = content.strip()
        
        # Security: Prevent writing files outside data directory
        filepath = os.path.basename(filepath)
        full_path = os.path.join(DATA_DIR, filepath)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Successfully wrote {len(content)} characters to '{filepath}'"
    
    except PermissionError:
        return f"Error: No permission to write to '{filepath}'"
    except Exception as e:
        return f"Error writing file: {str(e)}"