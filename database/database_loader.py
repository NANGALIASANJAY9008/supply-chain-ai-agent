import sqlite3
from pathlib import Path

import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_FILE = DATABASE_DIR / "supply_chain.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    return connection


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    print("=" * 60)
    print("SUPPLY CHAIN DATABASE CREATION")
    print("=" * 60)

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Remove existing database
    # --------------------------------------------------------

    if DATABASE_FILE.exists():

        print("\nExisting database found.")
        print("Removing old database...")

        DATABASE_FILE.unlink()

    # --------------------------------------------------------
    # Connect to SQLite
    # --------------------------------------------------------

    connection = get_connection()

    print("\nDatabase connection established.")

    # ========================================================
    # PRODUCTS
    # ========================================================

    print("\nLoading products...")

    products_file = DATA_DIR / "products.csv"

    products = pd.read_csv(
        products_file
    )

    products.to_sql(
        "products",
        connection,
        if_exists="replace",
        index=False
    )

    print(
        f"Products loaded: {len(products):,}"
    )

    # ========================================================
    # SUPPLIERS
    # ========================================================

    print("\nLoading suppliers...")

    suppliers_file = DATA_DIR / "suppliers.csv"

    suppliers = pd.read_csv(
        suppliers_file
    )

    suppliers.to_sql(
        "suppliers",
        connection,
        if_exists="replace",
        index=False
    )

    print(
        f"Suppliers loaded: {len(suppliers):,}"
    )

    # ========================================================
    # INVENTORY
    # ========================================================

    print("\nLoading inventory...")

    inventory_file = DATA_DIR / "inventory.csv"

    inventory = pd.read_csv(
        inventory_file
    )

    inventory.to_sql(
        "inventory",
        connection,
        if_exists="replace",
        index=False
    )

    print(
        f"Inventory loaded: {len(inventory):,}"
    )

    # ========================================================
    # ORDERS
    # ========================================================

    print("\nLoading orders...")

    orders_file = DATA_DIR / "orders.csv"

    orders = pd.read_csv(
        orders_file
    )

    orders.to_sql(
        "orders",
        connection,
        if_exists="replace",
        index=False,
        chunksize=100_000
    )

    print(
        f"Orders loaded: {len(orders):,}"
    )

    # ========================================================
    # CREATE INDEXES
    # ========================================================

    print("\nCreating database indexes...")

    cursor = connection.cursor()

    # Products
    cursor.execute("""
        CREATE INDEX idx_products_product_id
        ON products(product_id)
    """)

    # Suppliers
    cursor.execute("""
        CREATE INDEX idx_suppliers_supplier_id
        ON suppliers(supplier_id)
    """)

    # Inventory
    cursor.execute("""
        CREATE INDEX idx_inventory_product_id
        ON inventory(product_id)
    """)

    cursor.execute("""
        CREATE INDEX idx_inventory_warehouse
        ON inventory(warehouse)
    """)

    # Orders
    cursor.execute("""
        CREATE INDEX idx_orders_order_id
        ON orders(order_id)
    """)

    cursor.execute("""
        CREATE INDEX idx_orders_product_id
        ON orders(product_id)
    """)

    cursor.execute("""
        CREATE INDEX idx_orders_supplier_id
        ON orders(supplier_id)
    """)

    cursor.execute("""
        CREATE INDEX idx_orders_status
        ON orders(status)
    """)

    connection.commit()

    print("Indexes created successfully.")

    # ========================================================
    # CLOSE CONNECTION
    # ========================================================

    connection.close()

    print("\n" + "=" * 60)
    print("DATABASE CREATION COMPLETED")
    print("=" * 60)

    print(
        f"\nDatabase location:\n{DATABASE_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    create_database()