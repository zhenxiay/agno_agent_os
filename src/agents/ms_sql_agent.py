'''
This module defines an agent configured to interact with a MS SQL Server instance via MCPTools.
'''
from sqlalchemy import create_engine
import urllib
from textwrap import dedent

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.sql import SQLTools

from utils.sqlite_memory import sqlite_db
from utils.agent_instructions import (
    get_ms_sql_agent_instructions,
    get_ms_sql_agent_output
    )
from utils.logger import get_logger
from utils.config import SQL_SERVER

# Initialize logger
logger = get_logger()

def get_connection_string() -> str:
    '''
    Get the connection string for Azure Synapse using the appropriate authentication method.

    Returns:
        Connection string for connecting to Azure Synapse
    '''

    _connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_SERVER};"
        f"Authentication=ActiveDirectoryIntegrated;"
        "Encrypt=yes;TrustServerCertificate=no;"
    )

    return _connection_string

def get_connection_for_toolkit():
    '''
    Create a sql db instance which can get the langchain sql database toolkit.
    '''
    params = urllib.parse.quote_plus(get_connection_string())
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    return engine

def create_agent(llm: str = "claude") -> Agent:
    '''
    This function creates an agent configured to interact with MS SQL server via MCPTools.

    Args:
        llm: The LLM model to use ("claude" or "AzureOpenAI")
    '''

    agent = Agent(
        name="MS SQL Agent",
        model=Claude("claude-sonnet-4-5") if llm == "claude" else AzureOpenAI(id="gpt-4.1", api_version="2024-12-01-preview"),
        db=sqlite_db(),
        tools=[
            SQLTools(db_engine=get_connection_for_toolkit()),
            ],
        instructions=get_ms_sql_agent_instructions(),
        expected_output=dedent(get_ms_sql_agent_output()),
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )

    return agent
