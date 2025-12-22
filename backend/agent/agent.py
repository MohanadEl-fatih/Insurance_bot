"""LangChain agent setup with tools and memory."""
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.agent.llm import get_llm
from backend.agent.tools import get_tools
from backend.memory.redis import get_memory
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

# System prompt for the insurance agent
SYSTEM_PROMPT = """You are a helpful insurance quote assistant. Your goal is to help users get insurance quotes for their vehicles.

When interacting with users:
1. Identify their intent - they may want vehicle information, insurance quotes, or have questions about coverage types
2. Ask targeted follow-up questions if you need missing information (make, model, year, coverage type)
3. Use the vehicle_lookup tool first if vehicle details are unclear
4. Use the get_quote tool to retrieve quotes after you have vehicle information
5. Always present the cheapest quote prominently, but show all available options
6. Summarize quotes clearly with:
   - Provider name
   - Monthly premium (with currency)
   - Coverage type
   - Key features/conditions
   - Next steps for the user

Be conversational, friendly, and helpful. If a user asks about coverage types, explain:
- Liability: Basic coverage required by law
- Comprehensive: Covers theft, vandalism, natural disasters
- Full: Complete coverage including liability, comprehensive, and collision

Always be clear about what information you need to proceed."""


def create_agent(session_id: str):
    """
    Create a LangChain agent with tools for a session.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        Tuple of (AgentExecutor, memory) for the session
    """
    llm = get_llm()
    tools = get_tools()
    
    # Get memory for this session
    memory = get_memory(session_id, settings.redis_url)
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    return agent_executor, memory


async def ask_agent(agent_executor: AgentExecutor, memory, message: str) -> str:
    """
    Send a message to the agent and get a response.
    
    Args:
        agent_executor: The agent executor instance
        memory: Redis chat message history instance
        message: User message
        
    Returns:
        Agent response as string
    """
    try:
        # Get current chat history (previous messages, not including current)
        chat_history = memory.messages
        
        # Invoke agent with current message and history
        result = await agent_executor.ainvoke({
            "input": message,
            "chat_history": chat_history,
        })
        
        response = result.get("output", "I apologize, but I couldn't generate a response.")
        
        # Add both user message and assistant response to memory for persistence
        memory.add_user_message(message)
        memory.add_ai_message(response)
        
        return response
    
    except Exception as e:
        logger.error(f"Error in agent execution: {e}", exc_info=True)
        error_msg = f"I encountered an error while processing your request: {str(e)}"
        # Add error message to memory
        memory.add_ai_message(error_msg)
        return error_msg

