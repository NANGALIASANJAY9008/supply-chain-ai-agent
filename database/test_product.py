import sqlite3

DATABASE_PATH = "database/supply_chain.db"

PRODUCT_ID = "P0084729"

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

query = """
SELECT
    product_id,
    product_name,
    category,
    unit_price,
    reorder_level,
    warehouse
FROM products
WHERE product_id = ?
"""

cursor.execute(query, (PRODUCT_ID,))

product = cursor.fetchone()

if product:
    print("Product found!")
    print()
    print(f"Product ID:       {product[0]}")
    print(f"Product Name:     {product[1]}")
    print(f"Category:         {product[2]}")
    print(f"Unit Price:       ₹{product[3]:,.2f}")
    print(f"Reorder Level:    {product[4]}")
    print(f"Warehouse:        {product[5]}")
else:
    print(f"Product {PRODUCT_ID} was not found.")

connection.close()