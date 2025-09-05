from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
import logging
from app.gemini_service import gemini_service
from app.appwrite_service import appwrite_service
from appwrite.exception import AppwriteException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Handle chat messages with Gemini AI and Appwrite storage
    """
    try:
        # Generate or use existing session ID
        session_id = message.session_id or str(uuid.uuid4())
        
        logger.info(f"Processing chat message for session: {session_id}")
        
        # Ensure conversation exists in Appwrite
        await appwrite_service.create_conversation(session_id)
        
        # Get conversation history for context
        try:
            conversation_history = await appwrite_service.get_conversation_messages(session_id)
        except Exception as e:
            logger.warning(f"Could not fetch conversation history: {str(e)}")
            conversation_history = []
        
        # Add user message to Appwrite
        try:
            await appwrite_service.add_message(session_id, "user", message.message)
        except Exception as e:
            logger.warning(f"Could not save user message to Appwrite: {str(e)}")
        
        # Generate AI response using Gemini
        try:
            # If we have conversation history, use it for context
            if conversation_history:
                ai_response = await gemini_service.generate_response(
                    message.message, 
                    conversation_history
                )
            else:
                # Fallback to simple response if no history
                ai_response = await gemini_service.generate_simple_response(message.message)
                
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            ai_response = "I apologize, but I'm experiencing technical difficulties. How else can I assist you today?"
        
        # Add AI response to Appwrite
        try:
            await appwrite_service.add_message(session_id, "assistant", ai_response)
        except Exception as e:
            logger.warning(f"Could not save AI response to Appwrite: {str(e)}")
        
        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again.")

@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """
    Retrieve chat history for a session from Appwrite
    """
    try:
        # Check if conversation exists
        conversation = await appwrite_service.get_conversation(session_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get messages
        messages = await appwrite_service.get_conversation_messages(session_id)
        
        return {
            "session_id": session_id, 
            "conversation": conversation,
            "messages": messages
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve chat history")

@router.get("/chat/sessions")
async def list_chat_sessions():
    """
    List all chat sessions (for admin/debugging purposes)
    """
    try:
        # This is a simplified implementation
        # In production, you'd want pagination and user filtering
        return {"message": "Session listing not implemented yet - use specific session_id"}
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not list sessions")