from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime

# In-memory storage for demo purposes
conversations = {}

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Handle chat messages with contextual memory
    """
    try:
        # Generate or use existing session ID
        session_id = message.session_id or str(uuid.uuid4())
        
        # Initialize conversation history if new session
        if session_id not in conversations:
            conversations[session_id] = []
        
        # Add user message to history
        conversations[session_id].append({
            "role": "user",
            "content": message.message,
            "timestamp": datetime.now()
        })
        
        # Simple echo response for now (would integrate OpenAI API here)
        response_text = f"Thank you for your message: '{message.message}'. How can I help you further?"
        
        # Add assistant response to history
        conversations[session_id].append({
            "role": "assistant", 
            "content": response_text,
            "timestamp": datetime.now()
        })
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """
    Retrieve chat history for a session
    """
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"session_id": session_id, "messages": conversations[session_id]}