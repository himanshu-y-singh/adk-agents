from google.adk.agents import Agent
from nexus.config import config
from nexus.utils.utils import load_prompt_from_file

resume = load_prompt_from_file("resume_himanshu.txt")
instruction = load_prompt_from_file(f"{config.agent_config.job_applicant_agent_name}.txt").replace("{(resume)}", resume)

job_applicant_agent = Agent(
    name=config.agent_config.job_applicant_agent_name,
    model=config.research_config.critic_model,
    description="Helps finding and applying for jobs.",
    instruction=instruction,
)
 

