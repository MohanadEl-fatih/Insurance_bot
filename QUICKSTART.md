# Quick Start Guide

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed  
- [ ] Docker installed and running
- [ ] OpenAI API key (get one at https://platform.openai.com/api-keys)

## Step-by-Step Setup

### 1. Create Environment File

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

### 2. Start Redis

```bash
./scripts/start-redis.sh
```

Or manually:
```bash
docker-compose -f infra/docker-compose.yml up -d
```

Verify Redis is running:
```bash
docker ps | grep redis
```

### 3. Start Backend

In a new terminal:
```bash
./scripts/start-backend.sh
```

Wait for: `Application startup complete` and `Uvicorn running on http://127.0.0.1:8000`

### 4. Start Frontend

In another terminal:
```bash
./scripts/start-frontend.sh
```

Wait for: `Ready on http://localhost:3000`

### 5. Test the Chat

1. Open http://localhost:3000 in your browser
2. Try: "I want full insurance for my car"
3. The agent will ask follow-up questions if needed
4. It will use mock tools to generate quotes

## Troubleshooting

### Backend won't start
- Check Redis is running: `docker ps`
- Verify `.env` file exists and has `OPENAI_API_KEY`
- Check port 8000 is not in use: `lsof -i :8000`

### Frontend won't connect to backend
- Verify backend is running on http://localhost:8000
- Check `NEXT_PUBLIC_BACKEND_URL` in `.env` (defaults to http://localhost:8000)
- Check browser console for CORS errors

### Agent not responding
- Check backend logs for errors
- Verify OpenAI API key is valid
- Check Redis connection in backend logs

## Next Steps

- **Phase 2**: Replace mock tools with real API clients
- **Phase 3**: Add streaming responses
- **Phase 4**: Deploy to cloud
- **Phase 5**: Add enhancements (RAG, analytics, etc.)

phase 1:
User Input
    ↓
[Frontend UI] ChatWindow.tsx
    ↓ POST /api/chat
[Frontend API] route.ts (Next.js API Route)
    ↓ Proxy to backend
[Backend API] chat.py (FastAPI Router)
    ↓
[Service Layer] chat_service.py
    ↓
[Agent Layer] agent_factory.py → AgentExecutor
    ↓ (may use)
[Tools Layer] tools.py → VehicleService/QuoteService
    ↓ (uses)
[Memory Layer] redis.py → Redis
    ↓
Response flows back up