from agno.agent import Agent
from agno.team import Team
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.models.azure.openai_chat import AzureOpenAI
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

from dotenv import load_dotenv
import os

from utils.sqlite_memory import sqlite_db
from utils.logger import get_logger
from utils.mlflow_tracer import setup_mlflow_tracer
from utils.config import (
    MLFLOW_TRACING,
    MLFLOW_TRACK_SERVER,
    MLFLOW_EXPERIMENT_NAME,
    DATABRICKS_HOST,
)
from agents.github_agent import create_agent as create_github_agent
from agents.airbnb_agent import create_agent as create_airbnb_agent
from agents.oracle_agent import create_agent as create_oracle_agent
from agents.faq_agent import create_agent as create_faq_agent
from agents.ms_sql_agent import create_agent as create_ms_sql_agent

# Load environment variables from .env file
load_dotenv()

# Get logger
logger = get_logger()

# Set up MLflow tracer if enabled
if MLFLOW_TRACING == 'true':
    setup_mlflow_tracer(
        track_server=MLFLOW_TRACK_SERVER,
        experiment_name=MLFLOW_EXPERIMENT_NAME
                            )
    if MLFLOW_TRACK_SERVER == "databricks":
        logger.info(f"Initialized mlflow trace to Databricks: {DATABRICKS_HOST}")
    else:
        logger.info("Initialized mlflow trace to http://localhost:5000")

# Create the Agents
github_agent = create_github_agent()
airbnb_agent = create_airbnb_agent()
oracle_agent = create_oracle_agent()
faq_agent = create_faq_agent()
ms_sql_agent = create_ms_sql_agent()

# Create a team
research_team = Team(
    name="Research Team",
    description="A team of agents that collobarates to generate useful responses.",
    members=[
        oracle_agent, 
        ms_sql_agent
        ],
    model=AzureOpenAI(id="gpt-4.1", api_version="2024-12-01-preview"),
    #model=Claude(id="claude-sonnet-4-5"),
    id="research_team",
    instructions=[
        "You are the lead researcher of a research team! 🔍",
    ],
    db=sqlite_db(),
    enable_user_memories=True,
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
)

# Set NO_PROXY to avoid proxy for localhost connections (important for local MCP server access)
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

# Create the AgentOS
agent_os = AgentOS(
                    agents=[faq_agent,
                            #github_agent,
                            #airbnb_agent,
                            ms_sql_agent, 
                            oracle_agent],
                    teams=[research_team],
                    )
# Get the FastAPI app for the AgentOS
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app", port=8010)
