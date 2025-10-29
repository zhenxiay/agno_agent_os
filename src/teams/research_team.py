'''
This module defines a research team of agents that collaborate to generate useful responses.
'''
from agno.team import Team
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.reasoning import ReasoningTools

from utils.sqlite_memory import sqlite_db

def create_team(member_list: list) -> Team:
    '''
    Create a research team with the given members.

    Args:
        member_list: List of Agent instances to be members of the team.

    Returns:
        An instance of Team configured as a research team.
    '''

    research_team = Team(
        name="Research Team",
        description="A team of agents that collobarates to generate useful responses.",
        members=member_list,
        model=AzureOpenAI(id="gpt-4.1", api_version="2024-12-01-preview"),
        id="research_team",
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are the lead researcher of a research team! 🔍",
        ],
        db=sqlite_db(),
        enable_user_memories=True,
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
    )

    return research_team
