from app.database.connection import get_db_connection


# ============================================================
# LOW STOCK PRODUCTS WITH INCOMING ORDERS
# ============================================================

def get_low_stock_with_incoming_orders(
    limit: int = 20,
) -> list[dict]:
    """
    Find products where available inventory is below
    the reorder level and there are pending/in-transit
    orders for that product.
    """

    connection = get_db_connection()

    query = """
        SELECT
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
            i.reorder_level,

            COUNT(o.order_id) AS active_order_count,

            COALESCE(
                SUM(o.quantity),
                0
            ) AS active_order_quantity

        FROM inventory AS i

        JOIN products AS p
            ON i.product_id = p.product_id

        LEFT JOIN orders AS o
            ON i.product_id = o.product_id

            AND o.status IN (
                'Pending',
                'In Transit'
            )

        WHERE (
            i.current_stock
            - i.reserved_stock
        ) < i.reorder_level

        GROUP BY
            i.product_id,
            p.product_name,
            p.category,
            i.warehouse,
            i.current_stock,
            i.reserved_stock,
            i.incoming_stock,
            i.reorder_level

        ORDER BY
            available_stock ASC

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
# SUPPLIER RISK ANALYSIS
# ============================================================

def get_supplier_risk_analysis(
    minimum_delay: float = 5.0,
    maximum_reliability: float = 80.0,
    limit: int = 20,
) -> list[dict]:
    """
    Find suppliers that have both:
    - high average delivery delay
    - relatively low reliability
    """

    connection = get_db_connection()

    query = """
        SELECT
            supplier_id,
            supplier_name,
            location,
            lead_time_days,
            reliability_score,
            average_delay_days
        FROM suppliers

        WHERE average_delay_days >= ?

        AND reliability_score <= ?

        ORDER BY
            average_delay_days DESC,
            reliability_score ASC

        LIMIT ?
    """

    rows = connection.execute(
        query,
        (
            minimum_delay,
            maximum_reliability,
            limit,
        ),
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]

# ============================================================
# PRODUCT ORDER SUMMARY
# ============================================================

def get_product_order_summary(
    product_id: str,
) -> dict | None:
    """
    Return order and inventory summary for a product.
    """

    connection = get_db_connection()

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,

            i.warehouse,
            i.current_stock,
            i.reserved_stock,
            i.incoming_stock,
            i.reorder_level,

            (
                i.current_stock
                - i.reserved_stock
            ) AS available_stock,

            COUNT(o.order_id) AS total_orders,

            COALESCE(
                SUM(o.quantity),
                0
            ) AS total_order_quantity,

            COALESCE(
                SUM(o.total_value),
                0
            ) AS total_order_value,

            SUM(
                CASE
                    WHEN o.status = 'Pending'
                    THEN 1
                    ELSE 0
                END
            ) AS pending_orders,

            SUM(
                CASE
                    WHEN o.status = 'In Transit'
                    THEN 1
                    ELSE 0
                END
            ) AS in_transit_orders

        FROM products AS p

        LEFT JOIN inventory AS i
            ON p.product_id = i.product_id

        LEFT JOIN orders AS o
            ON p.product_id = o.product_id

        WHERE p.product_id = ?

        GROUP BY
            p.product_id,
            p.product_name,
            p.category,
            i.warehouse,
            i.current_stock,
            i.reserved_stock,
            i.incoming_stock,
            i.reorder_level
    """

    row = connection.execute(
        query,
        (product_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)