import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from app.main import app
from app.appwrite_service import appwrite_service
from app.gemini_service import gemini_service
import uuid

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client():
    """Create an HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test the health endpoint."""
    response = await client.get("/api/health")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test the root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "AI Customer Support Agent API" in data["message"]

@pytest.mark.asyncio
async def test_chat_endpoint_new_session(client):
    """Test chat endpoint with a new session."""
    message_data = {
        "message": "Hello, I need help with my order"
    }
    
    response = await client.post("/api/chat", json=message_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert "timestamp" in data
    assert len(data["session_id"]) > 0
    assert len(data["response"]) > 0

@pytest.mark.asyncio
async def test_chat_endpoint_existing_session(client):
    """Test chat endpoint with an existing session."""
    session_id = str(uuid.uuid4())
    
    # First message
    message_data = {
        "message": "Hello, I need help",
        "session_id": session_id
    }
    
    response = await client.post("/api/chat", json=message_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["session_id"] == session_id
    
    # Second message in same session
    message_data = {
        "message": "My order number is 12345",
        "session_id": session_id
    }
    
    response = await client.post("/api/chat", json=message_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["session_id"] == session_id
    assert len(data["response"]) > 0

@pytest.mark.asyncio
async def test_chat_history_endpoint(client):
    """Test chat history retrieval."""
    session_id = str(uuid.uuid4())
    
    # Send a message first
    message_data = {
        "message": "Test message for history",
        "session_id": session_id
    }
    
    await client.post("/api/chat", json=message_data)
    
    # Get history
    response = await client.get(f"/api/chat/history/{session_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert "session_id" in data
    assert "messages" in data
    assert data["session_id"] == session_id
    assert len(data["messages"]) >= 2  # User message + AI response

@pytest.mark.asyncio
async def test_chat_history_nonexistent_session(client):
    """Test chat history for nonexistent session."""
    fake_session_id = str(uuid.uuid4())
    
    response = await client.get(f"/api/chat/history/{fake_session_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_chat_empty_message(client):
    """Test chat endpoint with empty message."""
    message_data = {
        "message": ""
    }
    
    response = await client.post("/api/chat", json=message_data)
    # Should still work but with empty message
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_chat_long_message(client):
    """Test chat endpoint with a long message."""
    long_message = "This is a very long message. " * 100
    message_data = {
        "message": long_message
    }
    
    response = await client.post("/api/chat", json=message_data)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["response"]) > 0

def test_appwrite_service_mock_mode():
    """Test that AppwriteService initializes in mock mode."""
    assert appwrite_service.use_mock == True
    assert isinstance(appwrite_service.mock_data, dict)

def test_gemini_service_mock_mode():
    """Test that GeminiService initializes in mock mode."""
    assert gemini_service.use_mock == True

@pytest.mark.asyncio
async def test_appwrite_service_operations():
    """Test AppwriteService operations in mock mode."""
    session_id = str(uuid.uuid4())
    
    # Test create conversation
    conversation = await appwrite_service.create_conversation(session_id)
    assert conversation["session_id"] == session_id
    
    # Test get conversation
    retrieved = await appwrite_service.get_conversation(session_id)
    assert retrieved["session_id"] == session_id
    
    # Test add message
    message = await appwrite_service.add_message(session_id, "user", "Test message")
    assert message["session_id"] == session_id
    assert message["role"] == "user"
    assert message["content"] == "Test message"
    
    # Test get messages
    messages = await appwrite_service.get_conversation_messages(session_id)
    assert len(messages) == 1
    assert messages[0]["content"] == "Test message"

@pytest.mark.asyncio
async def test_gemini_service_responses():
    """Test GeminiService response generation."""
    # Test simple response
    response = await gemini_service.generate_simple_response("Hello")
    assert len(response) > 0
    assert "Hello" in response
    
    # Test response with history
    history = [
        {"role": "user", "content": "Hi there"},
        {"role": "assistant", "content": "Hello! How can I help?"}
    ]
    response = await gemini_service.generate_response("Tell me about your services", history)
    assert len(response) > 0