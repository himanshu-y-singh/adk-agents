from pydantic import BaseModel, Field

class Expense(BaseModel):
    amount: float = Field(..., description="The amount of the expense")
    category: str = Field(..., description="The category of the expense (e.g., Food, Transport)")
    description: str = Field(..., description="A brief description of the expense")
    date: str = Field(..., description="The date of the expense in YYYY-MM-DD format")
