from app.database.connection import (
    get_db_connection,
    check_database_connection,
)


def test_database_connection():

    assert check_database_connection() is True


def test_database_query():

    connection = get_db_connection()

    result = connection.execute(
        "SELECT 1 AS test_value"
    ).fetchone()

    connection.close()

    assert result["test_value"] == 1


def test_products_table():

    connection = get_db_connection()

    result = connection.execute(
        "SELECT COUNT(*) AS count FROM products"
    ).fetchone()

    connection.close()

    assert result["count"] == 100_000