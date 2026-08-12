import sqlite3
from pathlib import Path


# ============================================================
# DATABASE PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "supply_chain.db"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the
    Supply Chain SQLite database.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    # Return rows that can be accessed
    # using column names as well as indexes.
    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE HEALTH CHECK
# ============================================================

def check_database_connection() -> bool:
    """
    Check whether the database is accessible.
    """

    try:

        connection = get_db_connection()

        connection.execute(
            "SELECT 1"
        )

        connection.close()

        return True

    except sqlite3.Error:

        return False