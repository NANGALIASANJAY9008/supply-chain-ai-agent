from app.services.supplier_service import (
    get_supplier_by_id,
    get_top_reliable_suppliers,
    get_high_delay_suppliers,
)


def test_supplier_lookup():

    supplier_id = "S003821"

    result = get_supplier_by_id(
        supplier_id
    )

    assert result is not None

    assert result["supplier_id"] == supplier_id

    assert "supplier_name" in result
    assert "location" in result
    assert "lead_time_days" in result
    assert "reliability_score" in result
    assert "average_delay_days" in result


def test_supplier_not_found():

    result = get_supplier_by_id(
        "S999999"
    )

    assert result is None


def test_top_reliable_suppliers():

    results = get_top_reliable_suppliers(
        limit=10
    )

    assert isinstance(results, list)

    assert len(results) <= 10

    for supplier in results:
        assert "reliability_score" in supplier


def test_high_delay_suppliers():

    results = get_high_delay_suppliers(
        minimum_delay=5.0,
        limit=20,
    )

    assert isinstance(results, list)

    assert len(results) <= 20

    for supplier in results:

        assert (
            supplier["average_delay_days"]
            >= 5.0
        )