# ============================================================
# SUPPLY CHAIN AGENT ERRORS
# ============================================================


class SupplyChainAgentError(
    Exception
):
    """
    Base exception for the Supply Chain Agent.
    """
    pass


class InvalidQuestionError(
    SupplyChainAgentError
):
    """
    Raised when the user question is empty
    or invalid.
    """
    pass


class QueryPlanningError(
    SupplyChainAgentError
):
    """
    Raised when the dynamic query planner
    cannot produce a valid query plan.
    """
    pass


class QueryExecutionError(
    SupplyChainAgentError
):
    """
    Raised when database query execution fails.
    """
    pass


class LLMServiceError(
    SupplyChainAgentError
):
    """
    Raised when the LLM service fails.
    """
    pass