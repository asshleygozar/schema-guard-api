# Schema Guard API
An AI powered Database Schema Intelligence Platform designed to detect breaking database schema changes and provide warnings, analysis, recommendation, and feedback to automate schema detection changes.

## Technology Stack
- **Backend**
    - Python
    - FastAPI
    - SQLAlchemy

- **Infrastructure**
    - PostgreSQL
    - Redis
    - Docker
    - Github Actions

- **AI**
    - OpenAI API

## Setting Up (Development)

**Environment Variables**
Before you can get started you have to setup your environment variables. Create your own copy of the env file and fill up the required variables. Copy the env example using this command to create your own .env file 
```bash
cp .env.example .env
```

## Development
Complete guide on workarounds during development and improvement of the api

### Schema Changes
Steps for changing database schemas using alembic for tracking migration and sqlalchemy for database schema

**Step 1:** For creating new migration
```
uv run alembic revision --autogenerate -m "<message here>"
```

**Step 2:** For updating new schema changes on database server
```
uv run alembic upgrade head
```