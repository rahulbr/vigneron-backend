.PHONY: help install dev-install setup clean test lint format type-check pre-commit
.PHONY: server db-up db-down db-reset migration migrate rollback seed
.PHONY: docker-build docker-up docker-down docker-logs
.PHONY: check-all ci build deploy

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
UVICORN := uvicorn
ALEMBIC := alembic
SUPABASE := npx supabase
PORT := 8000
HOST := 0.0.0.0

help: ## Show this help message
	@echo "Vigneron AI Backend - Development Commands"
	@echo "==========================================\n"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Setup and Installation
install: ## Install production dependencies
	$(PIP) install -e .

dev-install: ## Install all dependencies including dev tools
	$(PIP) install -e ".[dev]"

setup: ## Complete project setup for new developers
	@echo "Setting up Vigneron AI Backend..."
	make dev-install
	cp .env.example .env
	@echo "Please edit .env file with your configuration"
	make db-up
	make migrate
	@echo "Setup complete! Run 'make server' to start development"

clean: ## Clean up cache files and temporary directories
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Development Server
server: ## Start the development server with hot reload
	$(UVICORN) app.main:app --reload --host $(HOST) --port $(PORT)

server-prod: ## Start the production server
	$(UVICORN) app.main:app --host $(HOST) --port $(PORT) --workers 4

# Database Operations
db-up: ## Start Supabase local development environment
	$(SUPABASE) start

db-down: ## Stop Supabase local development environment
	$(SUPABASE) stop

db-reset: ## Reset local database (WARNING: Destroys all data)
	$(SUPABASE) db reset

db-status: ## Show database status
	$(SUPABASE) status

migration: ## Create a new database migration
	@read -p "Enter migration description: " desc; \
	$(ALEMBIC) revision --autogenerate -m "$$desc"

migrate: ## Apply all pending migrations
	$(ALEMBIC) upgrade head

rollback: ## Rollback last migration
	$(ALEMBIC) downgrade -1

db-history: ## Show migration history
	$(ALEMBIC) history

seed: ## Seed database with sample data
	$(PYTHON) scripts/seed_db.py

# Code Quality
format: ## Format code with black and isort
	black app/ tests/ --line-length 88
	isort app/ tests/ --profile black

lint: ## Run linting with flake8
	flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503

type-check: ## Run type checking with mypy
	mypy app/ --ignore-missing-imports

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

check-all: format lint type-check ## Run all code quality checks

# Testing
test: ## Run all tests
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	pytest tests/ -v --tb=short -x --looponfail

test-integration: ## Run integration tests only
	pytest tests/integration/ -v

test-unit: ## Run unit tests only
	pytest tests/unit/ -v

# Docker Operations
docker-build: ## Build Docker image
	docker build -t vigneron-backend:latest .

docker-up: ## Start services with Docker Compose
	docker-compose up -d

docker-down: ## Stop Docker Compose services
	docker-compose down

docker-logs: ## Show Docker Compose logs
	docker-compose logs -f

# CI/CD and Production
ci: ## Run CI pipeline locally
	make check-all
	make test-cov
	make build

build: ## Build production artifacts
	@echo "Building production artifacts..."
	make clean
	$(PYTHON) -m pip wheel --no-deps -w dist/ .

deploy-staging: ## Deploy to staging environment
	@echo "Deploying to staging..."
	# Add your staging deployment commands here

deploy-prod: ## Deploy to production environment
	@echo "Deploying to production..."
	# Add your production deployment commands here

# Utilities
shell: ## Open Python shell with app context
	$(PYTHON) -c "from app.main import app; from app.db.base import get_db; import IPython; IPython.embed()"

requirements: ## Show currently installed packages
	$(PIP) list

security-check: ## Run security checks
	safety check
	bandit -r app/

docs: ## Generate API documentation
	$(PYTHON) scripts/generate_docs.py

logs: ## Show application logs
	tail -f logs/app.log

# Health checks
health: ## Check application health
	curl -f http://localhost:$(PORT)/health || exit 1

health-db: ## Check database health
	curl -f http://localhost:$(PORT)/api/v1/health/db || exit 1