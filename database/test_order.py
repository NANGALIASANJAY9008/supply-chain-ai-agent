from app.services.order_service import (
    get_order_by_id,
    get_orders_by_product,
    get_orders_by_supplier,
    get_active_orders,
    get_order_statistics,
)


# ============================================================
# SPECIFIC ORDER
# ============================================================

ORDER_ID = "O000500001"

order = get_order_by_id(
    ORDER_ID
)

print("=" * 60)
print("ORDER INFORMATION")
print("=" * 60)

if order is None:

    print(
        f"Order {ORDER_ID} was not found."
    )

else:

    for key, value in order.items():

        print(
            f"{key}: {value}"
        )


# ============================================================
# PRODUCT ORDERS
# ============================================================

print("\n")
print("=" * 60)
print("ORDERS FOR P0084729")
print("=" * 60)

product_orders = get_orders_by_product(
    "P0084729",
    limit=5,
)

for order in product_orders:

    print(
        f"{order['order_id']} | "
        f"{order['supplier_id']} | "
        f"{order['quantity']} units | "
        f"{order['status']}"
    )


# ============================================================
# SUPPLIER ORDERS
# ============================================================

print("\n")
print("=" * 60)
print("ORDERS FROM S003821")
print("=" * 60)

supplier_orders = get_orders_by_supplier(
    "S003821",
    limit=5,
)

for order in supplier_orders:

    print(
        f"{order['order_id']} | "
        f"{order['product_id']} | "
        f"{order['quantity']} units | "
        f"{order['status']}"
    )


# ============================================================
# ACTIVE ORDERS
# ============================================================

print("\n")
print("=" * 60)
print("ACTIVE ORDERS")
print("=" * 60)

active_orders = get_active_orders(
    limit=5
)

for order in active_orders:

    print(
        f"{order['order_id']} | "
        f"{order['status']} | "
        f"{order['total_value']}"
    )


# ============================================================
# STATISTICS
# ============================================================

print("\n")
print("=" * 60)
print("ORDER STATISTICS")
print("=" * 60)

statistics = get_order_statistics()

for key, value in statistics.items():

    print(
        f"{key}: {value}"
    )