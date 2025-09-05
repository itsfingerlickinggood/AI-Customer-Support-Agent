from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from app.config import settings
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AppwriteService:
    def __init__(self):
        self.use_mock = True  # Start in mock mode for demo
        self.mock_data = {}  # In-memory storage for demo
        
        # Only try to initialize Appwrite if API key looks valid
        if (settings.appwrite_api_key != "demo_api_key" and 
            settings.appwrite_project_id != "demo_project"):
            try:
                # Initialize Appwrite client
                self.client = Client()
                self.client.set_endpoint(settings.appwrite_endpoint)
                self.client.set_project(settings.appwrite_project_id)
                self.client.set_key(settings.appwrite_api_key)
                
                # Initialize database service
                self.databases = Databases(self.client)
                self.use_mock = False
                logger.info("Appwrite client initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize Appwrite client: {str(e)}. Using mock mode.")
                self.use_mock = True
        else:
            logger.info("Using demo/mock mode for Appwrite (no real API keys configured)")
        
    async def create_conversation(self, session_id: str) -> Dict[str, Any]:
        """Create a new conversation in Appwrite or mock storage"""
        if self.use_mock:
            if session_id not in self.mock_data:
                self.mock_data[session_id] = {
                    "conversation": {
                        "session_id": session_id,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    "messages": []
                }
            return self.mock_data[session_id]["conversation"]
        
        try:
            return self.databases.create_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_conversations_collection_id,
                document_id=session_id,
                data={
                    "session_id": session_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            )
        except AppwriteException as e:
            if e.code == 409:  # Document already exists
                return await self.get_conversation(session_id)
            logger.error(f"Appwrite error creating conversation: {str(e)}")
            # Fallback to mock
            self.use_mock = True
            return await self.create_conversation(session_id)
        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}")
            # Fallback to mock
            self.use_mock = True
            return await self.create_conversation(session_id)
    
    async def get_conversation(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation by session ID"""
        if self.use_mock:
            if session_id in self.mock_data:
                return self.mock_data[session_id]["conversation"]
            return None
        
        try:
            return self.databases.get_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_conversations_collection_id,
                document_id=session_id
            )
        except AppwriteException as e:
            if e.code == 404:
                return None
            logger.error(f"Appwrite error getting conversation: {str(e)}")
            # Fallback to mock
            self.use_mock = True
            return await self.get_conversation(session_id)
        except Exception as e:
            logger.error(f"Error getting conversation: {str(e)}")
            # Fallback to mock
            self.use_mock = True
            return await self.get_conversation(session_id)
    
    async def add_message(self, session_id: str, role: str, content: str) -> Dict[str, Any]:
        """Add a message to a conversation"""
        message_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        message_data = {
            "id": message_id,
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        
        if self.use_mock:
            if session_id not in self.mock_data:
                await self.create_conversation(session_id)
            self.mock_data[session_id]["messages"].append(message_data)
            await self.update_conversation_timestamp(session_id)
            return message_data
        
        try:
            # Create message document
            message = self.databases.create_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_messages_collection_id,
                document_id=message_id,
                data=message_data
            )
            
            # Update conversation timestamp
            await self.update_conversation_timestamp(session_id)
            
            return message
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            # Fallback to mock
            self.use_mock = True
            return await self.add_message(session_id, role, content)
    
    async def get_conversation_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a conversation"""
        if self.use_mock:
            if session_id in self.mock_data:
                return self.mock_data[session_id]["messages"]
            return []
        
        try:
            from appwrite.query import Query
            
            result = self.databases.list_documents(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_messages_collection_id,
                queries=[
                    Query.equal("session_id", session_id),
                    Query.order_desc("timestamp")
                ]
            )
            
            # Reverse to get chronological order
            messages = result['documents']
            messages.reverse()
            return messages
        except Exception as e:
            logger.error(f"Error getting messages: {str(e)}")
            # Fallback to mock
            self.use_mock = True
            return await self.get_conversation_messages(session_id)
    
    async def update_conversation_timestamp(self, session_id: str):
        """Update the last updated timestamp of a conversation"""
        if self.use_mock:
            if session_id in self.mock_data:
                self.mock_data[session_id]["conversation"]["updated_at"] = datetime.now().isoformat()
            return
        
        try:
            self.databases.update_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_conversations_collection_id,
                document_id=session_id,
                data={
                    "updated_at": datetime.now().isoformat()
                }
            )
        except AppwriteException:
            # If conversation doesn't exist, create it
            await self.create_conversation(session_id)
        except Exception as e:
            logger.error(f"Error updating conversation timestamp: {str(e)}")
            # Fallback to mock
            self.use_mock = True
            await self.update_conversation_timestamp(session_id)

# Global instance
appwrite_service = AppwriteService()