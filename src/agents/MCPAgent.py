'''
This module defines an agent class which connects with MCP tools.
This object can be used to create different agents by changing the MCP tool command.
'''

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.mcp import MCPTools

from dotenv import load_dotenv
from utils.sqlite_memory import sqlite_db

class mcp_agent:
    '''
    This class defines an agent class configured to interact with MCPTools.
     Args:

        agent_name (str): The agent name to use.
        mcp_url (str): The url of the mcp server.
        llm (str): The llm provider to use -> choose from claude or azure_openai.
    '''
    
    def __init__(self, agent_name: str, mcp_url: str, llm: str):
        self.db = sqlite_db()
        self.add_history_to_context=True
        self.enable_user_memories=True
        self.markdown=True
        self.agent_name = agent_name
        self.mcp_url = mcp_url
        self.transport="streamable-http"
        self.timeout_seconds = 30
        self.model = Claude("claude-sonnet-4-5") if llm == "claude" else AzureOpenAI(id="gpt-4.1", api_version="2024-12-01-preview")
        self.agent = None

    def create_agent(self):
        '''
        This function creates an agent configured to interact with Airbnb API via MCPTools.
        '''

        load_dotenv()

        self.agent = Agent(
            name=self.agent_name,
            model=self.model,
            db=self.db,
            tools=[
                MCPTools(
                    url=self.mcp_url,
                    transport=self.transport,
                    timeout_seconds=self.timeout_seconds
                    ),
                ],
            add_history_to_context=self.add_history_to_context,
            enable_user_memories=self.enable_user_memories,
            markdown=self.markdown,
        )

        return self.agent
