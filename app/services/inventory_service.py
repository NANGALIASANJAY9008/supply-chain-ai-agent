from typing import Optional

from app.database.connection import get_db_connection


# ============================================================
# GET INVENTORY BY PRODUCT ID
# ============================================================

def get_inventory_by_product(
    product_id: str,
) -> Optional[dict]:
    """
    Retrieve inventory information for a specific product.

    Returns:
        Dictionary containing inventory information,
        or None if the product does not exist.
    """

    connection = get_db_connection()

    query = """
        SELECT
            i.inventory_id,
            i.product_id,
            p.product_name,
            p.category,
            i.warehouse,
            i.current_stock,
            i.reserved_stock,
            i.incoming_stock,
            i.reorder_level,
            i.last_restock_date
        FROM inventory AS i
        JOIN products AS p
            ON i.product_id = p.product_id
        WHERE i.product_id = ?
    """

    row = connection.execute(
        query,
        (product_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    available_stock = (
        row["current_stock"]
        - row["reserved_stock"]
    )

    if available_stock < row["reorder_level"]:
        stock_status = "LOW STOCK"
    else:
        stock_status = "SUFFICIENT STOCK"

    return {
        "inventory_id": row["inventory_id"],
        "product_id": row["product_id"],
        "product_name": row["product_name"],
        "category": row["category"],
        "warehouse": row["warehouse"],
        "current_stock": row["current_stock"],
        "reserved_stock": row["reserved_stock"],
        "available_stock": available_stock,
        "incoming_stock": row["incoming_stock"],
        "reorder_level": row["reorder_level"],
        "last_restock_date": row["last_restock_date"],
        "stock_status": stock_status,
    }

def get_low_stock_products(
    limit: int = 20,
) -> list[dict]:
    """
    Return products whose available stock
    is below their reorder level.
    """

    connection = get_db_connection()

    query = """
        SELECT
            i.inventory_id,
            i.product_id,
            p.product_name,
            p.category,
            i.warehouse,
            i.current_stock,
            i.reserved_stock,
            (
                i.current_stock
                - i.reserved_stock
            ) AS available_stock,
            i.incoming_stock,
            i.reorder_level
        FROM inventory AS i
        JOIN products AS p
            ON i.product_id = p.product_id
        WHERE (
            i.current_stock
            - i.reserved_stock
        ) < i.reorder_level
        ORDER BY available_stock ASC
        LIMIT ?
    """

    rows = connection.execute(
        query,
        (limit,),
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]