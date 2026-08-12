import json

from app.rag.llm_service import client, MODEL_NAME


# ============================================================
# ROUTE USER QUESTION
# ============================================================

def route_question(
    question: str,
) -> dict:
    """
    Decide whether a user question requires:

    SQL  -> structured database information
    RAG  -> document/policy information
    BOTH -> database + document information
    """

    system_prompt = """
You are a routing agent for a Supply Chain Q&A system.

Classify the user's question into exactly one category:

SQL
RAG
BOTH

Use these rules.

SQL:
Use SQL when the question requires structured
business data from the supply-chain database.

Examples:
- inventory of a product
- current stock
- available stock
- orders
- pending orders
- supplier reliability
- supplier delays
- order statistics
- product information
- low stock products

RAG:
Use RAG when the question asks about policies,
procedures, rules, guidelines, or information
contained in supply-chain documents.

Examples:
- procurement policy
- supplier policy
- inventory policy
- return policy
- delivery policy
- emergency procurement rules
- supplier evaluation rules

BOTH:
Use BOTH when the question requires actual
database information AND policy/document information.

Examples:
- A product is low in stock. What does policy recommend?
- Supplier S003821 has poor reliability. What does supplier policy say?
- An order is delayed. What does the delivery policy recommend?

Return ONLY valid JSON in this format:

{
    "route": "SQL"
}

or

{
    "route": "RAG"
}

or

{
    "route": "BOTH"
}
"""

    user_prompt = f"""
Classify this supply-chain question:

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

    content = response.choices[0].message.content.strip()

    try:
        result = json.loads(content)

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Router returned invalid JSON: {content}"
        ) from exc

    route = result.get("route")

    if route not in {
        "SQL",
        "RAG",
        "BOTH",
    }:

        raise ValueError(
            f"Invalid route returned: {route}"
        )

    return result