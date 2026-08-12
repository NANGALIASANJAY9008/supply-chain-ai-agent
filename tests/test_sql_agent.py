from app.agents.sql_agent import (
    product_lookup,
    inventory_lookup,
    supplier_lookup,
    order_lookup,
    get_low_stock_products,
    get_top_reliable_suppliers,
    get_active_orders,
    orders_by_product,
)


TEST_PRODUCT = "P0084729"
TEST_SUPPLIER = "S003821"
TEST_ORDER = "O000500001"


def test_product_lookup():

    result = product_lookup(
        TEST_PRODUCT
    )

    assert result is not None

    assert (
        result["product_id"]
        == TEST_PRODUCT
    )

    assert (
        result["product_name"]
        == "Pro Module 84729"
    )


def test_inventory_lookup():

    result = inventory_lookup(
        TEST_PRODUCT
    )

    assert result is not None

    assert (
        result["product_id"]
        == TEST_PRODUCT
    )

    assert "available_stock" in result

    assert (
        result["available_stock"]
        ==
        result["current_stock"]
        - result["reserved_stock"]
    )


def test_supplier_lookup():

    result = supplier_lookup(
        TEST_SUPPLIER
    )

    assert result is not None

    assert (
        result["supplier_id"]
        == TEST_SUPPLIER
    )


def test_order_lookup():

    result = order_lookup(
        TEST_ORDER
    )

    assert result is not None

    assert (
        result["order_id"]
        == TEST_ORDER
    )


def test_low_stock_products():

    results = (
        get_low_stock_products()
    )

    assert isinstance(
        results,
        list,
    )


def test_top_reliable_suppliers():

    results = (
        get_top_reliable_suppliers()
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) <= 5


def test_active_orders():

    results = (
        get_active_orders()
    )

    assert isinstance(
        results,
        list,
    )


def test_orders_by_product():

    results = orders_by_product(
        TEST_PRODUCT
    )

    assert isinstance(
        results,
        list,
    )