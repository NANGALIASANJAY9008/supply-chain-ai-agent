import json

from app.rag.llm_service import (
    client,
    MODEL_NAME,
)


# ============================================================
# ALLOWED DATABASE SCHEMA
# ============================================================

ALLOWED_TABLES = {
    "products",
    "suppliers",
    "inventory",
    "orders",
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


ALLOWED_PRODUCT_FIELDS = {
    "product_id",
    "product_name",
    "category",
    "unit_price",
    "reorder_level",
    "warehouse",
}


ALLOWED_SUPPLIER_FIELDS = {
    "supplier_id",
    "supplier_name",
    "location",
    "lead_time_days",
    "reliability_score",
    "average_delay_days",
}


ALLOWED_INVENTORY_FIELDS = {
    "product_id",
    "warehouse",
    "current_stock",
    "reserved_stock",
    "incoming_stock",
    "reorder_level",
}


ALLOWED_ORDER_FIELDS = {
    "order_id",
    "product_id",
    "supplier_id",
    "order_date",
    "quantity",
    "expected_delivery_date",
    "actual_delivery_date",
    "total_value",
    "status",
}


# ============================================================
# QUERY PLANNER
# ============================================================

def plan_query(
    question: str,
) -> dict:
    """
    Convert a complex natural-language supply-chain
    question into a structured query plan.

    Groq creates the plan.

    Python validates the plan.

    Groq NEVER generates executable SQL.
    """

    system_prompt = """
You are a Supply Chain Query Planner.

Your job is to convert a natural-language
supply-chain question into a SAFE structured
JSON query plan.

You MUST NOT generate SQL.

Allowed tables:

products
suppliers
inventory
orders

Allowed operations:

COUNT
SUM
AVG
MIN
MAX
FILTER
GROUP_BY

Return ONLY valid JSON.

The JSON must follow this structure:

{
    "operation": "AVG",
    "table": "suppliers",
    "field": "average_delay_days",
    "conditions": [],
    "group_by": null
}

Examples:

Question:
"What is the average supplier delay?"

Return:

{
    "operation": "AVG",
    "table": "suppliers",
    "field": "average_delay_days",
    "conditions": [],
    "group_by": null
}

Question:
"How many pending orders are there?"

Return:

{
    "operation": "COUNT",
    "table": "orders",
    "field": "*",
    "conditions": [
        {
            "field": "status",
            "operator": "=",
            "value": "Pending"
        }
    ],
    "group_by": null
}

Question:
"What is the total order value?"

Return:

{
    "operation": "SUM",
    "table": "orders",
    "field": "total_value",
    "conditions": [],
    "group_by": null
}

Question:
"What is the average reliability score of suppliers?"

Return:

{
    "operation": "AVG",
    "table": "suppliers",
    "field": "reliability_score",
    "conditions": [],
    "group_by": null
}

Question:
"How many orders are there for each status?"

Return:

{
    "operation": "GROUP_BY",
    "table": "orders",
    "field": "order_id",
    "conditions": [],
    "group_by": "status"
}

Question:
"Which products have a unit price above 50000?"

Return:

{
    "operation": "FILTER",
    "table": "products",
    "field": "*",
    "conditions": [
        {
            "field": "unit_price",
            "operator": ">",
            "value": 50000
        }
    ],
    "group_by": null
}

Allowed operators:

=
!=
>
<
>=
<=

For conditions, use only fields belonging
to the selected table.

Do not invent table names.

Do not invent field names.

Do not generate SQL.

Return ONLY JSON.
"""

    user_prompt = f"""
Create a safe structured query plan
for this supply-chain question:

{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0,
    )

    content = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    # ========================================================
    # CLEAN MARKDOWN JSON
    # ========================================================

    if content.startswith("```json"):

        content = content[
            len("```json"):
        ].strip()

    elif content.startswith("```"):

        content = content[
            len("```"):
        ].strip()

    if content.endswith("```"):

        content = content[
            :-len("```")
        ].strip()

    # ========================================================
    # PARSE JSON
    # ========================================================

    try:

        plan = json.loads(
            content
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Query planner returned invalid JSON: "
            f"{content}"
        ) from exc

    # ========================================================
    # VALIDATE PLAN
    # ========================================================

    validate_query_plan(
        plan
    )

    return plan


# ============================================================
# QUERY PLAN VALIDATION
# ============================================================

def validate_query_plan(
    plan: dict,
) -> None:
    """
    Validate a query plan before it can be
    converted into SQL.
    """

    if not isinstance(
        plan,
        dict,
    ):

        raise ValueError(
            "Query plan must be a dictionary."
        )

    operation = plan.get(
        "operation"
    )

    table = plan.get(
        "table"
    )

    field = plan.get(
        "field"
    )

    conditions = plan.get(
        "conditions",
        [],
    )

    group_by = plan.get(
        "group_by"
    )

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

    # --------------------------------------------------------
    # TABLE FIELDS
    # --------------------------------------------------------

    table_fields = {

        "products":
            ALLOWED_PRODUCT_FIELDS,

        "suppliers":
            ALLOWED_SUPPLIER_FIELDS,

        "inventory":
            ALLOWED_INVENTORY_FIELDS,

        "orders":
            ALLOWED_ORDER_FIELDS,
    }

    allowed_fields = table_fields[
        table
    ]

    # --------------------------------------------------------
    # FIELD
    # --------------------------------------------------------

    if field != "*":

        if field not in allowed_fields:

            raise ValueError(
                f"Unsupported field '{field}' "
                f"for table '{table}'."
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

    if not isinstance(
        conditions,
        list,
    ):

        raise ValueError(
            "Conditions must be a list."
        )

    allowed_operators = {
        "=",
        "!=",
        ">",
        "<",
        ">=",
        "<=",
    }

    for condition in conditions:

        if not isinstance(
            condition,
            dict,
        ):

            raise ValueError(
                "Each condition must be "
                "a dictionary."
            )

        condition_field = (
            condition.get("field")
        )

        operator = (
            condition.get("operator")
        )

        if condition_field not in allowed_fields:

            raise ValueError(
                f"Unsupported condition field: "
                f"{condition_field}"
            )

        if operator not in allowed_operators:

            raise ValueError(
                f"Unsupported operator: "
                f"{operator}"
            )

        if "value" not in condition:

            raise ValueError(
                "Condition is missing "
                "a value."
            )