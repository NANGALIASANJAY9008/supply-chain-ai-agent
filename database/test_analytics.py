from app.services.analytics_service import (
    get_low_stock_with_incoming_orders,
    get_supplier_risk_analysis,
    get_product_order_summary,
)


# ============================================================
# LOW STOCK + ACTIVE ORDERS
# ============================================================

print("=" * 70)
print("LOW STOCK PRODUCTS WITH ACTIVE ORDERS")
print("=" * 70)

results = get_low_stock_with_incoming_orders(
    limit=5
)

for item in results:

    print(
        f"{item['product_id']} | "
        f"{item['product_name']} | "
        f"Available: {item['available_stock']} | "
        f"Reorder: {item['reorder_level']} | "
        f"Active Orders: {item['active_order_count']} | "
        f"Active Qty: {item['active_order_quantity']}"
    )


# ============================================================
# SUPPLIER RISK
# ============================================================

print("\n")
print("=" * 70)
print("SUPPLIER RISK ANALYSIS")
print("=" * 70)

risk_suppliers = get_supplier_risk_analysis(
    minimum_delay=5.0,
    maximum_reliability=80.0,
    limit=5,
)

for supplier in risk_suppliers:

    print(
        f"{supplier['supplier_id']} | "
        f"{supplier['supplier_name']} | "
        f"Reliability: "
        f"{supplier['reliability_score']}% | "
        f"Delay: "
        f"{supplier['average_delay_days']} days"
    )


# ============================================================
# PRODUCT SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("PRODUCT SUPPLY-CHAIN SUMMARY")
print("=" * 70)

summary = get_product_order_summary(
    "P0084729"
)

if summary is None:

    print("Product not found.")

else:

    for key, value in summary.items():

        print(
            f"{key}: {value}"
        )