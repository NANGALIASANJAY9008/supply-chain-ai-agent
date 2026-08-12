import os
import sqlite3

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SQLITE_PATH = "database/supply_chain.db"

BATCH_SIZE = 5000


# ============================================================
# VALIDATION
# ============================================================

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

if not os.path.exists(SQLITE_PATH):
    raise FileNotFoundError(
        f"SQLite database not found: {SQLITE_PATH}"
    )


# ============================================================
# TABLE SCHEMAS
# ============================================================

TABLES = {
    "products": [
        ("product_id", "TEXT"),
        ("product_name", "TEXT"),
        ("category", "TEXT"),
        ("unit_price", "DOUBLE PRECISION"),
        ("reorder_level", "INTEGER"),
        ("warehouse", "TEXT"),
    ],

    "inventory": [
        ("inventory_id", "TEXT"),
        ("product_id", "TEXT"),
        ("warehouse", "TEXT"),
        ("current_stock", "INTEGER"),
        ("reserved_stock", "INTEGER"),
        ("incoming_stock", "INTEGER"),
        ("reorder_level", "INTEGER"),
        ("last_restock_date", "TEXT"),
    ],

    "suppliers": [
        ("supplier_id", "TEXT"),
        ("supplier_name", "TEXT"),
        ("location", "TEXT"),
        ("lead_time_days", "INTEGER"),
        ("reliability_score", "DOUBLE PRECISION"),
        ("average_delay_days", "DOUBLE PRECISION"),
    ],

    "orders": [
        ("order_id", "TEXT"),
        ("product_id", "TEXT"),
        ("supplier_id", "TEXT"),
        ("order_date", "TEXT"),
        ("expected_delivery_date", "TEXT"),
        ("actual_delivery_date", "TEXT"),
        ("quantity", "INTEGER"),
        ("unit_price", "DOUBLE PRECISION"),
        ("total_value", "DOUBLE PRECISION"),
        ("status", "TEXT"),
    ],
}


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables(pg_conn):
    cursor = pg_conn.cursor()

    for table_name, columns in TABLES.items():

        column_sql = ", ".join(
            f"{name} {data_type}"
            for name, data_type in columns
        )

        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {column_sql}
        )
        """

        cursor.execute(sql)

        print(f"Table ready: {table_name}")

    pg_conn.commit()
    cursor.close()


# ============================================================
# MIGRATE ONE TABLE
# ============================================================

def migrate_table(sqlite_conn, pg_conn, table_name, columns):

    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()

    column_names = [name for name, _ in columns]

    columns_sql = ", ".join(column_names)

    placeholders = ", ".join(
        ["%s"] * len(column_names)
    )

    select_sql = f"""
        SELECT {columns_sql}
        FROM {table_name}
    """

    insert_sql = f"""
        INSERT INTO {table_name}
        ({columns_sql})
        VALUES %s
    """

    sqlite_cursor.execute(select_sql)

    total_inserted = 0

    while True:

        rows = sqlite_cursor.fetchmany(BATCH_SIZE)

        if not rows:
            break

        execute_values(
            pg_cursor,
            insert_sql,
            rows,
            page_size=BATCH_SIZE
        )

        pg_conn.commit()

        total_inserted += len(rows)

        print(
            f"{table_name}: "
            f"{total_inserted:,} rows migrated"
        )

    sqlite_cursor.close()
    pg_cursor.close()

    print(
        f"Completed {table_name}: "
        f"{total_inserted:,} rows"
    )


# ============================================================
# VERIFY ROW COUNTS
# ============================================================

def verify_counts(pg_conn):

    cursor = pg_conn.cursor()

    print("\n")
    print("=" * 60)
    print("POSTGRESQL ROW COUNTS")
    print("=" * 60)

    for table_name in TABLES:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table_name:15} {count:,}"
        )

    cursor.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("SQLITE → POSTGRESQL MIGRATION")
    print("=" * 60)

    print("\nConnecting to SQLite...")

    sqlite_conn = sqlite3.connect(
        SQLITE_PATH
    )

    print("SQLite connection: SUCCESS")

    print("\nConnecting to PostgreSQL...")

    pg_conn = psycopg2.connect(
        DATABASE_URL
    )

    print("PostgreSQL connection: SUCCESS")

    try:

        print("\nCreating PostgreSQL tables...")

        create_tables(pg_conn)

        for table_name, columns in TABLES.items():

            print("\n")
            print("=" * 60)
            print(f"MIGRATING: {table_name}")
            print("=" * 60)

            migrate_table(
                sqlite_conn,
                pg_conn,
                table_name,
                columns
            )

        verify_counts(pg_conn)

        print("\n")
        print("=" * 60)
        print("MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception:

        pg_conn.rollback()

        print("\nMigration failed.")

        raise

    finally:

        sqlite_conn.close()
        pg_conn.close()

        print("\nConnections closed.")


if __name__ == "__main__":
    main()