'''
This module tests whether a certain llm is set .
'''
import os
import sys
from dotenv import load_dotenv

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from agno.os import AgentOS
from agno.agent import Agent
from agno.models.azure.openai_chat import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Set NO_PROXY to avoid proxy for localhost connections (important for local MCP server access)
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

def test_azure_openai_model():
    '''
    This function tests the Azure OpenAI model initialization.
    '''
    try:
        agent = Agent(
                model=AzureOpenAI(id="gpt-4.1", api_version="2024-12-01-preview"), 
                reasoning_model=AzureOpenAI(id="gpt-4.1", api_version="2024-12-01-preview")
                )

        agent.print_response(
            "Where is the Eiffel Tower located?",
            stream=True,
            )

    except Exception as e:
        print(f"Error while testing Azure Open AI model: {e}")

if __name__ == "__main__":
    test_azure_openai_model()
