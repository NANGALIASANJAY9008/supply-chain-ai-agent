from typing import Optional

from app.database.connection import get_db_connection


# ============================================================
# GET ORDER BY ID
# ============================================================

def get_order_by_id(
    order_id: str,
) -> Optional[dict]:
    """
    Retrieve complete information for a specific order.

    Returns:
        Order information as a dictionary,
        or None if the order does not exist.
    """

    connection = get_db_connection()

    query = """
        SELECT
            o.order_id,
            o.product_id,
            p.product_name,
            o.supplier_id,
            s.supplier_name,
            o.order_date,
            o.expected_delivery_date,
            o.actual_delivery_date,
            o.quantity,
            o.unit_price,
            o.total_value,
            o.status
        FROM orders AS o

        JOIN products AS p
            ON o.product_id = p.product_id

        JOIN suppliers AS s
            ON o.supplier_id = s.supplier_id

        WHERE o.order_id = ?
    """

    row = connection.execute(
        query,
        (order_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


# ============================================================
# GET ORDERS FOR A PRODUCT
# ============================================================

def get_orders_by_product(
    product_id: str,
    limit: int = 20,
) -> list[dict]:
    """
    Retrieve orders associated with a specific product.
    """

    connection = get_db_connection()

    query = """
        SELECT
            o.order_id,
            o.product_id,
            p.product_name,
            o.supplier_id,
            s.supplier_name,
            o.order_date,
            o.expected_delivery_date,
            o.actual_delivery_date,
            o.quantity,
            o.unit_price,
            o.total_value,
            o.status
        FROM orders AS o

        JOIN products AS p
            ON o.product_id = p.product_id

        JOIN suppliers AS s
            ON o.supplier_id = s.supplier_id

        WHERE o.product_id = ?

        ORDER BY o.order_date DESC

        LIMIT ?
    """

    rows = connection.execute(
        query,
        (product_id, limit),
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# GET ORDERS FOR A SUPPLIER
# ============================================================

def get_orders_by_supplier(
    supplier_id: str,
    limit: int = 20,
) -> list[dict]:
    """
    Retrieve orders associated with a specific supplier.
    """

    connection = get_db_connection()

    query = """
        SELECT
            o.order_id,
            o.product_id,
            p.product_name,
            o.supplier_id,
            s.supplier_name,
            o.order_date,
            o.expected_delivery_date,
            o.actual_delivery_date,
            o.quantity,
            o.unit_price,
            o.total_value,
            o.status
        FROM orders AS o

        JOIN products AS p
            ON o.product_id = p.product_id

        JOIN suppliers AS s
            ON o.supplier_id = s.supplier_id

        WHERE o.supplier_id = ?

        ORDER BY o.order_date DESC

        LIMIT ?
    """

    rows = connection.execute(
        query,
        (supplier_id, limit),
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# GET ACTIVE ORDERS
# ============================================================

def get_active_orders(
    limit: int = 20,
) -> list[dict]:
    """
    Retrieve orders that are currently pending
    or in transit.
    """

    connection = get_db_connection()

    query = """
        SELECT
            o.order_id,
            o.product_id,
            p.product_name,
            o.supplier_id,
            s.supplier_name,
            o.order_date,
            o.expected_delivery_date,
            o.quantity,
            o.unit_price,
            o.total_value,
            o.status
        FROM orders AS o

        JOIN products AS p
            ON o.product_id = p.product_id

        JOIN suppliers AS s
            ON o.supplier_id = s.supplier_id

        WHERE o.status IN (
            'Pending',
            'In Transit'
        )

        ORDER BY o.order_date DESC

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


# ============================================================
# ORDER STATISTICS
# ============================================================

def get_order_statistics() -> dict:
    """
    Return overall order statistics.
    """

    connection = get_db_connection()

    query = """
        SELECT
            COUNT(*) AS total_orders,

            SUM(quantity) AS total_quantity,

            SUM(total_value) AS total_order_value,

            SUM(
                CASE
                    WHEN status = 'Pending'
                    THEN 1
                    ELSE 0
                END
            ) AS pending_orders,

            SUM(
                CASE
                    WHEN status = 'In Transit'
                    THEN 1
                    ELSE 0
                END
            ) AS in_transit_orders,

            SUM(
                CASE
                    WHEN status = 'Delivered'
                    THEN 1
                    ELSE 0
                END
            ) AS delivered_orders,

            SUM(
                CASE
                    WHEN status = 'Delivered Late'
                    THEN 1
                    ELSE 0
                END
            ) AS delivered_late_orders

        FROM orders
    """

    row = connection.execute(
        query
    ).fetchone()

    connection.close()

    return dict(row)