# MemoCloud

A full-stack cloud-based notes application built with modern technologies.

## Tech Stack

### Backend

* Python
* FastAPI
* SQLModel
* PostgreSQL
* JWT Authentication
* Docker
* Redis

### Frontend

* Next.js
* TypeScript
* Tailwind CSS
* Axios

---

# Project Structure

```txt
MemoCloud/
│
├── backend/
    ├── alembic/
│   ├── core/
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── main.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env
│   └── README.md
│
└── frontend/
    ├── src/
    ├── public/
    ├── package.json
    ├── .env.local
    └── README.md
```

---

# Features

## Authentication

* User Registration
* User Login
* JWT Access Tokens
* Protected Routes
* Secure Password Hashing

## Notes Management

* Create Notes
* Update Notes
* Delete Notes
* Archive Notes
* Search Notes
* Markdown Support

## Infrastructure

* Dockerized Backend
* PostgreSQL Database
* Redis Integration
* Environment-based Configuration

---

# Backend Setup

## 1. Navigate To Backend

```bash
cd backend
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create `.env`

```env
DATABASE_URL=postgresql://postgres:password@postgres:5432/notes_app
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REDIS_URL=redis://redis:6379
```

---

## 5. Run Backend Locally

```bash
uvicorn main:app --reload
```

Backend:

```txt
http://localhost:8000
```

Swagger Docs:

```txt
http://localhost:8000/docs
```

---

# Docker Setup

## Start Services

```bash
docker compose up --build
```

This starts:

* FastAPI Backend
* PostgreSQL
* Redis

---

## Stop Services

```bash
docker compose down
```

---

## Remove Containers + Volumes

```bash
docker compose down -v
```

---

# Frontend Setup

## 1. Navigate To Frontend

```bash
cd frontend
```

---

## 2. Install Dependencies

```bash
npm install
```

---

## 3. Create `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 4. Run Frontend

```bash
npm run dev
```

Frontend:

```txt
http://localhost:3000
```

---

# Frontend Architecture

```txt
frontend/
│
├── src/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── services/
│   ├── hooks/
│   ├── store/
│   ├── types/
│   └── utils/
│
├── public/
├── package.json
└── .env.local
```

---

# API Endpoints

## Authentication

| Method | Endpoint       | Description   |
| ------ | -------------- | ------------- |
| POST   | /auth/register | Register user |
| POST   | /auth/login    | Login user    |
| GET    | /auth/me       | Current user  |

---

## Notes

| Method | Endpoint    | Description     |
| ------ | ----------- | --------------- |
| GET    | /notes      | Get all notes   |
| POST   | /notes      | Create note     |
| GET    | /notes/{id} | Get single note |
| PUT    | /notes/{id} | Update note     |
| DELETE | /notes/{id} | Delete note     |

---

# Recommended Backend Dependencies

```txt
fastapi
uvicorn
sqlmodel
psycopg2-binary
python-dotenv
python-jose
passlib[bcrypt]
alembic
redis
```

---

# Recommended Frontend Dependencies

```txt
next
react
react-dom
typescript
axios
tailwindcss
react-query
zustand
```

---

# Git Workflow

## Create Branch

```bash
git checkout -b feature/auth
```

---

## Commit Changes

```bash
git add .
git commit -m "Added authentication"
```

---

## Push Changes

```bash
git push origin feature/auth
```

---

# Future Improvements

* Refresh Tokens
* Email Verification
* Password Reset
* Rich Text Editor
* Real-time Collaboration
* WebSockets
* File Uploads
* AI Summarization
* Note Sharing
* Folder Organization
* Tags & Filters
* Rate Limiting
* CI/CD Pipeline
* Kubernetes Deployment

---

# Deployment Suggestions

## Backend

* Render
* Railway
* AWS EC2
* DigitalOcean

## Frontend

* Vercel
* Netlify

## Database

* Neon PostgreSQL
* Supabase
* Railway PostgreSQL

---

# Development Notes

* Use Docker for consistent local development.
* Never commit `.env` files.
* Use Alembic for database migrations.
* Keep business logic inside services.
* Keep routes thin and clean.
* Use environment variables for all secrets.

---

# License

MIT License

---

# Author

Built with FastAPI, Next.js, and Docker.
