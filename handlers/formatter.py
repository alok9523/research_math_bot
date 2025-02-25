def format_math_expression(expression: str) -> str:
    # Example: Replace * with × and / with ÷
    return expression.replace("*", "×").replace("/", "÷")

def format_latex(expression: str) -> str:
    # Example: Wrap expression in LaTeX format
    return f"`{expression}`"

def format_markdown(expression: str) -> str:
    # Example: Wrap expression in Markdown format
    return f"**{expression}**"
