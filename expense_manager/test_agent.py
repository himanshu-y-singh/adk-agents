import json
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai.types import Content, Part
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os
from pydantic import BaseModel
from config import get_logger
from .config import config
from .agent import root_agent 

logger = get_logger(__name__)

# Load environment variables from .env
load_dotenv()

session_service = InMemorySessionService()
runner = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global runner
    try:
        runner = Runner(
            agent=root_agent,
            app_name=config.app_name,
            session_service=session_service
        )
        logger.info("ADK Runner initialized successfully")
    except Exception as e:
        logger.exception("Failed to initialize ADK Runner")
    yield

    # cleanup logic
    logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan)

class QueryPayload(BaseModel):
    query: str
    user_id: str | None = None
    session_id: str | None = None
    payload: object | None = None

async def get_session_id(user_id: str):
    session = await session_service.create_session(
        app_name=config.app_name,
        user_id=user_id,
    )
    return session.id

def generate_user_query(query: str, payload: object):
    if not payload or not isinstance(payload, dict):
        logger.info('payload is not valid') 
        return query

    formatted_payload = {}
    for key, value in payload.items():
        if isinstance(value, (dict, list)):
            formatted_payload[key] = json.dumps(value)
        else:
            formatted_payload[key] = value

    logger.info(f'formatted_payload => {query.format(**formatted_payload)}')

    return query.format(**formatted_payload)


@app.get("/health") 
def health(): 
    return {"status": "ok"}

@app.post("/query")
async def document(request: QueryPayload):
    try:
        logger.info(f"request => {request}")
        user_id = request.user_id or config.session_memory_config.default_user_id
        user_query = generate_user_query(request.query, request.payload)
        session_id = request.session_id or await get_session_id(user_id)
        user_message = Content(parts=[Part(text=user_query)], role="user")
        logger.info(f"user_message => {user_message}")

        agent_response = ""
        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message
        ):
            if event.is_final_response():
                for part in event.content.parts:
                    if hasattr(part, "text"):
                        agent_response += part.text
                # logger.debug(f"{agent_response}.....................") # Optional debug log
                state = session_service.sessions[config.app_name][user_id][session_id].state
                logger.info(f"state => {state}")

        return {"agent_response": agent_response, "session_id": session_id, "user_id": user_id, "state": state}
    except Exception as e:
        logger.exception("Error processing query")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "expense_manager.test_agent:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        reload = True
    )
