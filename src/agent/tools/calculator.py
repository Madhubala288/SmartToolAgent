
import ast
import math
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

MAX_EXPRESSION_LENGTH = 200
MAX_EXPONENT = 1000
MAX_RESULT_MAGNITUDE = 1e100


def calculator(expression: str) -> float:
    """
    Safely calculate a mathematical expression.

    Supports +, -, *, /, %, and **.
    Limits expression length, exponent size, and result magnitude.
    The % operator calculates the remainder.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Expression must be a non-empty string.")

    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError(
            f"Expression is too long (maximum {MAX_EXPRESSION_LENGTH} characters)."
        )

    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError) as error:
        raise ValueError("Invalid mathematical expression.") from error

    def check_result(value):
        if isinstance(value, complex) or not isinstance(value, (int, float)):
            raise ValueError("The result must be a real number.")

        if not math.isfinite(value):
            raise ValueError("The result must be finite.")

        if abs(value) > MAX_RESULT_MAGNITUDE:
            raise ValueError("Result is too large.")

        return value

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            # bool is a subclass of int, so reject it explicitly.
            if isinstance(node.value, bool):
                raise ValueError("Boolean values are not allowed.")

            if isinstance(node.value, (int, float)):
                return check_result(node.value)

            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported mathematical operation.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow):
                if abs(right) > MAX_EXPONENT:
                    raise ValueError(
                        f"Exponent magnitude cannot exceed {MAX_EXPONENT}."
                    )
                if abs(left) > 1e6 and right > 1:
                    raise ValueError("Base is too large for exponentiation.")

            result = operation(left, right)
            return check_result(result)

        if isinstance(node, ast.UnaryOp):
            value = evaluate(node.operand)

            if isinstance(node.op, ast.USub):
                return check_result(-value)

            if isinstance(node.op, ast.UAdd):
                return check_result(value)

            raise ValueError("Unsupported unary operation.")

        raise ValueError("Invalid mathematical expression.")

    return evaluate(tree)
