from app.services.supplier_service import (
    get_supplier_by_id,
    get_top_reliable_suppliers,
    get_high_delay_suppliers,
)


SUPPLIER_ID = "S003821"


# ============================================================
# SUPPLIER LOOKUP
# ============================================================

supplier = get_supplier_by_id(
    SUPPLIER_ID
)

print("=" * 60)
print("SUPPLIER INFORMATION")
print("=" * 60)

if supplier is None:

    print(
        f"Supplier {SUPPLIER_ID} "
        "was not found."
    )

else:

    print(
        f"Supplier ID:       "
        f"{supplier['supplier_id']}"
    )

    print(
        f"Supplier Name:     "
        f"{supplier['supplier_name']}"
    )

    print(
        f"Location:          "
        f"{supplier['location']}"
    )

    print(
        f"Lead Time:         "
        f"{supplier['lead_time_days']} days"
    )

    print(
        f"Reliability:       "
        f"{supplier['reliability_score']}%"
    )

    print(
        f"Average Delay:     "
        f"{supplier['average_delay_days']} days"
    )


# ============================================================
# TOP RELIABLE SUPPLIERS
# ============================================================

print("\n")
print("=" * 60)
print("TOP 5 RELIABLE SUPPLIERS")
print("=" * 60)

top_suppliers = get_top_reliable_suppliers(
    limit=5
)

for supplier in top_suppliers:

    print(
        f"{supplier['supplier_id']} | "
        f"{supplier['supplier_name']} | "
        f"{supplier['reliability_score']}%"
    )


# ============================================================
# HIGH DELAY SUPPLIERS
# ============================================================

print("\n")
print("=" * 60)
print("HIGH DELAY SUPPLIERS")
print("=" * 60)

high_delay_suppliers = (
    get_high_delay_suppliers(
        minimum_delay=5.0,
        limit=5,
    )
)

for supplier in high_delay_suppliers:

    print(
        f"{supplier['supplier_id']} | "
        f"{supplier['supplier_name']} | "
        f"{supplier['average_delay_days']} days"
    )