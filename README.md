# AI Customer Support Agent

**An AI-powered customer support agent with contextual memory using Google Gemini API and Appwrite.**

## Overview

This project provides an intelligent customer support solution that reduces support load by automatically handling customer inquiries with contextual memory. The system uses Google Gemini API for AI responses and Appwrite for data storage, providing accurate, context-aware responses based on conversation history.

## Tech Stack

- **Frontend**: React, TypeScript
- **Backend**: Python, FastAPI
- **AI/ML**: Google Gemini API, LangChain
- **Database**: Appwrite
- **Additional**: Contextual Memory, Real-time Responses

## Features

- **🤖 AI-Powered Responses**: Uses Google Gemini for intelligent customer support
- **💬 Contextual Memory**: Maintains conversation context using Appwrite database
- **⚡ Real-time Chat**: Modern React chat interface with instant responses
- **📱 Mobile Responsive**: Works perfectly on all device sizes
- **🔒 Session Management**: Persistent conversations across page refreshes
- **🛡️ Error Handling**: Graceful fallbacks and user-friendly error messages
- **🧪 Comprehensive Testing**: Full test coverage for backend and frontend

## Demo Screenshots

![Homepage](https://github.com/user-attachments/assets/4c146009-ea5c-43dd-b8bd-592169aa7ed3)

![Chat Interface](https://github.com/user-attachments/assets/7ec28ff4-05ec-41cc-bf0e-a87e1bdeadfe)

## Setup

### Prerequisites

- Node.js 16+ for frontend
- Python 3.8+ for backend
- Google Gemini API key (optional for demo mode)
- Appwrite account (optional for demo mode)

### Quick Start (Demo Mode)

The application includes demo/mock modes that work without API keys for testing:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Customer-Support-Agent
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Production Setup

For production deployment with real APIs:

#### 1. Get API Keys

**Google Gemini API:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key for environment configuration

**Appwrite Setup:**
1. Create an account at [Appwrite Cloud](https://appwrite.io/)
2. Create a new project
3. Create a database named "main"
4. Create collections: "conversations" and "messages"
5. Copy project ID and create an API key

#### 2. Environment Configuration

Create a `.env` file in the backend directory:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key

# Appwrite Configuration
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_DATABASE_ID=main
APPWRITE_CONVERSATIONS_COLLECTION_ID=conversations
APPWRITE_MESSAGES_COLLECTION_ID=messages

# Application Configuration
ENVIRONMENT=production
DEBUG=false
```

#### 3. Appwrite Database Schema

**Conversations Collection:**
- `session_id` (string, required)
- `created_at` (datetime)
- `updated_at` (datetime)

**Messages Collection:**
- `session_id` (string, required)
- `role` (string, required) - "user" or "assistant"
- `content` (string, required)
- `timestamp` (datetime)

## Testing

### Backend Tests
```bash
cd backend
pytest test_main.py -v
```

### Frontend Tests
```bash
cd frontend
npm test -- --watchAll=false
```

### Manual Testing
1. Start both backend and frontend servers
2. Open http://localhost:3000
3. Click the chat widget in the bottom right
4. Send test messages to verify functionality

## Project Structure

```
AI-Customer-Support-Agent/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app configuration
│   │   ├── config.py          # Settings management
│   │   ├── gemini_service.py  # Gemini AI integration
│   │   └── appwrite_service.py # Appwrite database integration
│   ├── routes/
│   │   ├── chat.py            # Chat API endpoints
│   │   └── health.py          # Health check endpoint
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── test_main.py          # Backend tests
│
├── frontend/                  # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx           # Main application component
│   │   ├── ChatWidget.tsx    # Chat interface component
│   │   ├── ChatWidget.css    # Chat widget styles
│   │   └── __tests__/        # Frontend tests
│   ├── package.json          # Node.js dependencies
│   └── public/               # Static files
│
└── README.md                 # This file
```

## API Endpoints

### Chat Endpoints

**POST /api/chat**
- Send a message to the AI assistant
- Body: `{"message": "string", "session_id": "optional_string"}`
- Response: `{"response": "string", "session_id": "string", "timestamp": "datetime"}`

**GET /api/chat/history/{session_id}**
- Retrieve conversation history
- Response: `{"session_id": "string", "messages": [...]}`

**GET /api/health**
- Health check endpoint
- Response: `{"status": "healthy"}`

## Key Features

### Intelligent AI Responses
- Powered by Google Gemini API
- Context-aware responses using conversation history
- Professional customer support prompting
- Fallback responses for error handling

### Persistent Storage
- Conversation storage using Appwrite
- Session management across page refreshes
- Message history tracking
- Real-time data synchronization

### Modern Frontend
- React with TypeScript for type safety
- Responsive design for all devices
- Smooth animations and transitions
- Professional customer support UI/UX

### Comprehensive Testing
- Backend API tests with pytest
- Frontend component tests with Jest
- Integration tests for complete workflows
- Mock implementations for development

## Deployment

### Backend Deployment
1. Set up environment variables
2. Install dependencies: `pip install -r requirements.txt`
3. Run with: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Frontend Deployment
1. Build production version: `npm run build`
2. Serve the build folder with any static file server
3. Update API proxy settings for production backend URL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.
