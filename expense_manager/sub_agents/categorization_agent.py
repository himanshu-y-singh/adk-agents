from google.adk.agents import Agent
from expense_manager.config import config
from expense_manager.utils.utils import load_prompt_from_file


categorization_agent = Agent(
    name=config.agent_config.categorization_agent_name,
    model=config.research_config.critic_model,
    description="Categorizes an expense description into predefined categories.",
    instruction=load_prompt_from_file(f"{config.agent_config.categorization_agent_name}.txt"),
)
