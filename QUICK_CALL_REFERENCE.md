# Quick Call Reference - Function Names in Sequence

## Complete Request Path (Service → Method)

```
USER ACTION
  ↓
Frontend::ChatWindow.handleSendMessage(content)
  ↓
Frontend::fetch('/api/chat', {message})
  ↓
Next.js::POST(request)
  ├─ request.json()
  ├─ request.cookies.get('sid')
  └─ fetch('http://localhost:8000/chat')
     ↓
FastAPI::chat(request, response, sid)
  ├─ uuid.uuid4()                       6   # Generate session ID
  ├─ response.set_cookie('sid')             # Set session cookie
  └─ ChatService.process_message(session_id, message)
     ↓
ChatService::process_message(session_id, message)
  ├─ get_memory(session_id, redis_url)
  │  └─ RedisChatMessageHistory(session_id, url, ttl)
  │     └─ Redis::GET session:<uuid>        # Fetch chat history
  │
  ├─ create_agent_executor(session_id)
  │  ├─ get_llm()                           # Get LLM instance
  │  ├─ get_tools()                         # Get [vehicle_lookup, get_quote]
  │  ├─ ChatPromptTemplate.from_messages()  # Create prompt
  │  ├─ create_openai_tools_agent()         # Create agent
  │  └─ AgentExecutor()                     # Create executor
  │
  ├─ memory.messages                         # Get chat history
  │
  └─ agent_executor.ainvoke({input, chat_history})
     ↓
LangChain::AgentExecutor.ainvoke()
  ├─ Format prompt with system + history + input
  │
  ├─ LLM::POST /v1/chat/completions         # FIRST LLM CALL
  │  └─ Response: tool_call(mock_vehicle_lookup)
  │
  ├─ Execute tool: mock_vehicle_lookup(make, model, year)
  │  └─ VehicleService.lookup_vehicle(vin, make, model, year)
  │     ├─ logger.info()
  │     └─ return {vin, make, model, year, status}
  │
  ├─ LLM::POST /v1/chat/completions         # SECOND LLM CALL (with vehicle data)
  │  └─ Response: tool_call(mock_get_quote)
  │
  ├─ Execute tool: mock_get_quote(vehicle_make, vehicle_model, vehicle_year, coverage_type)
  │  └─ QuoteService.get_quotes(vehicle_make, vehicle_model, vehicle_year, coverage_type)
  │     ├─ logger.info()
  │     ├─ Calculate base_premium
  │     ├─ Generate 3 quotes with variations
  │     └─ return [quote1, quote2, quote3]
  │
  ├─ LLM::POST /v1/chat/completions         # THIRD LLM CALL (with all tool results)
  │  └─ Response: final_text
  │
  └─ return {output: final_text}
     ↓
ChatService::process_message (continued)
  ├─ result.get('output')                    # Extract response text
  ├─ memory.add_user_message(message)
  │  └─ Redis::RPUSH session:<uuid> + EXPIRE 86400
  ├─ memory.add_ai_message(response)
  │  └─ Redis::RPUSH session:<uuid> + EXPIRE 86400
  └─ return response
     ↓
FastAPI::chat (continued)
  └─ return ChatResponse(message, meta)
     ↓
Next.js::POST (continued)
  ├─ response.json()
  ├─ NextResponse.json(data)
  ├─ nextResponse.headers.set('set-cookie')
  └─ return nextResponse
     ↓
Frontend::ChatWindow.handleSendMessage (continued)
  ├─ response.json()
  ├─ setMessages([...prev, assistantMessage])
  ├─ setIsLoading(false)
  └─ scrollToBottom()
     ↓
UI UPDATED - User sees response
```

---

## Service Layer Call Map

### 1. API Layer
```
FastAPI Router (/chat)
  → chat(request, response, sid)
    → ChatService.process_message()
```

### 2. Service Layer
```
ChatService
  → process_message(session_id, message)
    → Returns: AI response text

VehicleService
  → lookup_vehicle(vin, make, model, year)
    → Returns: {vin, make, model, year, status}

QuoteService
  → get_quotes(vehicle_make, vehicle_model, vehicle_year, coverage_type)
    → Returns: [quote1, quote2, quote3]
```

### 3. Agent Layer
```
agent_factory
  → create_agent_executor(session_id)
    → get_llm() → Returns ChatOpenAI instance
    → get_tools() → Returns [mock_vehicle_lookup, mock_get_quote]
    → Returns: AgentExecutor

tools
  → mock_vehicle_lookup(**kwargs)
    → VehicleService.lookup_vehicle()

  → mock_get_quote(**kwargs)
    → QuoteService.get_quotes()
```

### 4. Memory Layer
```
redis
  → get_memory(session_id, redis_url)
    → RedisChatMessageHistory()
    → Returns: memory instance with methods:
      - .messages (get history)
      - .add_user_message(msg)
      - .add_ai_message(msg)
```

---

## Key Methods by File

### Frontend
| File | Method | Purpose |
|------|--------|---------|
| ChatWindow.tsx | handleSendMessage(content) | Handle user input |
| ChatWindow.tsx | setMessages(messages) | Update UI state |
| ChatWindow.tsx | setIsLoading(bool) | Toggle loading state |
| ChatWindow.tsx | scrollToBottom() | Auto-scroll chat |

### Next.js Proxy
| File | Method | Purpose |
|------|--------|---------|
| route.ts | POST(request) | Proxy requests to backend |
| route.ts | request.json() | Parse request body |
| route.ts | request.cookies.get('sid') | Extract session cookie |

### Backend API
| File | Method | Purpose |
|------|--------|---------|
| chat.py | chat(request, response, sid) | Main chat endpoint |
| chat.py | uuid.uuid4() | Generate session ID |
| chat.py | response.set_cookie() | Set session cookie |

### Services
| File | Method | Purpose |
|------|--------|---------|
| chat_service.py | ChatService.process_message() | Orchestrate chat flow |
| vehicle_service.py | VehicleService.lookup_vehicle() | Get vehicle info |
| quote_service.py | QuoteService.get_quotes() | Get insurance quotes |

### Agent
| File | Method | Purpose |
|------|--------|---------|
| agent_factory.py | create_agent_executor() | Create LangChain agent |
| agent_factory.py | get_llm() | Get LLM instance |
| tools.py | get_tools() | Get tool list |
| tools.py | mock_vehicle_lookup() | Vehicle lookup tool |
| tools.py | mock_get_quote() | Quote tool |

### Memory
| File | Method | Purpose |
|------|--------|---------|
| redis.py | get_memory() | Get Redis memory instance |

---

## LLM Call Sequence

```
1. agent_executor.ainvoke()
   ↓
2. POST http://localhost:1234/v1/chat/completions
   Payload: {messages: [system, history, user_input], tools: [...]}
   Response: {tool_calls: [mock_vehicle_lookup(...)]}
   ↓
3. Execute: VehicleService.lookup_vehicle()
   ↓
4. POST http://localhost:1234/v1/chat/completions
   Payload: {messages: [...previous, tool_result], tools: [...]}
   Response: {tool_calls: [mock_get_quote(...)]}
   ↓
5. Execute: QuoteService.get_quotes()
   ↓
6. POST http://localhost:1234/v1/chat/completions
   Payload: {messages: [...previous, tool_result], tools: [...]}
   Response: {content: "Great! I found quotes..."}
   ↓
7. Return final response
```

---

## Redis Operations

```
1. GET session:<session_id>
   → Retrieve chat history

2. RPUSH session:<session_id> <user_message>
   → Append user message

3. EXPIRE session:<session_id> 86400
   → Reset TTL to 24 hours

4. RPUSH session:<session_id> <ai_message>
   → Append AI message

5. EXPIRE session:<session_id> 86400
   → Reset TTL to 24 hours
```

---

## HTTP Endpoints Called

```
1. POST http://localhost:3000/api/chat
   Frontend → Next.js Proxy

2. POST http://localhost:8000/chat
   Next.js Proxy → FastAPI Backend

3. POST http://localhost:1234/v1/chat/completions (×3)
   Backend → LM Studio LLM
```

---

## Complete Function Call Chain (One Line Per Call)

```
1.  ChatWindow.handleSendMessage()
2.  ChatWindow.setMessages()
3.  ChatWindow.setIsLoading(true)
4.  fetch('/api/chat')
5.  route.POST()
6.  request.json()
7.  request.cookies.get('sid')
8.  fetch('http://localhost:8000/chat')
9.  chat()
10. uuid.uuid4()
11. response.set_cookie()
12. ChatService.process_message()
13. get_memory()
14. RedisChatMessageHistory()
15. create_agent_executor()
16. get_llm()
17. get_tools()
18. ChatPromptTemplate.from_messages()
19. create_openai_tools_agent()
20. AgentExecutor()
21. memory.messages (Redis GET)
22. agent_executor.ainvoke()
23. [LangChain formats prompt]
24. POST /v1/chat/completions (Call #1)
25. mock_vehicle_lookup()
26. VehicleService.lookup_vehicle()
27. POST /v1/chat/completions (Call #2)
28. mock_get_quote()
29. QuoteService.get_quotes()
30. POST /v1/chat/completions (Call #3)
31. result.get('output')
32. memory.add_user_message() (Redis RPUSH)
33. memory.add_ai_message() (Redis RPUSH)
34. ChatResponse()
35. response.json()
36. NextResponse.json()
37. nextResponse.headers.set()
38. response.json()
39. ChatWindow.setMessages()
40. ChatWindow.setIsLoading(false)
41. ChatWindow.scrollToBottom()
```

---

## Summary by Component

| Component | Entry Method | Exit Method | Return Value |
|-----------|--------------|-------------|--------------|
| Frontend | handleSendMessage | scrollToBottom | void |
| Next.js Proxy | POST | return NextResponse | NextResponse |
| FastAPI | chat | return ChatResponse | ChatResponse |
| ChatService | process_message | return response | string |
| AgentExecutor | ainvoke | return result | dict |
| VehicleService | lookup_vehicle | return {...} | dict |
| QuoteService | get_quotes | return [...] | list[dict] |
| Redis Memory | get_memory | return memory | RedisChatMessageHistory |

---

## Debugging Entry Points

To add debug logging at key points:

```python
# 1. API Entry
backend/api/chat.py:26
logger.info(f"🔵 API: Received message from session {session_id}")

# 2. Service Entry
backend/services/chat_service.py:27
logger.info(f"🟢 Service: Processing message: {message[:50]}...")

# 3. Agent Entry
backend/services/chat_service.py:36
logger.info(f"🟡 Agent: Invoking with {len(chat_history)} history messages")

# 4. Tool Calls
backend/agent/tools.py:25
logger.info(f"🔧 Tool: Vehicle lookup called")

backend/agent/tools.py:45
logger.info(f"🔧 Tool: Get quote called")

# 5. Service Calls
backend/services/vehicle_service.py:31
logger.info(f"🚗 VehicleService: Lookup {make} {model} {year}")

backend/services/quote_service.py:31
logger.info(f"💰 QuoteService: Get quotes for {vehicle_make}")

# 6. Memory Operations
backend/services/chat_service.py:47
logger.info(f"💾 Memory: Saving user message")

backend/services/chat_service.py:48
logger.info(f"💾 Memory: Saving AI message")
```

This creates a trace like:
```
🔵 API: Received message from session 550e8400...
🟢 Service: Processing message: I need insurance for my 2020...
🟡 Agent: Invoking with 2 history messages
🔧 Tool: Vehicle lookup called
🚗 VehicleService: Lookup Toyota Camry 2020
🔧 Tool: Get quote called
💰 QuoteService: Get quotes for Toyota
💾 Memory: Saving user message
💾 Memory: Saving AI message
```
