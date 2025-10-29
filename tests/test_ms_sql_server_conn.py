'''
This module tests the connection to the SQL server using the configuration defined in utils.config.
'''
import os
import sys
# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from sqlalchemy import text

from agents.ms_sql_agent import get_connection_for_toolkit

from utils.logger import get_logger
from utils.config import SQL_SERVER

# Initialize logger
logger = get_logger()

def test_sql_server_connection():
    '''
    Test function for SQL Server connection.
    '''
    try:
        engine = get_connection_for_toolkit()
        query = "SELECT @@VERSION"
        with engine.connect() as connection:
            result = connection.execute(text(query))
            version = result.fetchone()
            logger.info(f"Successfully connected to SQL Server: {version[0]}")
    except Exception as e:
        logger.error(f"Error while connecting to SQL Server at {SQL_SERVER}: {e}")

if __name__ == "__main__":
    test_sql_server_connection()
