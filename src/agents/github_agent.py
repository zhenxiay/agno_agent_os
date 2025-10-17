'''
This module defines an agent configured to interact with GitHub Copilot via MCPTools.
'''

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

from dotenv import load_dotenv
from utils.sqlite_memory import sqlite_db

def create_agent():
    '''
    This function creates an agent configured to interact with GitHub Copilot via MCPTools.
    '''

    load_dotenv()

    agent = Agent(
        name="GitHub Agent",
        model=Claude(id="claude-sonnet-4-5"),
        db=sqlite_db(),
        tools=[
            MCPTools(transport="streamable-http", url="https://api.githubcopilot.com/mcp/"),
            ],
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )

    return agent
