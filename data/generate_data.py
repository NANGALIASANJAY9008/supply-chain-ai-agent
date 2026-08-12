import os
from datetime import datetime

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

NUM_PRODUCTS = 100_000
NUM_SUPPLIERS = 10_000
NUM_ORDERS = 1_000_000

NUM_WAREHOUSES = 50
ORDER_CHUNK_SIZE = 100_000

RANDOM_SEED = 42

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCTS_FILE = os.path.join(DATA_DIR, "products.csv")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.csv")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.csv")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.csv")


# ============================================================
# RANDOM GENERATOR
# ============================================================

rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# MASTER DATA
# ============================================================

CATEGORIES = [
    "Electronics",
    "Accessories",
    "Furniture",
    "Networking",
    "Warehouse Equipment",
    "Office Supplies",
    "Industrial Equipment",
    "Computer Hardware",
    "Packaging",
    "Safety Equipment",
    "Automotive Parts",
    "Electrical Components",
    "Mechanical Parts",
    "Tools",
    "Cleaning Supplies",
    "Storage Equipment",
    "IT Equipment",
    "Lighting",
    "Raw Materials",
    "Consumables",
]

WAREHOUSES = [
    f"WH{str(i).zfill(3)}"
    for i in range(1, NUM_WAREHOUSES + 1)
]

INDIAN_CITIES = [
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Gurgaon",
    "Noida",
    "Jaipur",
    "Kochi",
    "Lucknow",
    "Indore",
    "Coimbatore",
]

PRODUCT_PREFIXES = [
    "Pro",
    "Ultra",
    "Smart",
    "Advanced",
    "Industrial",
    "Premium",
    "Standard",
    "Eco",
    "Power",
    "NextGen",
]

PRODUCT_TYPES = [
    "Laptop",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Router",
    "Scanner",
    "Printer",
    "Desk",
    "Chair",
    "Camera",
    "Server",
    "Switch",
    "Cable",
    "Adapter",
    "Sensor",
    "Controller",
    "Drive",
    "Battery",
    "Module",
    "Terminal",
]


# ============================================================
# 1. GENERATE SUPPLIERS
# ============================================================

def generate_suppliers():
    print("Generating suppliers...")

    supplier_ids = [
        f"S{str(i).zfill(6)}"
        for i in range(1, NUM_SUPPLIERS + 1)
    ]

    supplier_names = [
        f"{rng.choice(PRODUCT_PREFIXES)} Supply Solutions {i}"
        for i in range(1, NUM_SUPPLIERS + 1)
    ]

    locations = rng.choice(
        INDIAN_CITIES,
        size=NUM_SUPPLIERS
    )

    lead_times = rng.integers(
        3,
        31,
        size=NUM_SUPPLIERS
    )

    reliability_scores = np.round(
        rng.uniform(65, 99, size=NUM_SUPPLIERS),
        2
    )

    average_delays = np.round(
        rng.uniform(0.2, 12.0, size=NUM_SUPPLIERS),
        2
    )

    suppliers = pd.DataFrame({
        "supplier_id": supplier_ids,
        "supplier_name": supplier_names,
        "location": locations,
        "lead_time_days": lead_times,
        "reliability_score": reliability_scores,
        "average_delay_days": average_delays,
    })

    suppliers.to_csv(
        SUPPLIERS_FILE,
        index=False
    )

    print(
        f"Suppliers created: {len(suppliers):,}"
    )


# ============================================================
# 2. GENERATE PRODUCTS
# ============================================================

def generate_products():
    print("Generating products...")

    product_ids = [
        f"P{str(i).zfill(7)}"
        for i in range(1, NUM_PRODUCTS + 1)
    ]

    product_names = [
        f"{rng.choice(PRODUCT_PREFIXES)} "
        f"{rng.choice(PRODUCT_TYPES)} "
        f"{i}"
        for i in range(1, NUM_PRODUCTS + 1)
    ]

    categories = rng.choice(
        CATEGORIES,
        size=NUM_PRODUCTS
    )

    unit_prices = np.round(
        rng.uniform(100, 150000, size=NUM_PRODUCTS),
        2
    )

    reorder_levels = rng.integers(
        10,
        500,
        size=NUM_PRODUCTS
    )

    warehouse_assignment = rng.choice(
        WAREHOUSES,
        size=NUM_PRODUCTS
    )

    products = pd.DataFrame({
        "product_id": product_ids,
        "product_name": product_names,
        "category": categories,
        "unit_price": unit_prices,
        "reorder_level": reorder_levels,
        "warehouse": warehouse_assignment,
    })

    products.to_csv(
        PRODUCTS_FILE,
        index=False
    )

    print(
        f"Products created: {len(products):,}"
    )


# ============================================================
# 3. GENERATE INVENTORY
# ============================================================

def generate_inventory():
    print("Generating inventory...")

    products = pd.read_csv(
        PRODUCTS_FILE,
        usecols=[
            "product_id",
            "reorder_level",
            "warehouse",
        ]
    )

    inventory_ids = [
        f"I{str(i).zfill(7)}"
        for i in range(1, len(products) + 1)
    ]

    current_stock = rng.integers(
        0,
        1000,
        size=len(products)
    )

    reserved_stock = np.minimum(
        rng.integers(
            0,
            250,
            size=len(products)
        ),
        current_stock
    )

    incoming_stock = rng.integers(
        0,
        1000,
        size=len(products)
    )

    start_date = np.datetime64("2026-01-01")
    end_date = np.datetime64("2026-08-10")

    days_range = (
        end_date - start_date
    ).astype("timedelta64[D]").astype(int)

    restock_dates = (
        start_date
        + rng.integers(
            0,
            days_range + 1,
            size=len(products)
        ).astype("timedelta64[D]")
    )

    inventory = pd.DataFrame({
        "inventory_id": inventory_ids,
        "product_id": products["product_id"],
        "warehouse": products["warehouse"],
        "current_stock": current_stock,
        "reserved_stock": reserved_stock,
        "incoming_stock": incoming_stock,
        "reorder_level": products["reorder_level"],
        "last_restock_date": restock_dates,
    })

    inventory.to_csv(
        INVENTORY_FILE,
        index=False
    )

    print(
        f"Inventory records created: {len(inventory):,}"
    )


# ============================================================
# 4. GENERATE ORDERS
# ============================================================

def generate_orders():
    print(
        f"Generating {NUM_ORDERS:,} orders..."
    )

    products = pd.read_csv(
        PRODUCTS_FILE,
        usecols=[
            "product_id",
            "unit_price",
        ]
    )

    suppliers = pd.read_csv(
        SUPPLIERS_FILE,
        usecols=[
            "supplier_id",
            "lead_time_days",
        ]
    )

    product_ids = products["product_id"].to_numpy()
    product_prices = products["unit_price"].to_numpy()

    supplier_ids = suppliers["supplier_id"].to_numpy()
    supplier_lead_times = (
        suppliers["lead_time_days"].to_numpy()
    )

    if os.path.exists(ORDERS_FILE):
        os.remove(ORDERS_FILE)

    order_counter = 1

    start_date = np.datetime64("2025-01-01")
    end_date = np.datetime64("2026-08-10")

    total_days = (
        end_date - start_date
    ).astype("timedelta64[D]").astype(int)

    first_chunk = True

    for start in range(
        0,
        NUM_ORDERS,
        ORDER_CHUNK_SIZE
    ):

        chunk_size = min(
            ORDER_CHUNK_SIZE,
            NUM_ORDERS - start
        )

        print(
            f"Processing orders "
            f"{start + 1:,} - "
            f"{start + chunk_size:,}"
        )

        selected_product_indexes = rng.integers(
            0,
            len(product_ids),
            size=chunk_size
        )

        selected_supplier_indexes = rng.integers(
            0,
            len(supplier_ids),
            size=chunk_size
        )

        selected_products = (
            product_ids[
                selected_product_indexes
            ]
        )

        selected_suppliers = (
            supplier_ids[
                selected_supplier_indexes
            ]
        )

        selected_prices = (
            product_prices[
                selected_product_indexes
            ]
        )

        selected_lead_times = (
            supplier_lead_times[
                selected_supplier_indexes
            ]
        )

        order_dates = (
            start_date
            + rng.integers(
                0,
                total_days + 1,
                size=chunk_size
            ).astype("timedelta64[D]")
        )

        expected_delivery_dates = (
            order_dates
            + selected_lead_times.astype(
                "timedelta64[D]"
            )
        )

        quantities = rng.integers(
            1,
            1000,
            size=chunk_size
        )

        total_values = np.round(
            quantities * selected_prices,
            2
        )

        random_values = rng.random(
            chunk_size
        )

        statuses = np.where(
            random_values < 0.55,
            "Delivered",
            np.where(
                random_values < 0.70,
                "Delivered Late",
                np.where(
                    random_values < 0.85,
                    "In Transit",
                    "Pending"
                )
            )
        )

        actual_delivery_dates = (
            expected_delivery_dates
            + rng.integers(
                -2,
                10,
                size=chunk_size
            ).astype("timedelta64[D]")
        )

        actual_delivery_dates = (
            actual_delivery_dates.astype(
                "datetime64[D]"
            )
        )

        actual_delivery_dates = np.where(
            np.isin(
                statuses,
                ["Pending", "In Transit"]
            ),
            np.datetime64("NaT"),
            actual_delivery_dates
        )

        order_ids = [
            f"O{str(i).zfill(9)}"
            for i in range(
                order_counter,
                order_counter + chunk_size
            )
        ]

        orders = pd.DataFrame({
            "order_id": order_ids,
            "product_id": selected_products,
            "supplier_id": selected_suppliers,
            "order_date": order_dates,
            "expected_delivery_date":
                expected_delivery_dates,
            "actual_delivery_date":
                actual_delivery_dates,
            "quantity": quantities,
            "unit_price":
                np.round(selected_prices, 2),
            "total_value":
                total_values,
            "status": statuses,
        })

        orders.to_csv(
            ORDERS_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        first_chunk = False

        order_counter += chunk_size

    print(
        f"Orders created: {NUM_ORDERS:,}"
    )


# ============================================================
# 5. MAIN
# ============================================================

def main():

    print("=" * 60)
    print("SUPPLY CHAIN DATA GENERATOR")
    print("=" * 60)

    print()
    print(f"Products   : {NUM_PRODUCTS:,}")
    print(f"Suppliers  : {NUM_SUPPLIERS:,}")
    print(f"Orders     : {NUM_ORDERS:,}")
    print(f"Warehouses : {NUM_WAREHOUSES}")
    print()

    generate_suppliers()

    generate_products()

    generate_inventory()

    generate_orders()

    print()
    print("=" * 60)
    print("DATA GENERATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()