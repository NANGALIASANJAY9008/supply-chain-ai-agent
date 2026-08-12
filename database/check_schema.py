import sqlite3


connection = sqlite3.connect(
    "database/supply_chain.db"
)

cursor = connection.cursor()


tables = [
    "products",
    "inventory",
    "suppliers",
    "orders",
]


for table in tables:

    print("\n")
    print("=" * 70)
    print(f"TABLE: {table}")
    print("=" * 70)

    cursor.execute(
        f"PRAGMA table_info({table})"
    )

    columns = cursor.fetchall()

    for column in columns:

        print(
            f"{column[1]:30} "
            f"{column[2]}"
        )


connection.close()