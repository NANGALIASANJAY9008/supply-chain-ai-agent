from app.agents.router import route_question


questions = [
    "What is the current stock of P0084729?",

    "What is the supplier return policy?",

    "Which suppliers have high delivery delays?",

    "What happens when a supplier delivers late?",

    "P0084729 is low in stock. "
    "What does the inventory policy recommend?",

    "How many pending orders are there?",
]


print("=" * 70)
print("SUPPLY CHAIN AGENT ROUTER")
print("=" * 70)


for question in questions:

    result = route_question(
        question
    )

    print("\nQUESTION:")
    print(question)

    print(
        f"ROUTE: {result['route']}"
    )

    print("-" * 70)