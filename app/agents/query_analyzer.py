import json

from app.rag.llm_service import (
    client,
    MODEL_NAME,
)


# ============================================================
# QUERY ANALYZER
# ============================================================

def analyze_query(
    question: str,
) -> dict:
    """
    Convert a natural-language supply-chain question
    into a structured intent.

    Groq determines the intent.
    It does NOT generate SQL.
    """

    system_prompt = """
You are a query analyzer for a Supply Chain Q&A system.

Convert the user's natural-language question into
structured JSON.

You MUST choose exactly one intent from:

PRODUCT_LOOKUP
INVENTORY_LOOKUP
PRODUCT_ORDERS
SUPPLIER_LOOKUP
SUPPLIER_RISK
LOW_STOCK
TOP_RELIABLE_SUPPLIERS
ACTIVE_ORDERS
ORDER_LOOKUP
UNKNOWN

Definitions:

PRODUCT_LOOKUP:
Questions asking for information about a specific
product, especially when a product_id is provided.

Examples:
- What is P0084729?
- Tell me about P0084729.
- What is the price of P0084729?
- Which warehouse contains P0084729?
- What is the reorder level of P0084729?

Do NOT use PRODUCT_LOOKUP for questions asking
which products satisfy a condition or threshold.

Examples that should NOT be PRODUCT_LOOKUP:
- Which products have a unit price above 50000?
- Which products cost more than 50000?
- Which products have a reorder level below 100?
- Show products in a particular category.



INVENTORY_LOOKUP:
Questions about current stock, available stock,
reserved stock, incoming stock, inventory status,
whether there is enough stock, whether inventory
is sufficient, whether a product needs more stock,
or whether a product has enough units to fulfill demand.

Examples:

"What is the current stock of P0084729?"
"How much inventory is available for P0084729?"
"Do we have enough P0084729?"
"Is there enough stock of P0084729?"
"Can we fulfill demand for P0084729?"
"Does P0084729 have sufficient inventory?"

PRODUCT_ORDERS:
Questions about orders associated with a specific product.

SUPPLIER_LOOKUP:
Questions about a specific supplier.

SUPPLIER_RISK:
Questions about supplier delays, supplier reliability,
supplier performance or risky suppliers.

LOW_STOCK:
Questions asking which products are low in stock
or need replenishment.

TOP_RELIABLE_SUPPLIERS:
Questions asking for the best, most reliable,
or highest-performing suppliers.

ACTIVE_ORDERS:
Questions about pending, active, processing,
or currently open orders.

ORDER_LOOKUP:
Questions about a specific order.

DYNAMIC QUERY RULE:

If the question asks to find, filter, compare, rank,
aggregate, count, sum, average, minimum, maximum,
or group database records using a condition or threshold,
and it does not clearly match one of the supported
specific intents above, classify it as UNKNOWN.

UNKNOWN questions will be handled by a separate
safe Dynamic Query Planner.

Examples:

"What is the total value of all orders?"
→ UNKNOWN

"Which products have a unit price above 50000?"
→ UNKNOWN

"Which suppliers have reliability above 90?"
→ UNKNOWN

"What is the average supplier delay?"
→ SUPPLIER_RISK if the question is specifically
about supplier delay/risk.

"Tell me about supplier S003821."
→ SUPPLIER_LOOKUP

UNKNOWN:
Use when the question does not match any supported
database operation.

Extract these entities when present:

product_id
supplier_id
order_id

If an entity is not present, return null.

Return ONLY valid JSON.

Example:

{
    "intent": "INVENTORY_LOOKUP",
    "product_id": "P0084729",
    "supplier_id": null,
    "order_id": null
}
"""

    user_prompt = f"""
Analyze this supply-chain question:

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
    # CLEAN GROQ MARKDOWN JSON
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

        result = json.loads(content)

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Query analyzer returned invalid JSON: "
            f"{content}"
        ) from exc

    # ========================================================
    # VALIDATE INTENT
    # ========================================================

    valid_intents = {
        "PRODUCT_LOOKUP",
        "INVENTORY_LOOKUP",
        "PRODUCT_ORDERS",
        "SUPPLIER_LOOKUP",
        "SUPPLIER_RISK",
        "LOW_STOCK",
        "TOP_RELIABLE_SUPPLIERS",
        "ACTIVE_ORDERS",
        "ORDER_LOOKUP",
        "UNKNOWN",
    }

    if result.get("intent") not in valid_intents:

        raise ValueError(
            f"Invalid intent: "
            f"{result.get('intent')}"
        )

    return result