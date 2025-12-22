# Insurance Quote Conversational Agent

A conversational AI chatbot that helps users get insurance quotes through natural language interaction. Built with FastAPI, LangChain, Redis, and Next.js.

## Features

- Natural language understanding (e.g., "I want full insurance for my car")
- LangChain agent with tool-calling capabilities
- Redis-backed conversation memory
- Mock API integration (Phase 1) → Real API integration (Phase 2)
- Modern React chat UI with streaming support (Phase 3)

## Architecture

- **Backend**: FastAPI with LangChain agent and Redis memory
- **Frontend**: Next.js App Router with React components
- **State**: Redis for session-based conversation history
- **LLM**: OpenAI (GPT-4) initially, switchable to Ollama

## Project Structure

```
.
├── backend/           # FastAPI backend
│   ├── api/          # API routes
│   ├── agent/        # LangChain agent and tools
│   ├── memory/       # Redis memory management
│   ├── schemas/      # Pydantic models
│   ├── services/     # External API clients (Phase 2)
│   └── main.py       # FastAPI app entry point
├── frontend/         # Next.js frontend
│   ├── app/          # Next.js app router
│   └── components/   # React components
├── infra/            # Infrastructure configs
│   └── docker-compose.yml
└── README.md
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (for Redis)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and fill in your values:
```bash
cp ../.env.example ../.env
# Edit .env with your OPENAI_API_KEY
```

5. Start Redis (from project root):
```bash
docker-compose -f infra/docker-compose.yml up -d
```

6. Run the backend:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set environment variable (or add to `.env.local`):
```bash
export NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

4. Run the frontend:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Quick Start

### Option 1: Using Helper Scripts (Recommended)

1. **Start Redis:**
   ```bash
   ./scripts/start-redis.sh
   ```

2. **Start Backend** (in a new terminal):
   ```bash
   ./scripts/start-backend.sh
   ```
   Make sure to add your `OPENAI_API_KEY` to the `.env` file first!

3. **Start Frontend** (in another terminal):
   ```bash
   ./scripts/start-frontend.sh
   ```

4. **Open browser** to `http://localhost:3000` and start chatting!

### Option 2: Manual Setup

1. **Start Redis:**
   ```bash
   docker-compose -f infra/docker-compose.yml up -d
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   # Create .env file with OPENAI_API_KEY
   uvicorn main:app --reload --port 8000
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Open browser** to `http://localhost:3000`

## Usage

Try asking:
- "I want full insurance for my car"
- "Get me a quote for a 2023 Toyota Camry"
- "What's the cheapest quote you can find?"

## Development Phases

- **Phase 1**: Core chat with mock tools (✅ Current)
- **Phase 2**: Connect real APIs (`/vehicle`, `/getQuote`)
- **Phase 3**: Add SSE streaming and enhanced UI
- **Phase 4**: Deploy to cloud
- **Phase 5**: Add enhancements (RAG, analytics, etc.)

## Environment Variables

See `.env.example` for all required variables.

Key variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `REDIS_URL`: Redis connection URL (default: `redis://localhost:6379/0`)
- `MODEL_PROVIDER`: `openai` or `ollama` (default: `openai`)
- `NEXT_PUBLIC_BACKEND_URL`: Backend URL for frontend (default: `http://localhost:8000`)

## License

MIT

