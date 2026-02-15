from google.adk.agents import Agent
from nexus.config import config
from nexus.utils.utils import load_prompt_from_file
from nexus.sub_agents.job_applicant import job_applicant_agent
from nexus.tools import add_work_log, get_work_logs
from toolbox_core import ToolboxSyncClient

# Initialize Context Toolbox if URL is available
toolbox_tools = []
if config.mcp_config.toolbox_url:
    try:
        client = ToolboxSyncClient(config.mcp_config.toolbox_url)
        toolbox_tools = client.load_toolset()
    except Exception:
        pass # Handle gracefully if toolbox is not running

root_agent = Agent(
    name=config.agent_config.nexus_agent_name,
    model=config.research_config.critic_model,
    description="Nexus: Personal Professional Assistant",
    instruction=load_prompt_from_file(f"{config.agent_config.nexus_agent_name}.txt"),
    tools=[add_work_log, get_work_logs] + toolbox_tools,
    sub_agents=[job_applicant_agent]
)
