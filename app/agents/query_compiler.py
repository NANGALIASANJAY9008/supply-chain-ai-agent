# ============================================================
# SAFE QUERY COMPILER
# ============================================================

ALLOWED_TABLES = {
    "products",
    "suppliers",
    "inventory",
    "orders",
}


ALLOWED_FIELDS = {

    "products": {
        "product_id",
        "product_name",
        "category",
        "unit_price",
        "reorder_level",
        "warehouse",
    },

    "suppliers": {
        "supplier_id",
        "supplier_name",
        "location",
        "lead_time_days",
        "reliability_score",
        "average_delay_days",
    },

    "inventory": {
        "product_id",
        "warehouse",
        "current_stock",
        "reserved_stock",
        "incoming_stock",
        "reorder_level",
    },

    "orders": {
        "order_id",
        "product_id",
        "supplier_id",
        "order_date",
        "quantity",
        "expected_delivery_date",
        "actual_delivery_date",
        "total_value",
        "status",
    },
}


ALLOWED_OPERATIONS = {
    "COUNT",
    "SUM",
    "AVG",
    "MIN",
    "MAX",
    "FILTER",
    "GROUP_BY",
}


ALLOWED_OPERATORS = {
    "=": "=",
    "!=": "!=",
    ">": ">",
    "<": "<",
    ">=": ">=",
    "<=": "<=",
}


# ============================================================
# VALIDATE PLAN
# ============================================================

def validate_plan(plan: dict) -> None:

    if not isinstance(plan, dict):
        raise ValueError(
            "Query plan must be a dictionary."
        )

    operation = plan.get("operation")
    table = plan.get("table")
    field = plan.get("field")
    conditions = plan.get("conditions", [])
    group_by = plan.get("group_by")

    # --------------------------------------------------------
    # OPERATION
    # --------------------------------------------------------

    if operation not in ALLOWED_OPERATIONS:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    if table not in ALLOWED_TABLES:
        raise ValueError(
            f"Unsupported table: {table}"
        )

    allowed_fields = ALLOWED_FIELDS[table]

    # --------------------------------------------------------
    # FIELD
    # --------------------------------------------------------

    if field != "*" and field not in allowed_fields:
        raise ValueError(
            f"Unsupported field: {field}"
        )

    # --------------------------------------------------------
    # GROUP BY
    # --------------------------------------------------------

    if group_by is not None:

        if group_by not in allowed_fields:
            raise ValueError(
                f"Unsupported GROUP BY field: "
                f"{group_by}"
            )

    # --------------------------------------------------------
    # CONDITIONS
    # --------------------------------------------------------

    if not isinstance(conditions, list):
        raise ValueError(
            "conditions must be a list."
        )

    for condition in conditions:

        if not isinstance(condition, dict):
            raise ValueError(
                "Each condition must be a dictionary."
            )

        condition_field = condition.get(
            "field"
        )

        operator = condition.get(
            "operator"
        )

        if condition_field not in allowed_fields:
            raise ValueError(
                f"Unsupported condition field: "
                f"{condition_field}"
            )

        if operator not in ALLOWED_OPERATORS:
            raise ValueError(
                f"Unsupported operator: "
                f"{operator}"
            )

        if "value" not in condition:
            raise ValueError(
                "Condition must contain a value."
            )


# ============================================================
# SAFE IDENTIFIER
# ============================================================

def quote_identifier(
    identifier: str,
) -> str:

    if not isinstance(identifier, str):
        raise ValueError(
            "SQL identifier must be a string."
        )

    if (
        identifier.startswith(" ")
        or identifier.endswith(" ")
    ):
        raise ValueError(
            "Invalid SQL identifier."
        )

    return f'"{identifier}"'


# ============================================================
# WHERE CLAUSE
# ============================================================

def build_where_clause(
    conditions: list,
):

    if not conditions:
        return "", []

    clauses = []
    parameters = []

    for condition in conditions:

        field = condition["field"]

        operator = ALLOWED_OPERATORS[
            condition["operator"]
        ]

        value = condition["value"]

        clauses.append(
            f'{quote_identifier(field)} '
            f'{operator} ?'
        )

        parameters.append(
            value
        )

    return (
        " WHERE "
        + " AND ".join(clauses),
        parameters,
    )


# ============================================================
# COMPILE QUERY
# ============================================================

def compile_query(
    plan: dict,
):

    validate_plan(plan)

    operation = plan["operation"]
    table = plan["table"]
    field = plan["field"]

    conditions = plan.get(
        "conditions",
        [],
    )

    group_by = plan.get(
        "group_by"
    )

    table_sql = quote_identifier(
        table
    )

    where_sql, parameters = (
        build_where_clause(
            conditions
        )
    )

    # ========================================================
    # COUNT
    # ========================================================

    if operation == "COUNT":

        if field == "*":

            select_sql = "COUNT(*)"

        else:

            field_sql = quote_identifier(
                field
            )

            select_sql = (
                f"COUNT({field_sql})"
            )

        sql = (
            f"SELECT {select_sql} "
            f"FROM {table_sql}"
            f"{where_sql}"
        )

        return sql, parameters

    # ========================================================
    # SUM
    # ========================================================

    if operation == "SUM":

        if field == "*":
            raise ValueError(
                "SUM requires a specific field."
            )

        field_sql = quote_identifier(
            field
        )

        sql = (
            f'SELECT SUM({field_sql}) '
            f'AS "result" '
            f'FROM {table_sql}'
            f'{where_sql}'
        )

        return sql, parameters

    # ========================================================
    # AVG
    # ========================================================

    if operation == "AVG":

        if field == "*":
            raise ValueError(
                "AVG requires a specific field."
            )

        field_sql = quote_identifier(
            field
        )

        sql = (
            f'SELECT AVG({field_sql}) '
            f'AS "result" '
            f'FROM {table_sql}'
            f'{where_sql}'
        )

        return sql, parameters

    # ========================================================
    # MIN
    # ========================================================

    if operation == "MIN":

        if field == "*":
            raise ValueError(
                "MIN requires a specific field."
            )

        field_sql = quote_identifier(
            field
        )

        sql = (
            f'SELECT MIN({field_sql}) '
            f'AS "result" '
            f'FROM {table_sql}'
            f'{where_sql}'
        )

        return sql, parameters

    # ========================================================
    # MAX
    # ========================================================

    if operation == "MAX":

        if field == "*":
            raise ValueError(
                "MAX requires a specific field."
            )

        field_sql = quote_identifier(
            field
        )

        sql = (
            f'SELECT MAX({field_sql}) '
            f'AS "result" '
            f'FROM {table_sql}'
            f'{where_sql}'
        )

        return sql, parameters

    # ========================================================
    # FILTER
    # ========================================================

    if operation == "FILTER":

        if field == "*":

            select_sql = "*"

        else:

            select_sql = quote_identifier(
                field
            )

        sql = (
            f"SELECT {select_sql} "
            f"FROM {table_sql}"
            f"{where_sql}"
        )

        return sql, parameters

    # ========================================================
    # GROUP BY
    # ========================================================

    if operation == "GROUP_BY":

        if group_by is None:
            raise ValueError(
                "GROUP_BY requires group_by."
            )

        group_sql = quote_identifier(
            group_by
        )

        if field == "*":

            count_sql = "COUNT(*)"

        else:

            field_sql = quote_identifier(
                field
            )

            count_sql = (
                f"COUNT({field_sql})"
            )

        sql = (
            f'SELECT {group_sql}, '
            f'{count_sql} '
            f'FROM {table_sql}'
            f'{where_sql} '
            f'GROUP BY {group_sql}'
        )

        return sql, parameters

    raise ValueError(
        f"Unsupported operation: {operation}"
    )