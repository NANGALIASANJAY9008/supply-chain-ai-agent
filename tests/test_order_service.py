from app.services.order_service import (
    get_order_by_id,
    get_orders_by_product,
    get_orders_by_supplier,
    get_active_orders,
    get_order_statistics,
)


# ============================================================
# ORDER LOOKUP
# ============================================================

def test_order_lookup():

    order_id = "O000500001"

    result = get_order_by_id(
        order_id
    )

    assert result is not None

    assert result["order_id"] == order_id

    assert "product_id" in result
    assert "product_name" in result
    assert "supplier_id" in result
    assert "supplier_name" in result
    assert "quantity" in result
    assert "total_value" in result
    assert "status" in result


# ============================================================
# ORDER NOT FOUND
# ============================================================

def test_order_not_found():

    result = get_order_by_id(
        "O999999999"
    )

    assert result is None


# ============================================================
# PRODUCT ORDERS
# ============================================================

def test_orders_by_product():

    results = get_orders_by_product(
        "P0084729",
        limit=10,
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) <= 10

    for order in results:

        assert (
            order["product_id"]
            == "P0084729"
        )


# ============================================================
# SUPPLIER ORDERS
# ============================================================

def test_orders_by_supplier():

    results = get_orders_by_supplier(
        "S003821",
        limit=10,
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) <= 10

    for order in results:

        assert (
            order["supplier_id"]
            == "S003821"
        )


# ============================================================
# ACTIVE ORDERS
# ============================================================

def test_active_orders():

    results = get_active_orders(
        limit=10
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) <= 10

    for order in results:

        assert order["status"] in [
            "Pending",
            "In Transit",
        ]


# ============================================================
# ORDER STATISTICS
# ============================================================

def test_order_statistics():

    result = get_order_statistics()

    assert isinstance(
        result,
        dict,
    )

    assert result["total_orders"] == 1_000_000

    assert result["total_quantity"] is not None

    assert result["total_order_value"] is not None

    assert result["pending_orders"] is not None

    assert result["in_transit_orders"] is not None

    assert result["delivered_orders"] is not None

    assert result["delivered_late_orders"] is not None