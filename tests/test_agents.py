'''
This module tests whether various agents are configured corrected.
'''
import os
import sys
from dotenv import load_dotenv

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from agno.os import AgentOS
from agents.github_agent import create_agent as create_github_agent
from agents.airbnb_agent import create_agent as create_airbnb_agent
from agents.oracle_agent import create_agent as create_oracle_agent
from agents.faq_agent import create_agent as create_faq_agent
from agents.ms_sql_agent import create_agent as create_ms_sql_agent

# Load environment variables from .env file
load_dotenv()

# Set NO_PROXY to avoid proxy for localhost connections (important for local MCP server access)
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

def test_faq_agent():
    '''
    Test function for FAQ Agent.
    '''
    try:
        agent = create_faq_agent()
        print(agent.name)
        print(len(agent.tools))
        print(agent.tools[0].url)
        # Test to create the AgentOS with the agent
        agent_os = AgentOS(
                    agents=[
                        agent,
                            ]
                    )
        print(agent_os.agents[0].name)
    except Exception as e:
        print(f"Error while testing FAQ Agent: {e}")
    #assert agent.name == "FAQ Agent"
    #assert len(agent.tools) == 1
    #assert agent.tools[0].url == "http://localhost:8000/thor_faq/mcp"

def test_mssql_agent():
    '''
    Test function for ms sql Agent.
    '''
    try:
        agent = create_ms_sql_agent()
        print(agent.name)
        print(len(agent.tools))
        for tool in agent.tools:
            print(tool.url)
    except Exception as e:
        print(f"Error while testing Docupedia Agent: {e}")

def test_oracle_agent():
    '''
    Test function for FAQ Agent.
    '''
    try:
        agent = create_oracle_agent()
        print(agent.name)
        print(len(agent.tools))
        for tool in agent.tools:
            print(tool.urls)
    except Exception as e:
        print(f"Error while testing FAQ Agent: {e}")

def test_agent_os():
    '''
    Test function for AgentOS with multiple agents.
    '''
    try:
        faq_agent = create_faq_agent()
        oracle_agent = create_oracle_agent()
        ms_sql_agent = create_ms_sql_agent()

        agent_os = AgentOS(
                    agents=[
                        faq_agent,
                        oracle_agent,
                        ms_sql_agent,
                            ]
                    )
        print(f"AgentOS created with agents: {[agent.name for agent in agent_os.agents]}")
    except Exception as e:
        print(f"Error while testing AgentOS: {e}")

if __name__ == "__main__":
    test_faq_agent()
    test_oracle_agent()
    test_mssql_agent()
    test_agent_os()
