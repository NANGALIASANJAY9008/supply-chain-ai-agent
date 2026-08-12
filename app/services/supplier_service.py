from typing import Optional

from app.database.connection import get_db_connection


# ============================================================
# GET SUPPLIER BY ID
# ============================================================

def get_supplier_by_id(
    supplier_id: str,
) -> Optional[dict]:
    """
    Retrieve supplier information by supplier ID.

    Returns:
        Supplier information as a dictionary,
        or None if the supplier does not exist.
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
        WHERE supplier_id = ?
    """

    row = connection.execute(
        query,
        (supplier_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "supplier_id": row["supplier_id"],
        "supplier_name": row["supplier_name"],
        "location": row["location"],
        "lead_time_days": row["lead_time_days"],
        "reliability_score": row["reliability_score"],
        "average_delay_days": row["average_delay_days"],
    }


# ============================================================
# GET TOP SUPPLIERS BY RELIABILITY
# ============================================================

def get_top_reliable_suppliers(
    limit: int = 10,
) -> list[dict]:
    """
    Return suppliers with the highest reliability scores.
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
        ORDER BY reliability_score DESC
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
# GET SUPPLIERS WITH HIGH DELIVERY DELAYS
# ============================================================

def get_high_delay_suppliers(
    minimum_delay: float = 5.0,
    limit: int = 20,
) -> list[dict]:
    """
    Return suppliers whose average delivery delay
    is greater than or equal to the specified threshold.
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
        ORDER BY average_delay_days DESC
        LIMIT ?
    """

    rows = connection.execute(
        query,
        (minimum_delay, limit),
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]