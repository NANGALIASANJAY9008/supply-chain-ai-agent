import re

from app.database.connection import get_db_connection


# ============================================================
# DATABASE CONFIGURATION

def get_connection():
    return get_db_connection()


# ============================================================
# ID EXTRACTION
# ============================================================

def extract_product_id(
    question: str,
) -> str | None:

    match = re.search(
        r"\bP\d{7}\b",
        question.upper(),
    )

    if match:
        return match.group(0)

    return None


def extract_supplier_id(
    question: str,
) -> str | None:

    match = re.search(
        r"\bS\d{6}\b",
        question.upper(),
    )

    if match:
        return match.group(0)

    return None


def extract_order_id(
    question: str,
) -> str | None:

    match = re.search(
        r"\bO\d{9}\b",
        question.upper(),
    )

    if match:
        return match.group(0)

    return None


# ============================================================
# PRODUCT LOOKUP
# ============================================================

def product_lookup(
    product_id: str,
) -> dict | None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            product_id,
            product_name,
            category,
            unit_price,
            reorder_level,
            warehouse
        FROM products
        WHERE product_id = %s
        """,
        (product_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "product_id": row[0],
        "product_name": row[1],
        "category": row[2],
        "unit_price": row[3],
        "reorder_level": row[4],
        "warehouse": row[5],
    }


# ============================================================
# INVENTORY LOOKUP
# ============================================================

def inventory_lookup(
    product_id: str,
) -> dict | None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            inventory_id,
            product_id,
            warehouse,
            current_stock,
            reserved_stock,
            incoming_stock,
            reorder_level,
            last_restock_date
        FROM inventory
        WHERE product_id = %s
        """,
        (product_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    available_stock = (
        row[3] - row[4]
    )

    return {
        "inventory_id": row[0],
        "product_id": row[1],
        "warehouse": row[2],
        "current_stock": row[3],
        "reserved_stock": row[4],
        "available_stock": available_stock,
        "incoming_stock": row[5],
        "reorder_level": row[6],
        "last_restock_date": row[7],
        "stock_status": (
            "LOW STOCK"
            if available_stock < row[6]
            else "SUFFICIENT STOCK"
        ),
    }


# ============================================================
# SUPPLIER LOOKUP
# ============================================================

def supplier_lookup(
    supplier_id: str,
) -> dict | None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            supplier_id,
            supplier_name,
            location,
            lead_time_days,
            reliability_score,
            average_delay_days
        FROM suppliers
        WHERE supplier_id = %s
        """,
        (supplier_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "supplier_id": row[0],
        "supplier_name": row[1],
        "location": row[2],
        "lead_time_days": row[3],
        "reliability_score": row[4],
        "average_delay_days": row[5],
    }


# ============================================================
# ORDER LOOKUP
# ============================================================

def order_lookup(
    order_id: str,
) -> dict | None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            order_id,
            product_id,
            supplier_id,
            order_date,
            expected_delivery_date,
            actual_delivery_date,
            quantity,
            unit_price,
            total_value,
            status
        FROM orders
        WHERE order_id = %s
        """,
        (order_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "order_id": row[0],
        "product_id": row[1],
        "supplier_id": row[2],
        "order_date": row[3],
        "expected_delivery_date": row[4],
        "actual_delivery_date": row[5],
        "quantity": row[6],
        "unit_price": row[7],
        "total_value": row[8],
        "status": row[9],
    }


# ============================================================
# LOW STOCK PRODUCTS
# ============================================================

def get_low_stock_products():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            i.product_id,
            p.product_name,
            i.warehouse,
            i.current_stock,
            i.reserved_stock,
            (i.current_stock - i.reserved_stock)
                AS available_stock,
            i.incoming_stock,
            i.reorder_level
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        WHERE
            (i.current_stock - i.reserved_stock)
            < i.reorder_level
        ORDER BY
            available_stock ASC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        results.append(
            {
                "product_id": row[0],
                "product_name": row[1],
                "warehouse": row[2],
                "current_stock": row[3],
                "reserved_stock": row[4],
                "available_stock": row[5],
                "incoming_stock": row[6],
                "reorder_level": row[7],
            }
        )

    return results


# ============================================================
# TOP RELIABLE SUPPLIERS
# ============================================================

def get_top_reliable_suppliers():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            supplier_id,
            supplier_name,
            location,
            lead_time_days,
            reliability_score,
            average_delay_days
        FROM suppliers
        ORDER BY reliability_score DESC
        LIMIT 5
        """
    )

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        results.append(
            {
                "supplier_id": row[0],
                "supplier_name": row[1],
                "location": row[2],
                "lead_time_days": row[3],
                "reliability_score": row[4],
                "average_delay_days": row[5],
            }
        )

    return results


# ============================================================
# ACTIVE / PENDING ORDERS
# ============================================================

def get_active_orders():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            order_id,
            product_id,
            supplier_id,
            order_date,
            expected_delivery_date,
            quantity,
            total_value,
            status
        FROM orders
        WHERE status IN (
            'Pending',
            'Processing',
            'Shipped'
        )
        ORDER BY order_date DESC
        LIMIT 20
        """
    )

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        results.append(
            {
                "order_id": row[0],
                "product_id": row[1],
                "supplier_id": row[2],
                "order_date": row[3],
                "expected_delivery_date": row[4],
                "quantity": row[5],
                "total_value": row[6],
                "status": row[7],
            }
        )

    return results


# ============================================================
# ORDERS BY PRODUCT
# ============================================================

def orders_by_product(
    product_id: str,
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            order_id,
            supplier_id,
            order_date,
            expected_delivery_date,
            actual_delivery_date,
            quantity,
            total_value,
            status
        FROM orders
        WHERE product_id = %s
        ORDER BY order_date DESC
        LIMIT 20
        """,
        (product_id,),
    )

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        results.append(
            {
                "order_id": row[0],
                "supplier_id": row[1],
                "order_date": row[2],
                "expected_delivery_date": row[3],
                "actual_delivery_date": row[4],
                "quantity": row[5],
                "total_value": row[6],
                "status": row[7],
            }
        )

    return results

# ============================================================
# HIGH DELAY / RISKY SUPPLIERS
# ============================================================

def get_high_delay_suppliers():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            supplier_id,
            supplier_name,
            location,
            lead_time_days,
            reliability_score,
            average_delay_days
        FROM suppliers
        ORDER BY average_delay_days DESC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        results.append(
            {
                "supplier_id": row[0],
                "supplier_name": row[1],
                "location": row[2],
                "lead_time_days": row[3],
                "reliability_score": row[4],
                "average_delay_days": row[5],
            }
        )

    return results

def get_active_order_summary():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            status,
            COUNT(*)
        FROM orders
        WHERE status IN (
            'Pending',
            'Processing',
            'Shipped',
            'In Transit'
        )
        GROUP BY status
        ORDER BY status
        """
    )

    rows = cursor.fetchall()

    connection.close()

    summary = {}

    total = 0

    for status, count in rows:

        summary[status] = count
        total += count

    return {
        "total_active_orders": total,
        "by_status": summary,
    }

def get_pending_order_count():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Pending'
        """
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count