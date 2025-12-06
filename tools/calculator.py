"""
Calculator Tool

Provides mathematical calculation capabilities to the agent.
Uses Python's eval() with safety restrictions.
"""

import ast
import operator


# Safe operators for mathematical expressions
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    """
    Safely evaluate a mathematical expression AST node.
    
    This prevents code injection by only allowing mathematical operations.
    """
    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    elif isinstance(node, ast.Num):  # Python 3.7 compatibility
        return node.n
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsafe operator: {op_type.__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return SAFE_OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsafe operator: {op_type.__name__}")
        operand = _safe_eval(node.operand)
        return SAFE_OPERATORS[op_type](operand)
    else:
        raise ValueError(f"Unsafe expression type: {type(node).__name__}")


def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    Args:
        expression: Mathematical expression like "2+2", "10*5", "(3+4)*2"
    Returns:
        Result of the calculation or error message
    """
    try:
        # Remove whitespace
        expression = expression.strip()
        
        # Parse the expression into an AST
        tree = ast.parse(expression, mode='eval')
        
        # Safely evaluate the AST
        result = _safe_eval(tree.body)
        
        return f"Result: {result}"
    
    except SyntaxError:
        return f"Error: Invalid mathematical expression '{expression}'"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error calculating: {str(e)}"