import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

MODEL_NAME = "llama-3.3-70b-versatile"


# ============================================================
# VALIDATE API KEY
# ============================================================

if not GROQ_API_KEY:

    raise RuntimeError(
        "GROQ_API_KEY is not configured. "
        "Add it to the .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# GENERATE GROUNDED ANSWER
# ============================================================

def generate_answer(
    question: str,
    context: str,
) -> str:
    """
    Generate a grounded answer using
    the retrieved RAG context.
    """

    system_prompt = """
You are a Supply Chain Q&A Assistant.

Your job is to answer questions using ONLY
the supplied context.

Rules:

1. Do not invent facts.
2. Do not use outside knowledge.
3. If the context does not contain enough
   information, clearly say that the available
   documents do not provide enough information.
4. Keep the answer clear and concise.
5. Preserve important numbers, conditions,
   dates, and business rules.
6. Do not make assumptions that are not supported
   by the context.
7. Do not mention information that is unrelated
   to the user's question.
"""

    user_prompt = f"""
CONTEXT
-------
{context}

USER QUESTION
-------------
{question}

Answer the user's question using only the
provided context.
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

    return response.choices[0].message.content