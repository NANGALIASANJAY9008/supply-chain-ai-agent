from app.agents.dynamic_sql import (
    execute_dynamic_query,
)


def test_average_supplier_delay():

    plan = {
        "operation": "AVG",
        "table": "suppliers",
        "field": "average_delay_days",
        "conditions": [],
        "group_by": None,
    }

    result = execute_dynamic_query(
        plan
    )

    assert (
        result["row_count"]
        == 1
    )

    assert (
        result["results"][0]
        ["result"]
        is not None
    )


def test_pending_order_count():

    plan = {
        "operation": "COUNT",
        "table": "orders",
        "field": "*",
        "conditions": [
            {
                "field": "status",
                "operator": "=",
                "value": "Pending",
            }
        ],
        "group_by": None,
    }

    result = execute_dynamic_query(
        plan
    )

    assert (
        result["row_count"]
        == 1
    )

    count = (
        result["results"][0]
        ["COUNT(*)"]
    )

    assert count >= 0


def test_total_order_value():

    plan = {
        "operation": "SUM",
        "table": "orders",
        "field": "total_value",
        "conditions": [],
        "group_by": None,
    }

    result = execute_dynamic_query(
        plan
    )

    assert (
        result["row_count"]
        == 1
    )

    total = (
        result["results"][0]
        ["result"]
    )

    assert total is not None
    assert total >= 0


def test_average_reliability():

    plan = {
        "operation": "AVG",
        "table": "suppliers",
        "field": "reliability_score",
        "conditions": [],
        "group_by": None,
    }

    result = execute_dynamic_query(
        plan
    )

    assert (
        result["row_count"]
        == 1
    )

    average = (
        result["results"][0]
        ["result"]
    )

    assert average is not None


def test_product_price_filter():

    plan = {
        "operation": "FILTER",
        "table": "products",
        "field": "*",
        "conditions": [
            {
                "field": "unit_price",
                "operator": ">",
                "value": 50000,
            }
        ],
        "group_by": None,
    }

    result = execute_dynamic_query(
        plan
    )

    assert (
        result["row_count"]
        >= 0
    )

    for product in result[
        "results"
    ]:

        assert (
            product["unit_price"]
            > 50000
        )