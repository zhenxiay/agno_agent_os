# AgnoOS - Multi-Agent Operating System

A powerful multi-agent orchestration platform built with the [Agno framework](https://docs.agno.com/) that enables seamless coordination between AI agents through MCP (Model Context Protocol) integrations.

## Features

- **Multi-Agent Architecture**: Deploy and coordinate multiple specialized AI agents
- **MCP Integration**: Connect to various services via Model Context Protocol
- **Team Collaboration**: Create agent teams for complex task coordination
- **Multiple LLM Support**: Choose between Claude Sonnet and Azure OpenAI models
- **Persistent Memory**: SQLite-based memory storage for agent context
- **MLflow Tracking**: Optional experiment tracking and monitoring
- **FastAPI Backend**: RESTful API with automatic documentation
- **Web Interface**: Connect via [os.agno.com](https://os.agno.com/)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agno_agent_os
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Running the Application

Start the AgnoOS server:

```bash
fastapi dev src/main.py --port 8010
```

The application will be available at:
- **API**: `http://localhost:8010`
- **Web Interface**: Connect to [https://os.agno.com/](https://os.agno.com/)
- **API Documentation**: `http://localhost:8010/docs`

## Architecture

### Available Agents

The system includes several pre-configured specialized agents:

- **GitHub Agent**: Interact with GitHub repositories and Copilot
- **Airbnb Agent**: Access Airbnb API services
- **Oracle Agent**: Connect to Oracle databases via MCP
- **FAQ Agent**: Answer frequently asked questions
- **MS SQL Agent**: Interact with Microsoft SQL Server databases

### Agent Teams

Agents can be organized into collaborative teams:

- **Research Team**: Combines GitHub, MS SQL, and Oracle agents for comprehensive data research

### MCP Integration

The platform leverages the Model Context Protocol (MCP) for:
- Database connections (Oracle, SQL Server)
- API integrations (GitHub, Airbnb)
- Documentation systems
- Custom service integrations

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# LLM Configuration
ANTHROPIC_API_KEY=your_anthropic_key
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint

# MLflow Tracking (Optional)
MLFLOW_TRACING=false
MLFLOW_TRACK_SERVER=local
MLFLOW_EXPERIMENT_NAME=MCP_Experiments
DATABRICKS_HOST=your_databricks_host

# Database Configuration
SQL_SERVER=your_sql_server_connection
```

### Agent Configuration

Agents can be configured with different models and parameters:

```python
from agents.MCPAgent import mcp_agent

# Create a custom agent
custom_agent = mcp_agent(
    agent_name="Custom Agent",
    mcp_url="https://your-mcp-server.com/mcp",
    llm="claude"  # or "azure_openai"
)
```

## Development

### Project Structure

```
agno_agent_os/
├── src/
│   ├── main.py              # Application entry point
│   ├── agents/              # Agent implementations
│   │   ├── MCPAgent.py      # Base MCP agent class
│   │   ├── github_agent.py  # GitHub integration
│   │   ├── oracle_agent.py  # Oracle database agent
│   │   └── ...
│   └── utils/               # Utility modules
│       ├── config.py        # Configuration management
│       ├── logger.py        # Logging utilities
│       ├── sqlite_memory.py # Memory storage
│       └── mlflow_tracer.py # MLflow integration
├── tests/                   # Test suite
├── pyproject.toml          # Project configuration
└── README.md
```

### Running Tests

```bash
uv run pytest tests/
```

### Adding New Agents

1. Create a new agent file in `src/agents/`:
```python
from agents.MCPAgent import mcp_agent

def create_agent():
    agent = mcp_agent(
        agent_name="My New Agent",
        mcp_url="https://my-service.com/mcp",
        llm="claude"
    )
    return agent.create_agent()
```

2. Import and register in `src/main.py`:
```python
from agents.my_new_agent import create_agent as create_my_agent

my_agent = create_my_agent()
```

## MLflow Integration

Enable experiment tracking and monitoring:

```env
MLFLOW_TRACING=true
MLFLOW_TRACK_SERVER=databricks  # or "local"
MLFLOW_EXPERIMENT_NAME=AgnoOS_Experiments
```

> [!NOTE]
> MLflow tracking helps monitor agent performance and conversation flows for debugging and optimization.

## API Usage

### Direct API Calls

```bash
# Get available agents
curl http://localhost:8010/agents

# Send a message to an agent
curl -X POST http://localhost:8010/agents/oracle-agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Query database for sales data"}'
```

### Web Interface

Connect to [https://os.agno.com/](https://os.agno.com/) and configure your local endpoint to interact with agents through a user-friendly interface.

## Troubleshooting

### Common Issues

1. **MCP Connection Errors**: Ensure MCP servers are running and accessible
2. **Database Connection Issues**: Verify database credentials and network connectivity
3. **API Key Errors**: Check that all required API keys are set in `.env`

### Proxy Configuration

For local MCP server access, the application automatically sets:
```python
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
```

## Technology Stack

- **[Agno Framework](https://docs.agno.com/)**: Multi-agent orchestration
- **FastAPI**: Web framework and API
- **SQLite**: Local data storage
- **MLflow**: Experiment tracking (optional)
- **MCP**: Model Context Protocol for integrations
- **Claude Sonnet**: Anthropic's language model
- **Azure OpenAI**: Microsoft's OpenAI service

---

> [!TIP]
> For detailed API documentation, visit `http://localhost:8010/docs` when the server is running.