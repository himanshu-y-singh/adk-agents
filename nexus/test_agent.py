import asyncio
import json
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai.types import Content, Part
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os
from pydantic import BaseModel
from nexus.config import config, configure_logging, get_logger
from nexus.agent import root_agent
import logging
import uvicorn

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

session_service = InMemorySessionService()
runner = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global runner
    try:
        runner = Runner(
            agent=root_agent,
            app_name=config.app_name, # Can share app name or use nexus specific
            session_service=session_service
        )
        logger.info("Nexus Runner initialized successfully")
    except Exception as e:
        logger.exception("Failed to initialize Nexus Runner")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)
configure_logging(config)

class QueryPayload(BaseModel):
    query: str
    user_id: str | None = None
    session_id: str | None = None

@app.post("/query")
async def query_nexus(request: QueryPayload):
    try:
        user_id = request.user_id or config.session_memory_config.default_user_id
        session_id = request.session_id or await session_service.create_session(config.app_name, user_id).id
        
        user_message = Content(parts=[Part(text=request.query)], role="user")
        
        agent_response = ""
        for event in runner.run(user_id=user_id, session_id=session_id, new_message=user_message):
            if event.is_final_response():
                 for part in event.content.parts:
                    if hasattr(part, "text"):
                        agent_response += part.text
        
        return {"response": agent_response}
    except Exception as e:
        logger.exception("Error processing query")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "nexus.test_agent:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8081)),
        reload=True
    )
