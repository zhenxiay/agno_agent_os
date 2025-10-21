"""
Configuration module for the agent application.
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables for mlflow tracer
MLFLOW_TRACING=os.getenv("MLFLOW_TRACING", "false")  # Default to false if not specified
MLFLOW_TRACK_SERVER = os.getenv("MLFLOW_TRACK_SERVER", "local")  # Default to local if not specified
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "MCP_Experiments")  # Default experiment name
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")

# SQL Server configuration
SQL_SERVER=os.getenv("SQL_SERVER")  # Default to a placeholder if not specified