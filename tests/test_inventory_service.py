from app.services.inventory_service import (
    get_inventory_by_product,
    get_low_stock_products,
)
def test_low_stock_products():

    results = get_low_stock_products(
        limit=10
    )

    assert isinstance(results, list)

    assert len(results) <= 10

    for product in results:

        assert (
            product["available_stock"]
            < product["reorder_level"]
        )

def test_inventory_lookup():

    product_id = "P0084729"

    result = get_inventory_by_product(
        product_id
    )

    assert result is not None

    assert result["product_id"] == product_id

    assert "product_name" in result

    assert "current_stock" in result

    assert "reserved_stock" in result

    assert "available_stock" in result

    assert "incoming_stock" in result

    assert "reorder_level" in result

    assert "stock_status" in result


def test_inventory_product_not_found():

    result = get_inventory_by_product(
        "P9999999"
    )

    assert result is None

def test_available_stock_calculation():

    result = get_inventory_by_product(
        "P0084729"
    )

    assert result is not None

    expected_available_stock = (
        result["current_stock"]
        - result["reserved_stock"]
    )

    assert (
        result["available_stock"]
        == expected_available_stock
    )