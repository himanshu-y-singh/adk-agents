from typing import List, Dict, Any
from google.adk.tools import ToolContext


# Mock database - in a real app, this would be a DB connection
expenses_db = []

class ToolContext:
    def __init__(self, state: Dict[str, Any] = None):
        self.state = state or {}

def add_expense(tool_context: ToolContext, amount: float, category: str, description: str, date: str) -> str:
    """Adds an expense to the database.
    
    Args:
        context: The tool execution context.
        amount: The amount of the expense.
        category: The category of the expense.
        description: Description of what was purchased.
        date: Date of the expense (YYYY-MM-DD).
    """
    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    tool_context.state["expenses"] = expenses_db
    expenses_db.append(expense)
    return f"Expense added: {expense}"

def get_expenses(tool_context: ToolContext) -> List[Dict[str, Any]]:
    """Retrieves all logged expensesß.
    
    Args:
        context: The tool execution context.
    """
    return tool_context.state["expenses"]
