'''
This module defines an agent configured to interact with a FAQ page via MCPTools.
'''

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

from dotenv import load_dotenv
from utils.sqlite_memory import sqlite_db
from utils.agent_instructions import get_faq_agent_instructions

def create_agent():
    '''
    This function creates an agent configured to interact with Airbnb API via MCPTools.
    '''

    load_dotenv()

    agent = Agent(
        name="FAQ Agent",
        model=Claude(id="claude-sonnet-4-5"),
        db=sqlite_db(),
        instructions=get_faq_agent_instructions(),
        tools=[
            MCPTools(transport="streamable-http", url="http://localhost:8000/thor_faq/mcp"),
            ],
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )

    return agent
