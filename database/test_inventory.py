from app.services.inventory_service import (
    get_inventory_by_product,
)


PRODUCT_ID = "P0084729"


result = get_inventory_by_product(
    PRODUCT_ID
)


if result is None:

    print(
        f"Product {PRODUCT_ID} "
        "was not found."
    )

else:

    print("=" * 50)
    print("INVENTORY INFORMATION")
    print("=" * 50)

    print(
        f"Product ID:       "
        f"{result['product_id']}"
    )

    print(
        f"Product Name:     "
        f"{result['product_name']}"
    )

    print(
        f"Category:         "
        f"{result['category']}"
    )

    print(
        f"Warehouse:        "
        f"{result['warehouse']}"
    )

    print(
        f"Current Stock:    "
        f"{result['current_stock']}"
    )

    print(
        f"Reserved Stock:   "
        f"{result['reserved_stock']}"
    )

    print(
        f"Available Stock:  "
        f"{result['available_stock']}"
    )

    print(
        f"Incoming Stock:   "
        f"{result['incoming_stock']}"
    )

    print(
        f"Reorder Level:    "
        f"{result['reorder_level']}"
    )

    print(
        f"Stock Status:     "
        f"{result['stock_status']}"
    )

    print(
        f"Last Restock:     "
        f"{result['last_restock_date']}"
    )

    print("=" * 50)