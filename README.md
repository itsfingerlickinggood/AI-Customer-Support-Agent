# AI Customer Support Agent

**An AI-powered customer support agent with contextual memory and RAG.**

## Overview

This project provides an intelligent customer support solution that reduces support load by automatically handling customer inquiries with contextual memory. The system uses retrieval-augmented generation (RAG) to provide accurate, context-aware responses based on conversation history and knowledge base.

## Tech Stack

- **Frontend**: React, TypeScript
- **Backend**: Python, FastAPI
- **AI/ML**: OpenAI API, LangChain
- **Database**: PostgreSQL
- **Additional**: RAG (Retrieval-Augmented Generation), Contextual Memory

## Features

- **Conversational agent with memory**: Maintains context across multiple conversation turns
- **Retrieval-augmented generation (RAG)**: Provides accurate responses based on knowledge base
- **Live chat widget UI in React**: Modern, responsive chat interface
- **Multi-turn support conversations**: Handles complex customer inquiries across multiple exchanges
- **Real-time responses**: Fast, intelligent responses to customer queries
- **Session management**: Tracks and maintains conversation state

## Setup

### Prerequisites

- Node.js 16+ for frontend
- Python 3.8+ for backend
- PostgreSQL (optional for basic setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-customer-support-agent
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Environment Configuration

Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Demo

<!-- ![Demo GIF](docs/demo.gif) -->
*Demo GIF coming soon - showing the chat interface and AI responses*

### Architecture

<!-- ![Architecture Diagram](docs/architecture.png) -->
*Architecture diagram coming soon - showing system components and data flow*

### Live Demo

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
ai-customer-support-agent/
│── frontend/ (React + TypeScript)
│   ├── src/
│   └── README.md
│
│── backend/ (Python + FastAPI)
│   ├── app/
│   ├── routes/
│   ├── models/
│   └── README.md
│
│── docs/
│   ├── architecture.png
│   ├── demo.gif
│   └── usage-guide.md
│
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
