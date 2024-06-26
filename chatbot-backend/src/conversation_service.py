from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import json
import logging
from datetime import datetime 

from src.chat.chat_service import get_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    logger.info(f"Retrieving conversation with ID {conversation_id}")
    existing_conversation_json = r.get(conversation_id)
    if existing_conversation_json:
        existing_conversation = json.loads(existing_conversation_json)
        return existing_conversation
    else:
        return {"error": "Conversation not found"}

@app.post("/conversations/{conversation_id}")
async def process_conversation(conversation_id: str, conversation: Conversation):
    logger.info(f"Processing conversation with ID {conversation_id}")
    existing_conversation_json = r.get(conversation_id)
    if existing_conversation_json:
        existing_conversation = json.loads(existing_conversation_json)
    else:
        existing_conversation = {"conversation": [{"role": "system", "content": "You are a helpful assistant."}]}

    existing_conversation["conversation"].append(conversation.model_dump()["conversation"][-1])

    user_message = conversation.model_dump()["conversation"][-1]["content"]
    assistant_message = get_response(user_message)

    assistant_message_with_timestamp = {
        "role": "assistant",
        "content": assistant_message,
        "timestamp": datetime.now().isoformat()  # timestamp here
    }

    existing_conversation["conversation"].append(assistant_message_with_timestamp)

    r.set(conversation_id, json.dumps(existing_conversation))

    return existing_conversation


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

