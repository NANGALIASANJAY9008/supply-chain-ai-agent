from app.agents.agent import (
    ask_supply_chain_agent,
)


questions = [

    "Do we have enough P0084729?",

    "How much inventory is currently "
    "available for P0084729?",

    "Tell me about supplier S003821.",

    "Which vendors have the highest delays?",

    "Which suppliers are the most dependable?",

    "Show me products that need replenishment.",

    "What happened with order O000500001?",

    "Show me orders associated with P0084729.",

    "Do we have any pending orders?",
]


print("=" * 80)
print("NATURAL LANGUAGE SUPPLY CHAIN TEST")
print("=" * 80)


for question in questions:

    print("\n")
    print("=" * 80)

    print("QUESTION:")
    print(question)

    result = ask_supply_chain_agent(
        question
    )

    print("\nROUTE:")
    print(result["route"])

    print("\nANSWER:")
    print(result["answer"])