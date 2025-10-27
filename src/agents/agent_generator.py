"""
Agent Generator for dynamically creating MCP agents from a list (agent_list.json).
"""

import json
from typing import Dict, List, Optional
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.models.anthropic import Claude
from agno.models.azure.openai_chat import AzureOpenAI

from utils.logger import get_logger
from utils.sqlite_memory import sqlite_db

logger = get_logger()

def load_config(config_path: str) -> Dict:
    """Load agent configuration from JSON file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"Loaded agent configuration from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Agent configuration file not found: {config_path}")
    except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")


def create_agent_from_config(config_path,
                              agent_key,
                              llm) -> List:
    """
    Create actual Agent instances (not mcp_agent) from configuration.
    
    Args:
        config_path: Path to the agent configuration JSON file
        agent_keys: List of specific agent keys to create (None for all)
        llm: LLM provider to use
        
    Returns:
        List of Agent instances
    """
    load_dotenv()
    config = load_config(config_path="src/agents/agent_list.json")

    agent_config = config["agents"][agent_key]
    agent_url = agent_config.get("url")

    try:
        agent_name = f"{agent_key.title()} Agent"
            
        mcp_agent_instance  = Agent(
            name=agent_name,
            model=Claude("claude-sonnet-4-5") if llm == "claude" else AzureOpenAI(id="gpt-4.1", api_version="2024-12-01-preview"),
            db=sqlite_db(),
            tools=[
                MCPTools(
                    url=agent_url,
                    transport="streamable-http",
                    timeout_seconds=90
                    ),
                ],
            add_history_to_context=True,
            enable_user_memories=True,
            markdown=True,
        )
        logger.info(f"Created MCP agent: {agent_name} -> {agent_url} (LLM: {llm})")
        return mcp_agent_instance
            
    except Exception as e:
        logger.error(f"Failed to create agent '{agent_key}': {e}")
        return None

def create_multi_agents_from_config(agent_keys: Optional[List[str]] = None,
                                     llm: str = "claude") -> List:
    """
    Create actual Agent instances from configuration.
    
    Args:
        agent_keys: List of specific agent keys to create (None for all)
        llm: LLM provider to use
        
    Returns:
        List of Agent instances
    """

    agent_instances = []
    
    for key in agent_keys:
        agent_instance = create_agent_from_config(
            config_path="src/agents/agent_list.json",
            agent_key=key,
            llm=llm
        )
        agent_instances.append(agent_instance)

    return agent_instances
