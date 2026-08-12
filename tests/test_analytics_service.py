from app.services.analytics_service import (
    get_low_stock_with_incoming_orders,
    get_supplier_risk_analysis,
    get_product_order_summary,
)


# ============================================================
# LOW STOCK + ACTIVE ORDERS
# ============================================================

def test_low_stock_with_incoming_orders():

    results = get_low_stock_with_incoming_orders(
        limit=10
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) <= 10

    for product in results:

        assert (
            product["available_stock"]
            < product["reorder_level"]
        )

        assert (
            product["active_order_count"]
            >= 0
        )

        assert (
            product["active_order_quantity"]
            >= 0
        )


# ============================================================
# SUPPLIER RISK
# ============================================================

def test_supplier_risk_analysis():

    results = get_supplier_risk_analysis(
        minimum_delay=5.0,
        maximum_reliability=80.0,
        limit=10,
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) <= 10

    for supplier in results:

        assert (
            supplier["average_delay_days"]
            >= 5.0
        )

        assert (
            supplier["reliability_score"]
            <= 80.0
        )


# ============================================================
# PRODUCT ORDER SUMMARY
# ============================================================

def test_product_order_summary():

    result = get_product_order_summary(
        "P0084729"
    )

    assert result is not None

    assert (
        result["product_id"]
        == "P0084729"
    )

    assert "product_name" in result

    assert "current_stock" in result

    assert "available_stock" in result

    assert "incoming_stock" in result

    assert "total_orders" in result

    assert "total_order_quantity" in result

    assert "total_order_value" in result

    assert "pending_orders" in result

    assert "in_transit_orders" in result


# ============================================================
# PRODUCT NOT FOUND
# ============================================================

def test_product_order_summary_not_found():

    result = get_product_order_summary(
        "P9999999"
    )

    assert result is None