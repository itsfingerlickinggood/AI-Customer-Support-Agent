# Backend - AI Customer Support Agent

This is the Python + FastAPI backend for the AI Customer Support Agent.

## Features

- FastAPI REST API
- OpenAI API integration
- LangChain for RAG
- PostgreSQL database
- Contextual memory for conversations

## Getting Started

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Tech Stack

- Python 3.8+
- FastAPI
- OpenAI API
- LangChain
- PostgreSQL
- SQLAlchemy
- Pydantic