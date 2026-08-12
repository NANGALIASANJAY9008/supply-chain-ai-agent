import groq
from app.agents.router import route_question

from app.agents.query_analyzer import (
    analyze_query,
)

from app.agents.sql_agent import (
    extract_product_id,
    extract_supplier_id,
    extract_order_id,
    product_lookup,
    inventory_lookup,
    supplier_lookup,
    order_lookup,
    get_low_stock_products,
    get_top_reliable_suppliers,
    get_active_orders,
    get_active_order_summary,
    get_pending_order_count,
    orders_by_product,
    get_high_delay_suppliers,
)

from app.agents.errors import (
    InvalidQuestionError,
    QueryPlanningError,
    QueryExecutionError,
    LLMServiceError,
)

from app.agents.query_planner import (
    plan_query,
)

from app.agents.dynamic_sql import (
    execute_dynamic_query,
)


from app.rag.llm_service import (
    client,
    MODEL_NAME,
)


# ============================================================
# SQL QUESTION EXECUTOR
# ============================================================

def execute_sql_question(
    question: str,
) -> dict:
    """
    Execute a controlled database operation
    based on the structured query intent.

    Known intents use existing safe SQL functions.

    Unknown/complex database questions are passed
    to the Dynamic Query Planner.
    """

    # ========================================================
    # ANALYZE NATURAL-LANGUAGE QUESTION
    # ========================================================

    analysis = analyze_query(
        question
    )

    intent = analysis["intent"]

    product_id = (
        analysis.get("product_id")
    )

    supplier_id = (
        analysis.get("supplier_id")
    )

    order_id = (
        analysis.get("order_id")
    )

    # ========================================================
    # ENTITY FALLBACK
    # ========================================================

    if product_id is None:

        product_id = extract_product_id(
            question
        )

    if supplier_id is None:

        supplier_id = extract_supplier_id(
            question
        )

    if order_id is None:

        order_id = extract_order_id(
            question
        )

    # ========================================================
    # INVENTORY SAFETY FALLBACK
    # ========================================================

    question_lower = question.lower()

    inventory_phrases = [
        "enough stock",
        "enough inventory",
        "enough units",
        "sufficient stock",
        "sufficient inventory",
        "current stock",
        "available stock",
        "available inventory",
        "inventory level",
        "stock level",
        "do we have enough",
        "is there enough",
        "can we fulfill",
        "can we fulfil",
        "fulfill demand",
        "fulfil demand",
    ]

    if (
        product_id
        and any(
            phrase in question_lower
            for phrase in inventory_phrases
        )
    ):

        intent = "INVENTORY_LOOKUP"

    # ========================================================
    # PRODUCT LOOKUP
    # ========================================================

    if intent == "PRODUCT_LOOKUP":

        if not product_id:

            return {
                "type": "product",
                "message": (
                    "A product ID is required "
                    "for this lookup."
                ),
            }

        product = product_lookup(
            product_id
        )

        return {
            "type": "product",
            "product": product,
        }

    # ========================================================
    # INVENTORY LOOKUP
    # ========================================================

    if intent == "INVENTORY_LOOKUP":

        if not product_id:

            return {
                "type": "inventory",
                "message": (
                    "A product ID is required "
                    "for this inventory lookup."
                ),
            }

        product = product_lookup(
            product_id
        )

        inventory = inventory_lookup(
            product_id
        )

        return {
            "type": "inventory",
            "product": product,
            "inventory": inventory,
        }

    # ========================================================
    # PRODUCT ORDERS
    # ========================================================

    if intent == "PRODUCT_ORDERS":

        if not product_id:

            return {
                "type": "orders",
                "message": (
                    "A product ID is required "
                    "for this order lookup."
                ),
            }

        orders = orders_by_product(
            product_id
        )

        return {
            "type": "orders",
            "product_id": product_id,
            "orders": orders,
        }

    # ========================================================
    # SUPPLIER LOOKUP
    # ========================================================

    if intent == "SUPPLIER_LOOKUP":

        if not supplier_id:

            return {
                "type": "supplier",
                "message": (
                    "A supplier ID is required "
                    "for this lookup."
                ),
            }

        supplier = supplier_lookup(
            supplier_id
        )

        return {
            "type": "supplier",
            "supplier": supplier,
        }

    # ========================================================
    # SUPPLIER RISK
    # ========================================================

    if intent == "SUPPLIER_RISK":

        suppliers = (
            get_high_delay_suppliers()
        )

        return {
            "type": "supplier_risk",
            "suppliers": suppliers,
        }

    # ========================================================
    # LOW STOCK
    # ========================================================

    if intent == "LOW_STOCK":

        products = (
            get_low_stock_products()
        )

        return {
            "type": "low_stock",
            "products": products,
        }

    # ========================================================
    # TOP RELIABLE SUPPLIERS
    # ========================================================

    if intent == "TOP_RELIABLE_SUPPLIERS":

        suppliers = (
            get_top_reliable_suppliers()
        )

        return {
            "type": "reliable_suppliers",
            "suppliers": suppliers,
        }

    # ========================================================
    # ACTIVE ORDERS
    # ========================================================

    if intent == "ACTIVE_ORDERS":

        orders = get_active_orders()

        summary = get_active_order_summary()

        pending_count = (
            get_pending_order_count()
        )

        return {
            "type": "active_orders",
            "orders": orders,
            "summary": summary,
            "pending_order_count": pending_count,
        }

    # ========================================================
    # ORDER LOOKUP
    # ========================================================

    if intent == "ORDER_LOOKUP":

        if not order_id:

            return {
                "type": "order",
                "message": (
                    "An order ID is required "
                    "for this lookup."
                ),
            }

        order = order_lookup(
            order_id
        )

        return {
            "type": "order",
            "order": order,
        }

    # ========================================================
    # DYNAMIC QUERY FALLBACK
    # ========================================================

    if intent == "UNKNOWN":

        plan = plan_query(
            question
        )

        dynamic_result = (
            execute_dynamic_query(
                plan
            )
        )

        return {
            "type": "dynamic_sql",
            "plan": plan,
            "data": dynamic_result,
        }

    # ========================================================
    # UNKNOWN
    # ========================================================

    return {
        "type": "unknown",
        "message": (
            "The requested database operation "
            "is not supported."
        ),
    }


# ============================================================
# FINAL ANSWER GENERATOR
# ============================================================

def generate_final_answer(
    question: str,
    sql_data=None,
    rag_data=None,
) -> str:
    """
    Generate a final grounded answer using
    SQL and/or RAG evidence.
    """

    import json

    # ========================================================
    # SQL CONTEXT
    # ========================================================

    if sql_data is not None:

        sql_context = json.dumps(
            sql_data,
            indent=2,
            default=str,
        )

    else:

        sql_context = (
            "No SQL data available."
        )

    # ========================================================
    # RAG CONTEXT
    # ========================================================

    if rag_data is not None:

        rag_context = json.dumps(
            rag_data,
            indent=2,
            default=str,
        )

    else:

        rag_context = (
            "No document context available."
        )

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    system_prompt = """
You are a Supply Chain Q&A Assistant.

You must answer using the supplied evidence.

IMPORTANT RULES:

1. SQL DATA is authoritative for database facts.

2. Never claim that a value is missing if it exists
   in SQL DATA.

3. Never invent numbers.

4. Preserve exact product IDs, supplier IDs,
   order IDs, dates and numerical values.

5. For inventory questions, distinguish carefully
   between:

   current_stock
   reserved_stock
   available_stock
   incoming_stock
   reorder_level

6. If available_stock is provided, use that exact value.

7. If current_stock and reserved_stock are provided,
   available_stock can be verified as:

   current_stock - reserved_stock

8. Do not confuse current_stock with available_stock.

9. For policy questions, use DOCUMENT/RAG DATA.

10. When both SQL DATA and DOCUMENT/RAG DATA are provided,
    combine them carefully.

11. If the evidence genuinely does not contain the requested
    information, clearly say that it is unavailable.

12. Do not say information is unavailable merely because
    the user did not explicitly mention the field.

13. Answer the user's actual question directly.

14. Keep the answer concise and professional.

15. Base factual statements only on the supplied evidence.

16. Never calculate a result that has already been
    calculated by SQL.

17. Never add records that are not present in SQL DATA.

18. Never create additional IDs, dates, quantities,
    statuses or values.

19. When listing database records, keep each record's
    fields together.

20. Never mix fields belonging to different records.

21. If SQL DATA contains a limited list of records,
    do not describe that list as the total database count
    unless an explicit total count is also provided.

22. If SQL DATA contains an explicit count, use that
    count as authoritative.

23. For active or pending orders, distinguish between:
    - returned/displayed orders
    - total pending orders
    - total active orders

24. Do not say "there are 20 pending orders" merely because
    20 orders were returned by a LIMIT query.

25. If pending_order_count is provided, use that exact
    value when answering how many pending orders exist.

26. For dynamic SQL results:

    - Treat the returned SQL data as authoritative.

    - Use the "result" field for aggregate operations
      such as AVG, SUM, MIN and MAX.

    - Do not invent additional records.

    - Do not expose SQL syntax unless the user asks for it.

    - Pay attention to:
      total_row_count,
      row_count,
      truncated,
      max_llm_rows.

    - If truncated is true, clearly explain that only
      a limited number of matching records are displayed.

    - If total_row_count is available, use that value
      when explaining how many records matched.

    - Never claim that the displayed rows represent
      every matching record when truncated is true.

    - Do not invent the records that were not included
      in the evidence.

    - For FILTER queries with many matching records,
      provide the total number of matches and summarize
      the displayed records rather than pretending the
      displayed records are the complete dataset.

    - For aggregate queries such as SUM, AVG, MIN, MAX
      or COUNT, use the aggregate result directly.

    - Do not recalculate aggregate values from a truncated
      list of rows.
"""

    # ========================================================
    # USER PROMPT
    # ========================================================

    user_prompt = f"""
USER QUESTION
-------------
{question}

SQL DATA
--------
{sql_context}

DOCUMENT/RAG DATA
-----------------
{rag_context}

Answer the user's question using ONLY the evidence above.
"""

    # ========================================================
    # GROQ
    # ========================================================

    try:

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

    except groq.RateLimitError as exc:

        raise LLMServiceError(
        "The AI service is temporarily "
        "rate-limited. Please try again shortly."
        ) from exc

    except groq.APIStatusError as exc:

        if getattr(
        exc,
        "status_code",
        None,
        ) == 413:

            raise LLMServiceError(
            "The request is too large for "
            "the AI service to process."
            ) from exc

        raise LLMServiceError(
        "The AI service returned an error. "
        "Please try again later."
    ) from exc

    except Exception as exc:

        raise LLMServiceError(
        "The AI service is currently unavailable. "
        "Please try again later."
        ) from exc

    return (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

# ============================================================
# QUESTION VALIDATION
# ============================================================

def validate_question(
    question: str,
) -> str:
    """
    Validate and normalize the user's question.
    """

    if question is None:

        raise InvalidQuestionError(
            "Question cannot be empty."
        )

    if not isinstance(
        question,
        str,
    ):

        raise InvalidQuestionError(
            "Question must be text."
        )

    question = question.strip()

    if not question:

        raise InvalidQuestionError(
            "Question cannot be empty."
        )

    if len(question) > 2000:

        raise InvalidQuestionError(
            "Question is too long. "
            "Please keep it under 2000 characters."
        )

    return question
# ============================================================
# MAIN SUPPLY CHAIN AGENT
# ============================================================

def ask_supply_chain_agent(
    question: str,
) -> dict:
    """
    Main entry point for the Supply Chain Agent.
    """

    # ========================================================
    # ROUTER
    # ========================================================
    question = validate_question(
        question
    )
    route_result = route_question(
        question
    )

    route = route_result["route"]

    sql_data = None
    rag_data = None

    # ========================================================
    # SQL ROUTE
    # ========================================================

    if route == "SQL":

        sql_data = execute_sql_question(
            question
        )

        answer = generate_final_answer(
            question=question,
            sql_data=sql_data,
        )

    # ========================================================
    # RAG ROUTE
    # ========================================================

    elif route == "RAG":

        from app.rag.rag_service import answer_question
        
        rag_result = answer_question(
            question,
            top_k=3,
        )

        rag_data = rag_result

        answer = rag_result["answer"]

    # ========================================================
    # BOTH ROUTE
    # ========================================================

    elif route == "BOTH":

        sql_data = execute_sql_question(
            question
        )

        rag_result = answer_question(
            question,
            top_k=3,
        )

        rag_data = rag_result

        answer = generate_final_answer(
            question=question,
            sql_data=sql_data,
            rag_data=rag_data,
        )

    # ========================================================
    # INVALID ROUTE
    # ========================================================

    else:

        raise ValueError(
            f"Unknown route: {route}"
        )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {
        "question": question,
        "route": route,
        "answer": answer,
        "sql_data": sql_data,
        "rag_data": rag_data,
    }