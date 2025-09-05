# AI Customer Support Agent - Usage Guide

## Getting Started

### Prerequisites

- Node.js 16+ for frontend
- Python 3.8+ for backend
- PostgreSQL database (optional for basic setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-customer-support-agent
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   The API will be available at http://localhost:8000

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm start
   ```
   The frontend will be available at http://localhost:3000

### API Usage

#### Send a chat message
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, I need help with my order"}'
```

#### Get conversation history
```bash
curl "http://localhost:8000/api/chat/history/{session_id}"
```

### Configuration

#### Environment Variables (Backend)
Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Features

- **Conversational AI**: Natural language processing for customer queries
- **Memory**: Maintains context across conversation turns
- **RAG**: Retrieval-augmented generation for accurate responses
- **Live Chat**: Real-time chat interface
- **Multi-turn Support**: Handles complex conversations

### Architecture

- **Frontend**: React + TypeScript SPA
- **Backend**: FastAPI Python service
- **Database**: PostgreSQL for conversation storage
- **AI**: OpenAI GPT models with LangChain

### Development

#### Adding New Features

1. Backend API endpoints go in `backend/routes/`
2. Frontend components go in `frontend/src/components/`
3. Data models go in `backend/models/`

#### Testing

- Backend: `pytest`
- Frontend: `npm test`