from google.adk.agents import Agent
from expense_manager.config import config
from expense_manager.tools import add_expense, get_expenses
from expense_manager.utils.utils import load_prompt_from_file
from expense_manager.sub_agents.categorization_agent import categorization_agent

instruction = load_prompt_from_file(f"{config.agent_config.expense_manager_agent_name}.txt")

expense_manager_agent = Agent(
    name=config.agent_config.expense_manager_agent_name,
    model=config.research_config.worker_model,
    description="This is the root agent for expense manager application",
    instruction=instruction,
    sub_agents=[categorization_agent]
)

root_agent = expense_manager_agent
    
