# Vigneron AI Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Supabase](https://img.shields.io/badge/Supabase-Latest-3ECF8E.svg?style=flat&logo=supabase&logoColor=white)](https://supabase.com)

A high-performance, production-ready FastAPI backend powering the Vigneron AI frontend application. Built with modern Python practices, comprehensive testing, and seamless database integration via Supabase.

## 🚀 Features

- **FastAPI Framework**: Modern, fast Python web framework with automatic API documentation
- **PostgreSQL + Supabase**: Robust database with real-time capabilities and built-in auth
- **SQLAlchemy ORM**: Type-safe database operations with Alembic migrations
- **Comprehensive Testing**: Unit, integration, and API tests with coverage reporting
- **Code Quality**: Pre-commit hooks, linting, formatting, and type checking
- **Developer Experience**: Hot reload, rich debugging, and extensive tooling
- **Production Ready**: Docker support, health checks, and monitoring capabilities

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Database Management](#database-management)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Deployment](#deployment)
- [Contributing](#contributing)

## ⚡ Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd vigneron-backend
make setup

# Start development
make server
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🛠 Development Setup

### Prerequisites

- **Python 3.8+** - [Download](https://python.org/downloads/)
- **Node.js 18+** - Required for Supabase CLI
- **PostgreSQL** - Or use Supabase (recommended)

### Installation

1. **Environment Setup**
   ```bash
   # Install dependencies
   make dev-install
   
   # Copy environment template
   cp .env.example .env
   ```

2. **Configure Environment Variables**
   
   Edit `.env` with your configuration:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:54322/postgres
   SUPABASE_URL=http://localhost:54321
   SUPABASE_ANON_KEY=your_anon_key_here
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
   ```

3. **Database Setup**
   ```bash
   # Start Supabase local development
   make db-up
   
   # Run migrations
   make migrate
   ```

4. **Start Development Server**
   ```bash
   make server
   ```

## 📁 Project Structure

```
vigneron-backend/
├── app/                    # Application source code
│   ├── api/               # API routes and endpoints
│   │   └── api_v1/       # Versioned API endpoints
│   │       ├── api.py    # Router configuration
│   │       └── endpoints/ # Individual endpoint modules
│   ├── core/             # Core application configuration
│   │   └── config.py     # Settings and environment variables
│   ├── db/               # Database configuration
│   │   └── base.py       # SQLAlchemy setup and session management
│   ├── models/           # SQLAlchemy database models
│   ├── schemas/          # Pydantic request/response schemas
│   └── main.py           # FastAPI application factory
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   └── env.py           # Alembic configuration
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── conftest.py      # Test configuration
├── supabase/             # Supabase configuration
├── scripts/              # Utility scripts
├── docs/                 # Project documentation
├── Makefile             # Development commands
├── pyproject.toml       # Project configuration and dependencies
├── .env.example         # Environment template
└── README.md           # This file
```

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Database connectivity
curl http://localhost:8000/api/v1/health/db
```

## 🗄 Database Management

### Migrations

```bash
# Create new migration
make migration

# Apply migrations
make migrate

# Rollback last migration
make rollback

# View migration history
make db-history
```

### Local Development

```bash
# Start Supabase locally
make db-up

# Stop Supabase
make db-down

# Reset database (WARNING: Destroys data)
make db-reset

# Check status
make db-status
```

## 🧪 Testing

### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Watch mode (re-runs on file changes)
make test-watch

# Specific test types
make test-unit
make test-integration
```

### Test Structure

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and database operations
- **Coverage**: Aim for >90% code coverage

## 🔍 Code Quality

### Automated Checks

```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# All quality checks
make check-all
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
make pre-commit
```

### Code Standards

- **Formatting**: Black with 88 character line length
- **Import Sorting**: isort with Black profile
- **Linting**: flake8 with sensible defaults
- **Type Checking**: mypy for static type analysis

## 🚢 Deployment

### Docker

```bash
# Build image
make docker-build

# Run with Docker Compose
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

### Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL certificates configured
- [ ] Health checks enabled
- [ ] Monitoring and logging setup
- [ ] Security headers configured
- [ ] Rate limiting implemented

## 🤝 Contributing

### Development Workflow

1. **Fork and Clone**
   ```bash
   git clone <your-fork>
   cd vigneron-backend
   make setup
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Development**
   ```bash
   # Make changes
   make check-all  # Ensure code quality
   make test       # Run tests
   ```

4. **Submit PR**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

### Code Style

- Follow PEP 8 and Black formatting
- Write comprehensive docstrings
- Add type hints to all functions
- Write tests for new features
- Update documentation as needed

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Supabase Documentation](https://supabase.com/docs)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## 🆘 Support

For questions and support:

1. Check the [API documentation](http://localhost:8000/docs)
2. Review the [CLAUDE.md](./CLAUDE.md) for development guidance
3. Search existing [issues](../../issues)
4. Create a new [issue](../../issues/new) if needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
