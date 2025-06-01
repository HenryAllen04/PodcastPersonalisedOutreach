# 🛳️ PODVOX Containerisation Guide

Run the FastAPI backend and the Vite + React frontend locally or in the cloud with **Docker Compose** — no object-storage service required.

---

## 📦 Project Layout

```
podvox/
├─ backend/
│  ├─ app/           # FastAPI code
│  ├─ Dockerfile
│  └─ requirements.txt
├─ frontend/
│  ├─ src/           # React + Vite
│  ├─ Dockerfile
│  └─ package.json
└─ docker-compose.yml
```

---

## ⚡ Quick Start

```bash
# From repo root
docker compose up --build

# Access:
#  • http://localhost:3000        → React UI
#  • http://localhost:8000/docs   → FastAPI Swagger
```

---

## 🔧 Development

### Backend Only
```bash
cd backend
docker build -t podvox-backend .
docker run -p 8000:8000 podvox-backend
```

### Frontend Only
```bash
cd frontend
docker build -t podvox-frontend .
docker run -p 3000:3000 podvox-frontend
```

### Hot Reload Development
```bash
# The docker-compose.yml includes volume mounts for hot reloading
docker compose up --build
# Edit files in backend/ or frontend/ and see changes live!
```

---

## 🌍 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

---

## 📝 Notes

• API keys supplied via `.env` or your hosting provider's env settings.
• No object storage included; backend should stream or return audio directly.
• For production, consider a multi-stage Poetry build or gunicorn-uvicorn worker model.
• The frontend includes a backend connectivity check button for testing.

---

## 🚀 Next Steps

1. Test the setup: `docker compose up --build`
2. Visit the frontend at http://localhost:3000
3. Check backend API docs at http://localhost:8000/docs
4. Use the "Check Backend Connection" button to verify connectivity
5. Start building your PODVOX features! 