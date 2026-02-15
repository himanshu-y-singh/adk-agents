from dataclasses import dataclass, field
import os
from dotenv import load_dotenv
import logging
from config import AppConfig

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
class NexusAgentConfiguration:
    """Configuration for Nexus agent names"""
    nexus_agent_name: str = "nexus_agent"
    job_applicant_agent_name: str = "job_applicant_agent"

@dataclass
class mcp_config:
    toolbox_url: str = os.getenv("TOOLBOX_URL", "http://127.0.0.1:5000")

@dataclass
class NexusConfig(AppConfig):
    """Nexus specific configuration"""
    agent_config: NexusAgentConfiguration = field(
        default_factory=lambda: NexusAgentConfiguration()
    )
    research_config: ResearchConfiguration = field(
        default_factory=lambda: ResearchConfiguration()
    )
    session_memory_config: SessionMemoryConfiguration = field(
        default_factory=lambda: SessionMemoryConfiguration()
    )
    mcp_config: mcp_config = field(
        default_factory=lambda: mcp_config()
    )


config = NexusConfig()

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
