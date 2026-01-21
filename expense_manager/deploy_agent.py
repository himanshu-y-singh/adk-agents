import os
import logging
from dotenv import load_dotenv

import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines
from .config import config
from .agent import root_agent # Your root Agent definition

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Vertex AI
vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket="gs://" + os.getenv("GOOGLE_CLOUD_PROJECT") + "-bucket"
)

# ✅ Wrap your root agent in AdkApp
app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=False,
)

# ✅ Deploy the app using agent_engines.create
remote_app = agent_engines.create(
    display_name=config.app_name,
    agent_engine=app, # must be the AdkApp
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines,pydantic]",
    ],
    extra_packages=["./expense_manager"], # optional: local directory with custom code
)

logger.info(f"✅ Agent deployed: {remote_app.resource_name}")