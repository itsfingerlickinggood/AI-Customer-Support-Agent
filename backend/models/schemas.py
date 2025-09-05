from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Message(BaseModel):
    id: Optional[int] = None
    content: str
    role: str  # 'user' or 'assistant'
    session_id: str
    timestamp: datetime
    
class Conversation(BaseModel):
    session_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []

class User(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    name: Optional[str] = None
    created_at: datetime