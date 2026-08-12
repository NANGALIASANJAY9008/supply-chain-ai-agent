from app.agents.query_compiler import (
    compile_query,
)

from app.database.connection import (
    get_db_connection,
)

from app.agents.errors import (
    QueryExecutionError,
)


# ============================================================
# MAXIMUM ROWS SENT TO LLM
# ============================================================

MAX_LLM_ROWS = 50


# ============================================================
# EXECUTE DYNAMIC QUERY
# ============================================================

def execute_dynamic_query(
    plan: dict,
) -> dict:
    """
    Execute a validated dynamic query plan.

    Large result sets are limited before being
    passed to the LLM.
    """

    try:

        sql, parameters = compile_query(
            plan
        )

    except Exception as exc:

        raise QueryExecutionError(
            "Unable to compile the requested "
            "database query."
        ) from exc

    try:

        connection = get_db_connection()

    except Exception as exc:

        raise QueryExecutionError(
            "Unable to connect to the supply-chain database."
        ) from exc

    try:

        cursor = connection.cursor()

        cursor.execute(
            sql,
            parameters,
        )

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description
            in cursor.description
        ]

        all_results = []

        for row in rows:

            all_results.append(
                dict(
                    zip(
                        columns,
                        row,
                    )
                )
            )

        total_row_count = len(
            all_results
        )

        truncated = (
            total_row_count
            > MAX_LLM_ROWS
        )

        results = all_results[
            :MAX_LLM_ROWS
        ]

        return {
            "sql_operation": plan[
                "operation"
            ],

            "table": plan[
                "table"
            ],

            "total_row_count": (
                total_row_count
            ),

            "row_count": len(
                results
            ),

            "truncated": truncated,

            "max_llm_rows": (
                MAX_LLM_ROWS
            ),

            "results": results,
        }

    except Exception as exc:

        raise QueryExecutionError(
            "Unable to execute the requested "
            "database query."
        ) from exc

    finally:

        connection.close()