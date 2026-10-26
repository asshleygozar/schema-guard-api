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
Set `FRONTEND_ORIGIN` to the exact origin of the client application (for example,
`http://localhost:3000`). Credentialed browser requests are restricted to this
origin; configure the deployed client origin in production.
Set `API_ORIGIN` to the public origin of this FastAPI server (for example,
`http://localhost:8000`). The server builds the GitHub callback URL as
`<API_ORIGIN>/api/v1/auth/github/callback`; register that exact URL in the
GitHub OAuth app. GitHub login and callback traffic go directly to FastAPI.
The API issues an HttpOnly session cookie, and the client validates it through
the authenticated API endpoint.

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