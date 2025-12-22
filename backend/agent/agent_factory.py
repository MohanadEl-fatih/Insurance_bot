"""LangChain agent factory for creating agent executors."""
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


def create_agent_executor(session_id: str) -> AgentExecutor:
    """
    Create a LangChain agent executor with tools for a session.
    
    This is a LangChain-specific implementation detail. The service layer
    should use this factory to get agent executors.
    
    Args:
        session_id: Unique session identifier (used for memory initialization)
        
    Returns:
        AgentExecutor instance configured with tools and prompt
    """
    llm = get_llm()
    tools = get_tools()
    
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
    
    return agent_executor


