# Local Skill-Sharing Event Platform

A full-stack skeleton for a community learning management platform built with a Next.js 14 frontend styled with Mantine and a FastAPI backend backed by PostgreSQL.

## Features

- Email/password authentication with JWT tokens issued by FastAPI
- Participant dashboard for tracking upcoming events and feedback
- Organizer event management tools with resource upload stubs
- Admin panel to review platform users and events
- Docker Compose setup for the frontend, backend, and PostgreSQL
- Unit tests for backend authentication flows and React tests for protected routing behaviour

## Project structure

```
backend/    # FastAPI application
frontend/   # Next.js 14 application
```

## Requirements

- Docker and Docker Compose (recommended for full stack run)
- Alternatively, Python 3.11+ and Node.js 18+ for running services locally

## Environment variables

Copy the backend example env file and adjust secrets as needed:

```
cp backend/.env.example backend/.env
```

`backend/.env` must define:

- `SECRET_KEY` – JWT signing key
- `DATABASE_URL` – SQLAlchemy connection string (PostgreSQL in production, SQLite allowed for local tests)

The frontend reads `NEXT_PUBLIC_API_URL` to know where the API is running (defaults to `http://localhost:8000`).

## Running with Docker Compose

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs for interactive API docs
- Database: PostgreSQL on `localhost:5432`

## Running locally without Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Ensure PostgreSQL is running and `DATABASE_URL` is set (or use SQLite for quick experiments).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000.

## Tests

### Backend tests

```bash
cd backend
pytest
```

### Frontend tests

```bash
cd frontend
npm test
```

## API overview

Key REST endpoints exposed by FastAPI:

- `POST /auth/register` – Create an account
- `POST /auth/token` – Obtain a JWT for subsequent requests
- `CRUD /events` – Manage events and resources (organizers)
- `POST /events/{id}/enroll` – Track attendance
- `POST /events/{id}/feedback` – Submit feedback after events
- `GET /admin/users` & `GET /admin/events` – Admin reporting endpoints

This skeleton is ready to extend with richer validation, file storage, calendar integrations, and production hardening.
