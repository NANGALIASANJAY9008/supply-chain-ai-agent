from pprint import pprint

from app.agents.sql_agent import (
    product_lookup,
    inventory_lookup,
    supplier_lookup,
    order_lookup,
    get_low_stock_products,
    get_top_reliable_suppliers,
    get_active_orders,
    orders_by_product,
)


PRODUCT_ID = "P0084729"
SUPPLIER_ID = "S003821"
ORDER_ID = "O000500001"


print("=" * 70)
print("SUPPLY CHAIN SQL AGENT")
print("=" * 70)


print("\nPRODUCT")
print("-" * 70)

pprint(
    product_lookup(
        PRODUCT_ID
    )
)


print("\nINVENTORY")
print("-" * 70)

pprint(
    inventory_lookup(
        PRODUCT_ID
    )
)


print("\nSUPPLIER")
print("-" * 70)

pprint(
    supplier_lookup(
        SUPPLIER_ID
    )
)


print("\nORDER")
print("-" * 70)

pprint(
    order_lookup(
        ORDER_ID
    )
)


print("\nLOW STOCK PRODUCTS")
print("-" * 70)

pprint(
    get_low_stock_products()
)


print("\nTOP RELIABLE SUPPLIERS")
print("-" * 70)

pprint(
    get_top_reliable_suppliers()
)


print("\nACTIVE ORDERS")
print("-" * 70)

pprint(
    get_active_orders()
)


print("\nORDERS FOR PRODUCT")
print("-" * 70)

pprint(
    orders_by_product(
        PRODUCT_ID
    )
)