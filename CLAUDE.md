# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the backend for Vigneron AI, built with FastAPI and PostgreSQL (via Supabase). The backend provides REST API endpoints to drive the vigneron-ai frontend application.

## Technology Stack

- **FastAPI**: Modern Python web framework for building APIs
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Database (via Supabase)
- **Supabase**: Backend-as-a-Service platform providing PostgreSQL hosting
- **Uvicorn**: ASGI server for running FastAPI

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js (for Supabase CLI via npx)

### Installation
```bash
# Install Python dependencies (development mode with dev tools)
pip install -e ".[dev]"

# Or use the Makefile
make dev-install

# Copy environment variables template
cp .env.example .env
# Edit .env with your actual Supabase credentials
```

### Local Development with Supabase

```bash
# Start Supabase local development environment
npx supabase start

# Run database migrations
alembic upgrade head

# Start the FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## Project Architecture

### Directory Structure
```
app/
├── api/
│   └── api_v1/
│       ├── api.py          # API router configuration
│       └── endpoints/      # API endpoint definitions
├── core/
│   └── config.py          # Application configuration
├── db/
│   └── base.py            # Database connection and session management
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic schemas for request/response
└── main.py               # FastAPI application entry point

alembic/                  # Database migration files
supabase/                 # Supabase configuration and functions
```

### API Design
- RESTful API following OpenAPI/Swagger standards
- Versioned API endpoints under `/api/v1/`
- Health check endpoints at `/health` and `/api/v1/health/`
- Automatic API documentation at `/docs` (Swagger UI)

### Database Layer
- SQLAlchemy ORM for database operations
- Alembic for database schema migrations
- Connection to Supabase PostgreSQL instance
- Database session management with dependency injection

## Environment Variables

Required environment variables (see .env.example):
- `DATABASE_URL`: PostgreSQL connection string
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role key (for admin operations)