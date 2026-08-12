import os
import sqlite3
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# SQLITE CONFIGURATION
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

def get_db_connection():
    """
    Return a database connection.

    If DATABASE_URL is configured, PostgreSQL is used.
    Otherwise, local SQLite is used.
    """

    database_url = os.getenv("DATABASE_URL")

    # --------------------------------------------------------
    # PostgreSQL
    # --------------------------------------------------------

    if database_url:
        return psycopg2.connect(
            database_url
        )

    # --------------------------------------------------------
    # Local SQLite fallback
    # --------------------------------------------------------

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE HEALTH CHECK
# ============================================================

def check_database_connection() -> bool:
    """
    Check whether the configured database is accessible.
    """

    connection = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1"
        )

        cursor.fetchone()

        cursor.close()
        connection.close()

        return True

    except Exception:

        if connection:
            connection.close()

        return False