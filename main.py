import json
from fastapi import FastAPI
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from db import router as db_router
from config import get_logger

logger = get_logger(__name__)
 
# Load environment variables from .env
load_dotenv()
 
app = FastAPI()
app.include_router(db_router)

class DocumentationQueryPayload(BaseModel):
    query: str
    user_id: str | None = None
    session_id: str | None = None
    payload: object | None = None

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
def health(): return {"status": "ok"}
 
@app.post("/expense")
async def expense(request: DocumentationQueryPayload):
    user_query = generate_user_query(request.query, request.payload)
    user_id = request.user_id
    session_id = request.session_id
    agent_path = os.getenv("DOCUMENTATION_AGENT_RESOURCE_NAME")
    return call_expense_manager_agent(user_query, agent_path, session_id, user_id)
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        reload = True
 )
