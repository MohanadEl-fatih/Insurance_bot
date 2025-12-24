# Insurance Bot - Complete Call Trace

## Detailed Request Path with Function Calls

This document provides a complete trace of every function/method call from user input to response, including file paths, line numbers, parameters, and return values.

---

## Example Request: "I need insurance for my 2020 Toyota Camry"

---

## LAYER 1: FRONTEND UI (React Component)

### Call 1: User Event Handler
**Trigger**: User clicks Send button or presses Enter

**File**: `frontend/components/ChatWindow.tsx:27`
```typescript
const handleSendMessage = async (content: string) => { ... }
```

**Parameters**:
- `content`: `"I need insurance for my 2020 Toyota Camry"`

**Internal Operations**:

#### Call 1.1: Validation Check
**Line**: `frontend/components/ChatWindow.tsx:28`
```typescript
if (!content.trim() || isLoading) return
```

#### Call 1.2: Create User Message Object
**Line**: `frontend/components/ChatWindow.tsx:31-36`
```typescript
const userMessage: Message = {
  id: Date.now().toString(),
  role: 'user',
  content: content.trim(),
  timestamp: new Date(),
}
```

**Result**:
```javascript
{
  id: "1703456789000",
  role: "user",
  content: "I need insurance for my 2020 Toyota Camry",
  timestamp: Date(2024-12-24T10:30:00.000Z)
}
```

#### Call 1.3: Update UI State
**Line**: `frontend/components/ChatWindow.tsx:37-38`
```typescript
setMessages((prev) => [...prev, userMessage])
setIsLoading(true)
```

**State Change**:
- `messages`: Array with new user message added
- `isLoading`: `false` → `true`

---

## LAYER 2: FRONTEND API CALL

### Call 2: HTTP POST to Next.js Proxy
**Line**: `frontend/components/ChatWindow.tsx:41-48`

```typescript
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ message: content.trim() }),
  credentials: 'include',
})
```

**HTTP Request**:
```
POST http://localhost:3000/api/chat
Content-Type: application/json
Cookie: sid=550e8400-e29b-41d4-a716-446655440000 (if exists)

Body:
{
  "message": "I need insurance for my 2020 Toyota Camry"
}
```

**Execution**: Async fetch request sent to Next.js server

---

## LAYER 3: NEXT.JS API ROUTE (Proxy)

### Call 3: Next.js Route Handler
**File**: `frontend/app/api/chat/route.ts:5`

```typescript
export async function POST(request: NextRequest) { ... }
```

**Parameters**:
- `request`: NextRequest object containing body and headers

**Internal Operations**:

#### Call 3.1: Parse Request Body
**Line**: `frontend/app/api/chat/route.ts:7-8`
```typescript
const body = await request.json()
const { message } = body
```

**Result**:
- `body`: `{ message: "I need insurance for my 2020 Toyota Camry" }`
- `message`: `"I need insurance for my 2020 Toyota Camry"`

#### Call 3.2: Validate Message
**Line**: `frontend/app/api/chat/route.ts:10-15`
```typescript
if (!message || typeof message !== 'string') {
  return NextResponse.json(
    { error: 'Message is required' },
    { status: 400 }
  )
}
```

**Result**: Validation passes, continues execution

#### Call 3.3: Extract Session Cookie
**Line**: `frontend/app/api/chat/route.ts:18`
```typescript
const sid = request.cookies.get('sid')?.value
```

**Result**:
- `sid`: `"550e8400-e29b-41d4-a716-446655440000"` (if exists) or `undefined` (new session)

#### Call 3.4: Forward to Backend
**Line**: `frontend/app/api/chat/route.ts:21-29`

```typescript
const response = await fetch(`${BACKEND_URL}/chat`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    ...(sid && { Cookie: `sid=${sid}` }),
  },
  credentials: 'include',
  body: JSON.stringify({ message, sid }),
})
```

**HTTP Request**:
```
POST http://localhost:8000/chat
Content-Type: application/json
Cookie: sid=550e8400-e29b-41d4-a716-446655440000 (if exists)

Body:
{
  "message": "I need insurance for my 2020 Toyota Camry",
  "sid": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## LAYER 4: BACKEND API (FastAPI)

### Call 4: FastAPI Route Handler
**File**: `backend/api/chat.py:14`

```python
@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    response: Response,
    sid: str = Cookie(None)
):
```

**Parameters**:
- `request`: `ChatRequest(message="I need insurance for my 2020 Toyota Camry", sid="550e...")`
- `response`: FastAPI Response object
- `sid`: `"550e8400-e29b-41d4-a716-446655440000"` or `None`

**Internal Operations**:

#### Call 4.1: Generate or Use Session ID
**Line**: `backend/api/chat.py:25`
```python
session_id = sid or str(uuid.uuid4())
```

**Result**:
- If `sid` exists: `session_id = "550e8400-e29b-41d4-a716-446655440000"`
- If new session: `session_id = "a1b2c3d4-e5f6-4789-a012-3456789abcde"`

#### Call 4.2: Set Session Cookie (if new)
**Line**: `backend/api/chat.py:28-35`
```python
if not sid:
    response.set_cookie(
        key="sid",
        value=session_id,
        httponly=True,
        samesite="lax",
        max_age=86400,
    )
```

**Result**: Cookie header prepared for response (if new session)

#### Call 4.3: Process Message via ChatService
**Line**: `backend/api/chat.py:39`

```python
reply = await ChatService.process_message(session_id, request.message)
```

**Parameters Passed**:
- `session_id`: `"550e8400-e29b-41d4-a716-446655440000"`
- `message`: `"I need insurance for my 2020 Toyota Camry"`

**Execution**: Async call to ChatService

---

## LAYER 5: CHAT SERVICE

### Call 5: Chat Service Process Message
**File**: `backend/services/chat_service.py:14`

```python
@staticmethod
async def process_message(session_id: str, message: str) -> str:
```

**Parameters**:
- `session_id`: `"550e8400-e29b-41d4-a716-446655440000"`
- `message`: `"I need insurance for my 2020 Toyota Camry"`

**Internal Operations**:

#### Call 5.1: Get Redis Memory
**Line**: `backend/services/chat_service.py:27`

```python
memory = get_memory(session_id, settings.redis_url)
```

**Delegates to**: `backend/memory/redis.py:9`

```python
def get_memory(session_id: str, redis_url: str) -> RedisChatMessageHistory:
```

**Parameters**:
- `session_id`: `"550e8400-e29b-41d4-a716-446655440000"`
- `redis_url`: `"redis://localhost:6379/0"`

**Line**: `backend/memory/redis.py:21-26`
```python
memory = RedisChatMessageHistory(
    session_id=f"session:{session_id}",
    url=redis_url,
    ttl=3600 * 24,  # 24 hours TTL
)
return memory
```

**Redis Key Created**: `"session:550e8400-e29b-41d4-a716-446655440000"`

**Returns**: `RedisChatMessageHistory` instance

**Back to ChatService**, `memory` now contains LangChain memory object

---

#### Call 5.2: Create Agent Executor
**Line**: `backend/services/chat_service.py:30`

```python
agent_executor = create_agent_executor(session_id)
```

**Delegates to**: `backend/agent/agent_factory.py:36`

```python
def create_agent_executor(session_id: str) -> AgentExecutor:
```

**Parameters**:
- `session_id`: `"550e8400-e29b-41d4-a716-446655440000"`

**Sub-operations**:

##### Call 5.2.1: Get LLM Instance
**Line**: `backend/agent/agent_factory.py:49`
```python
llm = get_llm()
```

**Delegates to**: `backend/agent/llm.py` (reads configuration)

**Returns**: `ChatOpenAI` instance configured with:
```python
ChatOpenAI(
    base_url="http://localhost:1234/v1",
    model="local-model",
    temperature=0.7,
    api_key="not-needed"  # For LM Studio
)
```

##### Call 5.2.2: Get Tools List
**Line**: `backend/agent/agent_factory.py:50`
```python
tools = get_tools()
```

**Delegates to**: `backend/agent/tools.py:59`

```python
def get_tools():
    return [mock_vehicle_lookup, mock_get_quote]
```

**Returns**: List of 2 LangChain tool objects:
```python
[
    <Tool: mock_vehicle_lookup>,
    <Tool: mock_get_quote>
]
```

##### Call 5.2.3: Create Prompt Template
**Line**: `backend/agent/agent_factory.py:53-58`
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
```

**Returns**: ChatPromptTemplate with 4 message placeholders

##### Call 5.2.4: Create Agent
**Line**: `backend/agent/agent_factory.py:61`
```python
agent = create_openai_tools_agent(llm, tools, prompt)
```

**Returns**: Runnable agent that processes messages

##### Call 5.2.5: Create Agent Executor
**Line**: `backend/agent/agent_factory.py:64-69`
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)
```

**Returns**: AgentExecutor instance

**Back to ChatService**, `agent_executor` now ready

---

#### Call 5.3: Retrieve Chat History
**Line**: `backend/services/chat_service.py:33`

```python
chat_history = memory.messages
```

**Redis Operation**: `GET session:550e8400-e29b-41d4-a716-446655440000`

**Returns**: List of previous messages (if any):
```python
[
    HumanMessage(content="Hello"),
    AIMessage(content="Hi! I'm your insurance assistant. How can I help you today?"),
]
```

Or empty list `[]` for new sessions

---

#### Call 5.4: Invoke Agent
**Line**: `backend/services/chat_service.py:36-39`

```python
result = await agent_executor.ainvoke({
    "input": message,
    "chat_history": chat_history,
})
```

**Parameters**:
```python
{
    "input": "I need insurance for my 2020 Toyota Camry",
    "chat_history": [
        HumanMessage(content="Hello"),
        AIMessage(content="Hi! I'm your insurance assistant..."),
    ]
}
```

**Execution**: Triggers LangChain agent execution chain

---

## LAYER 6: AGENT EXECUTION (LangChain)

### Call 6: Agent Executor Invoke
**Component**: LangChain AgentExecutor

**Internal LangChain Operations** (simplified):

#### Call 6.1: Format Prompt
**Action**: Combine system prompt, chat history, and user input

**Formatted Messages**:
```python
[
    SystemMessage(content="You are a helpful insurance quote assistant..."),
    HumanMessage(content="Hello"),
    AIMessage(content="Hi! I'm your insurance assistant..."),
    HumanMessage(content="I need insurance for my 2020 Toyota Camry"),
]
```

#### Call 6.2: Initial LLM Call
**Action**: LangChain calls LLM via HTTP

**HTTP Request**:
```
POST http://localhost:1234/v1/chat/completions
Content-Type: application/json

Body:
{
  "model": "local-model",
  "messages": [
    {"role": "system", "content": "You are a helpful insurance quote assistant..."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! I'm your insurance assistant..."},
    {"role": "user", "content": "I need insurance for my 2020 Toyota Camry"}
  ],
  "temperature": 0.7,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "mock_vehicle_lookup",
        "description": "Look up vehicle information...",
        "parameters": {
          "type": "object",
          "properties": {
            "vin": {"type": "string", "description": "Vehicle Identification Number"},
            "make": {"type": "string", "description": "Vehicle make"},
            "model": {"type": "string", "description": "Vehicle model"},
            "year": {"type": "integer", "description": "Vehicle year"}
          }
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "mock_get_quote",
        "description": "Get insurance quotes for a vehicle...",
        "parameters": {
          "type": "object",
          "properties": {
            "vehicle_make": {"type": "string"},
            "vehicle_model": {"type": "string"},
            "vehicle_year": {"type": "integer"},
            "coverage_type": {"type": "string", "enum": ["liability", "comprehensive", "full"]}
          },
          "required": ["vehicle_make", "vehicle_model", "vehicle_year"]
        }
      }
    }
  ]
}
```

**LLM Response** (decides to call vehicle lookup tool):
```json
{
  "id": "chatcmpl-abc123",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": null,
      "tool_calls": [{
        "id": "call_xyz789",
        "type": "function",
        "function": {
          "name": "mock_vehicle_lookup",
          "arguments": "{\"make\": \"Toyota\", \"model\": \"Camry\", \"year\": 2020}"
        }
      }]
    }
  }]
}
```

---

## LAYER 7: TOOL EXECUTION - Vehicle Lookup

### Call 7: Execute Vehicle Lookup Tool
**File**: `backend/agent/tools.py:12`

```python
@tool
def mock_vehicle_lookup(vin: str = None, make: str = None, model: str = None, year: int = None) -> dict:
```

**Called by**: LangChain agent executor

**Parameters**:
- `vin`: `None`
- `make`: `"Toyota"`
- `model`: `"Camry"`
- `year`: `2020`

**Line**: `backend/agent/tools.py:25`
```python
logger.info(f"Vehicle lookup tool called: vin={vin}, make={make}, model={model}, year={year}")
```

**Console Output**:
```
INFO: Vehicle lookup tool called: vin=None, make=Toyota, model=Camry, year=2020
```

#### Call 7.1: Delegate to Vehicle Service
**Line**: `backend/agent/tools.py:28`

```python
return VehicleService.lookup_vehicle(vin=vin, make=make, model=model, year=year)
```

**Delegates to**: `backend/services/vehicle_service.py:13`

```python
@staticmethod
def lookup_vehicle(
    vin: Optional[str] = None,
    make: Optional[str] = None,
    model: Optional[str] = None,
    year: Optional[int] = None
) -> dict:
```

**Parameters**:
- `vin`: `None`
- `make`: `"Toyota"`
- `model`: `"Camry"`
- `year`: `2020`

**Line**: `backend/services/vehicle_service.py:31`
```python
logger.info(f"Vehicle lookup: vin={vin}, make={make}, model={model}, year={year}")
```

**Console Output**:
```
INFO: Vehicle lookup: vin=None, make=Toyota, model=Camry, year=2020
```

**Line**: `backend/services/vehicle_service.py:44-51` (make, model, year all provided)
```python
if make and model and year:
    return {
        "vin": f"MOCK{year}{make[:3].upper()}{model[:3].upper()}",
        "make": make,
        "model": model,
        "year": year,
        "status": "found"
    }
```

**Returns**:
```python
{
    "vin": "MOCK2020TOYCAM",
    "make": "Toyota",
    "model": "Camry",
    "year": 2020,
    "status": "found"
}
```

**Back to tool**, this dict is returned to agent

---

## LAYER 8: AGENT EXECUTION - Process Tool Result

### Call 8: Agent Processes Vehicle Data
**Component**: LangChain AgentExecutor

**Action**: Add tool result to agent scratchpad

**Agent Scratchpad**:
```python
AIMessage(content="", tool_calls=[{
    "id": "call_xyz789",
    "function": {
        "name": "mock_vehicle_lookup",
        "arguments": '{"make": "Toyota", "model": "Camry", "year": 2020}'
    }
}])

ToolMessage(
    content='{"vin": "MOCK2020TOYCAM", "make": "Toyota", "model": "Camry", "year": 2020, "status": "found"}',
    tool_call_id="call_xyz789"
)
```

#### Call 8.1: Second LLM Call with Tool Results
**HTTP Request**:
```
POST http://localhost:1234/v1/chat/completions

Body:
{
  "model": "local-model",
  "messages": [
    {"role": "system", "content": "You are a helpful insurance quote assistant..."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! I'm your insurance assistant..."},
    {"role": "user", "content": "I need insurance for my 2020 Toyota Camry"},
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [{
        "id": "call_xyz789",
        "function": {
          "name": "mock_vehicle_lookup",
          "arguments": "{\"make\": \"Toyota\", \"model\": \"Camry\", \"year\": 2020}"
        }
      }]
    },
    {
      "role": "tool",
      "tool_call_id": "call_xyz789",
      "content": "{\"vin\": \"MOCK2020TOYCAM\", \"make\": \"Toyota\", \"model\": \"Camry\", \"year\": 2020, \"status\": \"found\"}"
    }
  ],
  "tools": [...]
}
```

**LLM Response** (decides to get quote):
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": null,
      "tool_calls": [{
        "id": "call_abc456",
        "type": "function",
        "function": {
          "name": "mock_get_quote",
          "arguments": "{\"vehicle_make\": \"Toyota\", \"vehicle_model\": \"Camry\", \"vehicle_year\": 2020, \"coverage_type\": \"full\"}"
        }
      }]
    }
  }]
}
```

---

## LAYER 9: TOOL EXECUTION - Get Quote

### Call 9: Execute Get Quote Tool
**File**: `backend/agent/tools.py:32`

```python
@tool
def mock_get_quote(vehicle_make: str, vehicle_model: str, vehicle_year: int, coverage_type: str = "full") -> List[dict]:
```

**Called by**: LangChain agent executor

**Parameters**:
- `vehicle_make`: `"Toyota"`
- `vehicle_model`: `"Camry"`
- `vehicle_year`: `2020`
- `coverage_type`: `"full"`

**Line**: `backend/agent/tools.py:45-48`
```python
logger.info(
    f"Get quote tool called: {vehicle_make} {vehicle_model} {vehicle_year}, "
    f"coverage={coverage_type}"
)
```

**Console Output**:
```
INFO: Get quote tool called: Toyota Camry 2020, coverage=full
```

#### Call 9.1: Delegate to Quote Service
**Line**: `backend/agent/tools.py:51-56`

```python
return QuoteService.get_quotes(
    vehicle_make=vehicle_make,
    vehicle_model=vehicle_model,
    vehicle_year=vehicle_year,
    coverage_type=coverage_type
)
```

**Delegates to**: `backend/services/quote_service.py:13`

```python
@staticmethod
def get_quotes(
    vehicle_make: str,
    vehicle_model: str,
    vehicle_year: int,
    coverage_type: str = "full"
) -> List[dict]:
```

**Parameters**:
- `vehicle_make`: `"Toyota"`
- `vehicle_model`: `"Camry"`
- `vehicle_year`: `2020`
- `coverage_type`: `"full"`

**Line**: `backend/services/quote_service.py:31-34`
```python
logger.info(
    f"Get quotes: {vehicle_make} {vehicle_model} {vehicle_year}, "
    f"coverage={coverage_type}"
)
```

**Console Output**:
```
INFO: Get quotes: Toyota Camry 2020, coverage=full
```

**Line**: `backend/services/quote_service.py:37-41` (get base premium)
```python
base_premiums = {
    "liability": 50.0,
    "comprehensive": 120.0,
    "full": 180.0
}

base_premium = base_premiums.get(coverage_type.lower(), 180.0)
```

**Result**: `base_premium = 180.0`

**Line**: `backend/services/quote_service.py:46-81` (generate quotes)
```python
quotes = [
    {
        "provider": "SafeDrive Insurance",
        "premium_monthly": round(base_premium * 0.9, 2),  # 162.0
        "coverage": coverage_type.lower(),
        "details": {
            "deductible": 500,
            "policy_limit": 100000,
            "special_features": ["Roadside assistance", "Rental car coverage"]
        }
    },
    {
        "provider": "BudgetCover Insurance",
        "premium_monthly": round(base_premium * 0.85, 2),  # 153.0
        "coverage": coverage_type.lower(),
        "details": {
            "deductible": 1000,
            "policy_limit": 50000,
            "special_features": ["Basic coverage"]
        }
    },
    {
        "provider": "PremiumGuard Insurance",
        "premium_monthly": round(base_premium * 1.1, 2),  # 198.0
        "coverage": coverage_type.lower(),
        "details": {
            "deductible": 250,
            "policy_limit": 250000,
            "special_features": [
                "24/7 support",
                "Accident forgiveness",
                "New car replacement"
            ]
        }
    }
]
```

**Line**: `backend/services/quote_service.py:83`
```python
return quotes
```

**Returns**: List of 3 quote dictionaries

**Back to tool**, this list is returned to agent

---

## LAYER 10: AGENT EXECUTION - Final Response

### Call 10: Agent Processes Quote Data
**Component**: LangChain AgentExecutor

**Action**: Add second tool result to scratchpad

**Updated Scratchpad**:
```python
ToolMessage(
    content='[{"provider": "SafeDrive Insurance", "premium_monthly": 162.0, ...}, ...]',
    tool_call_id="call_abc456"
)
```

#### Call 10.1: Third LLM Call for Final Response
**HTTP Request**:
```
POST http://localhost:1234/v1/chat/completions

Body:
{
  "model": "local-model",
  "messages": [
    // ... all previous messages ...
    {
      "role": "tool",
      "tool_call_id": "call_abc456",
      "content": "[{\"provider\": \"SafeDrive Insurance\", \"premium_monthly\": 162.0, ...}, ...]"
    }
  ],
  "tools": [...]
}
```

**LLM Response** (final natural language response):
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Great! I found some insurance quotes for your 2020 Toyota Camry. Here are your options:\n\n**1. BudgetCover Insurance - $153.00/month** (Best Price!)\n   - Coverage: Full\n   - Deductible: $1,000\n   - Policy Limit: $50,000\n   - Features: Basic coverage\n\n**2. SafeDrive Insurance - $162.00/month**\n   - Coverage: Full\n   - Deductible: $500\n   - Policy Limit: $100,000\n   - Features: Roadside assistance, Rental car coverage\n\n**3. PremiumGuard Insurance - $198.00/month**\n   - Coverage: Full\n   - Deductible: $250\n   - Policy Limit: $250,000\n   - Features: 24/7 support, Accident forgiveness, New car replacement\n\nI recommend the BudgetCover option if you're looking for the most affordable rate, but SafeDrive offers better coverage at a slightly higher price. Would you like more details about any of these options?"
    }
  }]
}
```

#### Call 10.2: Agent Returns Result
**Returns to ChatService**:
```python
{
    "input": "I need insurance for my 2020 Toyota Camry",
    "chat_history": [...],
    "output": "Great! I found some insurance quotes for your 2020 Toyota Camry..."
}
```

---

## LAYER 11: MEMORY PERSISTENCE

### Call 11: Save to Redis
**Back in**: `backend/services/chat_service.py`

#### Call 11.1: Extract Response
**Line**: `backend/services/chat_service.py:41-44`
```python
response = result.get(
    "output",
    "I apologize, but I couldn't generate a response."
)
```

**Result**: `response = "Great! I found some insurance quotes..."`

#### Call 11.2: Save User Message
**Line**: `backend/services/chat_service.py:47`

```python
memory.add_user_message(message)
```

**Delegates to**: LangChain's `RedisChatMessageHistory.add_user_message()`

**Redis Operation**:
```
RPUSH session:550e8400-e29b-41d4-a716-446655440000 <serialized HumanMessage>
EXPIRE session:550e8400-e29b-41d4-a716-446655440000 86400
```

**Stored Data**:
```python
HumanMessage(content="I need insurance for my 2020 Toyota Camry")
```

#### Call 11.3: Save AI Message
**Line**: `backend/services/chat_service.py:48`

```python
memory.add_ai_message(response)
```

**Delegates to**: LangChain's `RedisChatMessageHistory.add_ai_message()`

**Redis Operation**:
```
RPUSH session:550e8400-e29b-41d4-a716-446655440000 <serialized AIMessage>
EXPIRE session:550e8400-e29b-41d4-a716-446655440000 86400
```

**Stored Data**:
```python
AIMessage(content="Great! I found some insurance quotes...")
```

#### Call 11.4: Return Response
**Line**: `backend/services/chat_service.py:50`

```python
return response
```

**Returns**: `"Great! I found some insurance quotes..."`

---

## LAYER 12: BACKEND API RESPONSE

### Call 12: Build Response
**Back in**: `backend/api/chat.py`

**Line**: `backend/api/chat.py:39` (awaited, now complete)
```python
reply = "Great! I found some insurance quotes..."
```

**Line**: `backend/api/chat.py:41-44`
```python
return ChatResponse(
    message=reply,
    meta={"session_id": session_id}
)
```

**Response Object**:
```python
ChatResponse(
    message="Great! I found some insurance quotes...",
    meta={"session_id": "550e8400-e29b-41d4-a716-446655440000"}
)
```

**FastAPI Serializes to JSON**:
```json
{
  "message": "Great! I found some insurance quotes...",
  "meta": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**HTTP Response**:
```
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: sid=550e8400-e29b-41d4-a716-446655440000; HttpOnly; SameSite=lax; Max-Age=86400; Path=/

{
  "message": "Great! I found some insurance quotes...",
  "meta": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

---

## LAYER 13: NEXT.JS PROXY RESPONSE

### Call 13: Forward Response
**Back in**: `frontend/app/api/chat/route.ts`

**Line**: `frontend/app/api/chat/route.ts:21-29` (awaited, now complete)

**Line**: `frontend/app/api/chat/route.ts:36`
```typescript
const data = await response.json()
```

**Result**:
```javascript
{
  message: "Great! I found some insurance quotes...",
  meta: {
    session_id: "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Line**: `frontend/app/api/chat/route.ts:39`
```typescript
const nextResponse = NextResponse.json(data)
```

**Line**: `frontend/app/api/chat/route.ts:42-45`
```typescript
const setCookieHeader = response.headers.get('set-cookie')
if (setCookieHeader) {
  nextResponse.headers.set('set-cookie', setCookieHeader)
}
```

**Line**: `frontend/app/api/chat/route.ts:47`
```typescript
return nextResponse
```

**HTTP Response to Browser**:
```
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: sid=550e8400-e29b-41d4-a716-446655440000; HttpOnly; SameSite=lax; Max-Age=86400; Path=/

{
  "message": "Great! I found some insurance quotes...",
  "meta": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

---

## LAYER 14: FRONTEND UI UPDATE

### Call 14: Process Response
**Back in**: `frontend/components/ChatWindow.tsx`

**Line**: `frontend/components/ChatWindow.tsx:41-48` (awaited, now complete)

#### Call 14.1: Check Response Status
**Line**: `frontend/components/ChatWindow.tsx:50-52`
```typescript
if (!response.ok) {
  throw new Error(`HTTP error! status: ${response.status}`)
}
```

**Result**: Status 200, continues

#### Call 14.2: Parse JSON
**Line**: `frontend/components/ChatWindow.tsx:54`
```typescript
const data = await response.json()
```

**Result**:
```javascript
{
  message: "Great! I found some insurance quotes...",
  meta: {
    session_id: "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

#### Call 14.3: Create Assistant Message
**Line**: `frontend/components/ChatWindow.tsx:57-62`
```typescript
const assistantMessage: Message = {
  id: (Date.now() + 1).toString(),
  role: 'assistant',
  content: data.message || 'I apologize, but I could not generate a response.',
  timestamp: new Date(),
}
```

**Result**:
```javascript
{
  id: "1703456790001",
  role: "assistant",
  content: "Great! I found some insurance quotes...",
  timestamp: Date(2024-12-24T10:30:05.001Z)
}
```

#### Call 14.4: Update Messages State
**Line**: `frontend/components/ChatWindow.tsx:63`
```typescript
setMessages((prev) => [...prev, assistantMessage])
```

**State Change**:
```javascript
messages = [
  {
    id: "1703456789000",
    role: "user",
    content: "I need insurance for my 2020 Toyota Camry",
    timestamp: Date(...)
  },
  {
    id: "1703456790001",
    role: "assistant",
    content: "Great! I found some insurance quotes...",
    timestamp: Date(...)
  }
]
```

#### Call 14.5: Reset Loading State
**Line**: `frontend/components/ChatWindow.tsx:74`
```typescript
setIsLoading(false)
```

**State Change**: `isLoading`: `true` → `false`

#### Call 14.6: Trigger Auto-scroll
**Line**: `frontend/components/ChatWindow.tsx:23-25` (useEffect triggered by messages change)
```typescript
useEffect(() => {
  scrollToBottom()
}, [messages])
```

**Line**: `frontend/components/ChatWindow.tsx:19-21`
```typescript
const scrollToBottom = () => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
}
```

**Action**: Smooth scroll to bottom of chat

---

## LAYER 15: UI RENDER

### Call 15: React Re-render
**Component**: MessageList

**File**: `frontend/components/MessageList.tsx`

**Renders**: New assistant message displayed in chat UI

**Final UI State**: User sees the insurance quotes response

---

## COMPLETE CALL STACK SUMMARY

```
1. ChatWindow.handleSendMessage()                          [frontend/components/ChatWindow.tsx:27]
   └─> setMessages()                                       [ChatWindow.tsx:37]
   └─> setIsLoading(true)                                  [ChatWindow.tsx:38]
   └─> fetch('/api/chat')                                  [ChatWindow.tsx:41]
       │
       2. POST(request: NextRequest)                       [frontend/app/api/chat/route.ts:5]
          └─> request.json()                               [route.ts:7]
          └─> request.cookies.get('sid')                   [route.ts:18]
          └─> fetch('http://localhost:8000/chat')          [route.ts:21]
              │
              3. chat(request, response, sid)              [backend/api/chat.py:14]
                 └─> uuid.uuid4()                          [chat.py:25]
                 └─> response.set_cookie()                 [chat.py:29]
                 └─> ChatService.process_message()         [chat.py:39]
                     │
                     4. process_message(session_id, message) [backend/services/chat_service.py:14]
                        └─> get_memory()                   [chat_service.py:27]
                            │
                            5. get_memory(session_id, redis_url) [backend/memory/redis.py:9]
                               └─> RedisChatMessageHistory() [redis.py:21]
                               └─> return memory            [redis.py:26]
                        │
                        └─> create_agent_executor()        [chat_service.py:30]
                            │
                            6. create_agent_executor(session_id) [backend/agent/agent_factory.py:36]
                               └─> get_llm()               [agent_factory.py:49]
                               └─> get_tools()             [agent_factory.py:50]
                                   │
                                   7. get_tools()          [backend/agent/tools.py:59]
                                      └─> return [...]     [tools.py:61]
                               │
                               └─> ChatPromptTemplate.from_messages() [agent_factory.py:53]
                               └─> create_openai_tools_agent() [agent_factory.py:61]
                               └─> AgentExecutor()         [agent_factory.py:64]
                               └─> return agent_executor   [agent_factory.py:71]
                        │
                        └─> memory.messages                [chat_service.py:33]
                        │
                        └─> agent_executor.ainvoke()       [chat_service.py:36]
                            │
                            8. AgentExecutor.ainvoke()     [LangChain internal]
                               └─> Format prompt
                               └─> POST http://localhost:1234/v1/chat/completions (Call 1)
                               └─> LLM decides to call tool
                               └─> Execute mock_vehicle_lookup()
                                   │
                                   9. mock_vehicle_lookup() [backend/agent/tools.py:12]
                                      └─> logger.info()    [tools.py:25]
                                      └─> VehicleService.lookup_vehicle() [tools.py:28]
                                          │
                                          10. lookup_vehicle() [backend/services/vehicle_service.py:13]
                                              └─> logger.info() [vehicle_service.py:31]
                                              └─> return {...} [vehicle_service.py:44]
                               │
                               └─> POST http://localhost:1234/v1/chat/completions (Call 2)
                               └─> LLM decides to call another tool
                               └─> Execute mock_get_quote()
                                   │
                                   11. mock_get_quote()    [backend/agent/tools.py:32]
                                       └─> logger.info()   [tools.py:45]
                                       └─> QuoteService.get_quotes() [tools.py:51]
                                           │
                                           12. get_quotes() [backend/services/quote_service.py:13]
                                               └─> logger.info() [quote_service.py:31]
                                               └─> Calculate premiums [quote_service.py:37]
                                               └─> Generate quotes [quote_service.py:46]
                                               └─> return quotes [quote_service.py:83]
                               │
                               └─> POST http://localhost:1234/v1/chat/completions (Call 3)
                               └─> LLM generates final response
                               └─> return result
                        │
                        └─> result.get("output")           [chat_service.py:41]
                        └─> memory.add_user_message()      [chat_service.py:47]
                        └─> memory.add_ai_message()        [chat_service.py:48]
                        └─> return response                [chat_service.py:50]
                 │
                 └─> ChatResponse()                        [chat.py:41]
                 └─> return ChatResponse                   [chat.py:41]
          │
          └─> response.json()                              [route.ts:36]
          └─> NextResponse.json()                          [route.ts:39]
          └─> nextResponse.headers.set()                   [route.ts:44]
          └─> return nextResponse                          [route.ts:47]
   │
   └─> response.json()                                     [ChatWindow.tsx:54]
   └─> setMessages()                                       [ChatWindow.tsx:63]
   └─> setIsLoading(false)                                 [ChatWindow.tsx:74]
   └─> scrollToBottom()                                    [ChatWindow.tsx:19]
```

---

## Redis Operations Timeline

```
1. GET session:550e8400-e29b-41d4-a716-446655440000
   → Returns previous messages or empty list

2. RPUSH session:550e8400-e29b-41d4-a716-446655440000 <HumanMessage>
   → Adds user message

3. EXPIRE session:550e8400-e29b-41d4-a716-446655440000 86400
   → Reset 24hr TTL

4. RPUSH session:550e8400-e29b-41d4-a716-446655440000 <AIMessage>
   → Adds AI message

5. EXPIRE session:550e8400-e29b-41d4-a716-446655440000 86400
   → Reset 24hr TTL again
```

---

## LLM API Calls Timeline

```
Call 1: Initial message processing
  → Receives: User message + chat history
  → Responds: Tool call (mock_vehicle_lookup)

Call 2: After vehicle lookup tool result
  → Receives: Previous messages + tool result
  → Responds: Tool call (mock_get_quote)

Call 3: After quote tool result
  → Receives: All messages + all tool results
  → Responds: Final natural language response
```

---

## Performance Timing Breakdown

| Layer | Operation | Typical Time |
|-------|-----------|--------------|
| 1 | Frontend state update | ~5ms |
| 2 | HTTP request (frontend → proxy) | ~10ms |
| 3 | Proxy processing | ~5ms |
| 3 | HTTP request (proxy → backend) | ~15ms |
| 4 | Backend API processing | ~5ms |
| 5 | Redis GET (chat history) | ~5ms |
| 6 | Agent executor setup | ~10ms |
| 8 | LLM Call 1 (initial) | ~800ms |
| 9 | Vehicle lookup tool | ~2ms |
| 10 | LLM Call 2 (with vehicle data) | ~900ms |
| 11 | Quote tool | ~3ms |
| 12 | LLM Call 3 (final response) | ~1200ms |
| 13 | Redis RPUSH x2 (save messages) | ~8ms |
| 14 | Backend → Proxy → Frontend | ~30ms |
| 15 | Frontend state update & render | ~10ms |
| **TOTAL** | **End-to-end** | **~3.0 seconds** |

---

## Debugging Commands

### Monitor Real-time Calls

**Backend Logs**:
```bash
cd backend
uvicorn main:app --reload --log-level debug
```

**Redis Monitoring**:
```bash
redis-cli MONITOR
```

**Frontend Console**:
```javascript
// In browser DevTools Console
// Watch network tab for API calls
```

### Inspect State at Each Layer

**Layer 4 - API**:
```python
# Add to backend/api/chat.py:26
logger.info(f"Session ID: {session_id}")
logger.info(f"Message: {request.message}")
```

**Layer 5 - Service**:
```python
# Add to backend/services/chat_service.py:34
logger.info(f"Chat history length: {len(chat_history)}")
logger.info(f"Chat history: {chat_history}")
```

**Layer 7 - Tools**:
```python
# Already included in tools.py:25 and :45
# Shows all tool invocations
```

**Layer 9 - Services**:
```python
# Already included in vehicle_service.py:31 and quote_service.py:31
# Shows service calls with parameters
```

This complete call trace shows every single function invocation from user click to UI update!
