'''
This module configures a SQLite database for use as a memory store.
'''

from agno.db.sqlite import SqliteDb

def sqlite_db(db_path: str = "agno.db") -> SqliteDb:
    '''
    This function configures and returns a SQLite database for use as a memory store.

    Args:
        db_path (str): The file path for the SQLite database. Defaults to "agno.db".

    Returns:
        SqliteDb: An instance of SqliteDb configured with the specified database file.
    '''
    return SqliteDb(db_file=db_path)