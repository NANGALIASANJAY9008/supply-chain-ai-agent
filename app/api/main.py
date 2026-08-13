from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agents.agent import (
    ask_supply_chain_agent,
)

from fastapi import (
    FastAPI,
    HTTPException,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from pydantic import (
    BaseModel,
    Field,
)

from app.agents.errors import (
    InvalidQuestionError,
    QueryExecutionError,
    QueryPlanningError,
    LLMServiceError,
)

# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Supply Chain Q&A Agent",
    description=(
        "AI-powered Supply Chain Question "
        "Answering API using SQL, RAG and "
        "Dynamic Query Planning."
    ),
    version="1.0.0",
)
# ============================================================
# CORS CONFIGURATION
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    "http://localhost:4173",
    "http://127.0.0.1:4173",

    "http://localhost:3000",
    "http://127.0.0.1:3000",
]



# ============================================================
# REQUEST MODEL
# ============================================================

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description=(
            "Natural-language supply-chain question."
        ),
    )


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "name": "Supply Chain Q&A Agent",
        "status": "running",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
    }


# ============================================================
# ASK ENDPOINT
# ============================================================

# ============================================================
# ASK ENDPOINT
# ============================================================

@app.post("/ask")
def ask(
    request: AskRequest,
):

    try:

        result = ask_supply_chain_agent(
            request.question
        )

        return result

    except InvalidQuestionError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except (
        QueryExecutionError,
        QueryPlanningError,
        LLMServiceError,
    ) as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while processing the question."
            ),
        )