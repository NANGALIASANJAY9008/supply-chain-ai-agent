import sqlite3

DATABASE_PATH = "database/supply_chain.db"

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

# Check tables
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print("-", table[0])

# Check row counts
print("\nRow counts:")

for table in ["products", "suppliers", "inventory", "orders"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]

    print(f"{table}: {count:,}")

connection.close()

print("\nDatabase verification completed successfully.")