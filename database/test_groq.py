from app.rag.llm_service import (
    generate_answer,
)


context = """
The inventory management policy states that
available stock is calculated as:

Available Stock = Current Stock - Reserved Stock.

When available stock falls below the reorder
level, the product should be reviewed for
replenishment.
"""


question = (
    "When should inventory be reordered?"
)


answer = generate_answer(
    question,
    context,
)


print("=" * 70)
print("GROQ TEST")
print("=" * 70)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)

print("=" * 70)