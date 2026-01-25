from dataclasses import dataclass, field
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ResearchConfiguration:
    """ configuration for research related models and parameters

    Attributes:
        critic_model (str): Model for evaluation tasks.
        worker_model (str): Model for worker tasks.
    """

    critic_model: str = os.getenv("CRITIC_MODEL", "gemini-2.5-flash")
    worker_model: str = os.getenv("WORKER_MODEL", "gemini-2.5-flash-lite")

@dataclass
class SessionMemoryConfiguration:
    """ configuration for session state and memory of agent

    Attributes:
        default_user_id (int): Default user id to be used when no user id is provided.
        output_key (dict): A dictionary of keys to be used to store the output of the agent.
              - key: The name of the agent
              - value: The name of the session state variable to store the response of the agent  
        state_variables (dict): Dictionary of state variables to be used by the agent.
    """
    default_user_id: int = os.getenv("DEFAULT_USER_ID", "userabc")
    output_key: dict = field(
        default_factory=lambda: {
        "expense_manager": "expense_manager_response"
        }
    )
    
    state_variables: dict = field(
        default_factory=lambda: {
        "expense_manager": "expense_manager_response"
        }
    )
    

@dataclass
class AgentConfiguration:
    """ configuration for agent names """
    expense_manager_agent_name: str = "expense_manager"
    categorization_agent_name: str = "categorization_agent"

@dataclass
class McpConfiguration:
    """ configuration for mcp """
    toolbox_url: str = os.getenv("TOOLBOX_URL", "http://127.0.0.1:5000")    
    
@dataclass
class AppConfig:
    """ The central configuration class for the application. """

    debug_mode: bool = os.getenv("DEBUG_MODE", True)
    app_name: str = os.getenv("APP_NAME", "expense_manager")
    log_level: str = os.getenv("LOG_LEVEL", "debug")

    research_config: ResearchConfiguration = field(
        default_factory=lambda: ResearchConfiguration()
    )
    session_memory_config: SessionMemoryConfiguration = field(
        default_factory=lambda: SessionMemoryConfiguration()
    )
    agent_config: AgentConfiguration = field(
        default_factory=lambda: AgentConfiguration()
    )
    mcp_config: McpConfiguration = field(
        default_factory=lambda: McpConfiguration()
    )
    
config = AppConfig()
