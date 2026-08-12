import pytest

from app.agents.query_compiler import (
    compile_query,
)


def test_average_supplier_delay():

    plan = {
        "operation": "AVG",
        "table": "suppliers",
        "field": "average_delay_days",
        "conditions": [],
        "group_by": None,
    }

    sql, params = compile_query(
        plan
    )

    assert (
    sql
    == 'SELECT AVG("average_delay_days") '
       'AS "result" '
       'FROM "suppliers"'
    )

    assert params == []


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

    sql, params = compile_query(
        plan
    )

    assert (
        sql
        == 'SELECT COUNT(*) FROM "orders" '
           'WHERE "status" = ?'
    )

    assert params == [
        "Pending"
    ]


def test_total_order_value():

    plan = {
        "operation": "SUM",
        "table": "orders",
        "field": "total_value",
        "conditions": [],
        "group_by": None,
    }

    sql, params = compile_query(
        plan
    )

    assert (
    sql
    == 'SELECT SUM("total_value") '
       'AS "result" '
       'FROM "orders"'
    )

    assert params == []


def test_filter_products():

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

    sql, params = compile_query(
        plan
    )

    assert (
        sql
        == 'SELECT * FROM "products" '
           'WHERE "unit_price" > ?'
    )

    assert params == [
        50000
    ]


def test_group_orders_by_status():

    plan = {
        "operation": "GROUP_BY",
        "table": "orders",
        "field": "order_id",
        "conditions": [],
        "group_by": "status",
    }

    sql, params = compile_query(
        plan
    )

    assert (
        sql
        == 'SELECT "status", COUNT("order_id") '
           'FROM "orders" '
           'GROUP BY "status"'
    )

    assert params == []


def test_invalid_table():

    plan = {
        "operation": "COUNT",
        "table": "users",
        "field": "*",
        "conditions": [],
        "group_by": None,
    }

    with pytest.raises(
        ValueError
    ):

        compile_query(
            plan
        )


def test_invalid_field():

    plan = {
        "operation": "AVG",
        "table": "suppliers",
        "field": "password",
        "conditions": [],
        "group_by": None,
    }

    with pytest.raises(
        ValueError
    ):

        compile_query(
            plan
        )


def test_invalid_operator():

    plan = {
        "operation": "FILTER",
        "table": "products",
        "field": "*",
        "conditions": [
            {
                "field": "unit_price",
                "operator": "DROP",
                "value": 50000,
            }
        ],
        "group_by": None,
    }

    with pytest.raises(
        ValueError
    ):

        compile_query(
            plan
        )


def test_sql_injection_value_is_parameterized():

    plan = {
        "operation": "FILTER",
        "table": "products",
        "field": "*",
        "conditions": [
            {
                "field": "category",
                "operator": "=",
                "value": "'; DROP TABLE products; --",
            }
        ],
        "group_by": None,
    }

    sql, params = compile_query(
        plan
    )

    assert "DROP TABLE" not in sql

    assert params == [
        "'; DROP TABLE products; --"
    ]