from agno.agent import Agent
from agno.team import Team
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

from dotenv import load_dotenv
import os

from utils.sqlite_memory import sqlite_db
from agents.github_agent import create_agent as create_github_agent

# Load environment variables from .env file
load_dotenv()

# Create the Agents

github_agent = create_github_agent()

faq_agent = Agent(
    name="FAQ Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=sqlite_db(),
    tools=[
        MCPTools(transport="streamable-http", url="http://localhost:8000/faq/mcp"),
        ],
    add_history_to_context=True,
    enable_user_memories=True,
    markdown=True,
)

wikipedia_agent = Agent(
    name="wikipedia Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=sqlite_db(),
    tools=[
        MCPTools(transport="streamable-http", url="http://localhost:8000/wikipedia/mcp"),
        ],
    add_history_to_context=True,
    enable_user_memories=True,
    markdown=True,
)

oracle_agent = Agent(
    name="Oracle Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=sqlite_db(),
    tools=[
        MCPTools(transport="streamable-http", url="http://localhost:8000/oracle/mcp"),
        ],
    add_history_to_context=True,
    enable_user_memories=True,
    markdown=True,
)

# Create a team
research_team = Team(
    name="Research Team",
    description="A team of agents that collobarates to generate useful responses.",
    members=[docupedia_agent, oracle_agent],
    model=Claude(id="claude-sonnet-4-5"),
    id="research_team",
    instructions=[
        "You are the lead researcher of a research team! 🔍",
    ],
    db=sqlite_db(),
    enable_user_memories=True,
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
                            docupedia_agent, 
                            oracle_agent],
                    teams=[research_team],
                    )
# Get the FastAPI app for the AgentOS
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app", port=8010)
