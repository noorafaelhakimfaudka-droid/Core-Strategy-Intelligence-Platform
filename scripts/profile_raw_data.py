"""CSIP Raw Data Profiling and Referential Integrity Audit Script.

SKKNI Compliance:
- [UK-03 Menelaah Data]
- [UK-04 Memvalidasi Data]
- [UK-05 Menentukan Objek Data]
"""

import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.data.loader import OlistDataLoader, load_yaml_config


def profile_all_tables():
    loader = OlistDataLoader(
        config_path=REPO_ROOT / "config" / "data.yaml",
        raw_data_dir=REPO_ROOT / "data" / "raw",
    )

    table_keys = list(loader.tables_config.keys())
    print(f"Profiling {len(table_keys)} tables: {table_keys}\n")

    summary_records = []
    columns_catalog = {}
    loaded_dfs = {}

    for t_key in table_keys:
        print(f"--- Loading & Validating: {t_key} ---")
        df = loader.load_table(t_key, validate=True, use_cache=True)
        loaded_dfs[t_key] = df
        res = loader.validation_history[t_key]

        # Detailed column level profiling
        cols_info = []
        for col in df.columns:
            n_null = int(df[col].isnull().sum())
            pct_null = float((n_null / len(df)) * 100)
            n_unique = int(df[col].nunique(dropna=True))
            dtype_str = str(df[col].dtype)
            sample_val = df[col].dropna().iloc[0] if n_unique > 0 else None
            if isinstance(sample_val, (pd.Timestamp, np.datetime64)):
                sample_val = str(sample_val)
            elif isinstance(sample_val, (np.integer, int)):
                sample_val = int(sample_val)
            elif isinstance(sample_val, (np.floating, float)):
                sample_val = round(float(sample_val), 4)

            cols_info.append({
                "column_name": col,
                "dtype": dtype_str,
                "null_count": n_null,
                "null_pct": round(pct_null, 2),
                "unique_count": n_unique,
                "sample_value": sample_val,
            })

        columns_catalog[t_key] = cols_info

        summary_records.append({
            "table_name": t_key,
            "filename": loader.tables_config[t_key].get("filename"),
            "rows": len(df),
            "columns": len(df.columns),
            "primary_key": str(loader.tables_config[t_key].get("primary_key")),
            "duplicate_pk_rows": res.duplicate_pk_count,
            "initial_mb": round(res.memory_initial_mb, 2),
            "downsized_mb": round(res.memory_downsized_mb, 2),
            "reduction_pct": round(res.memory_reduction_pct, 1),
            "chronological_violations": res.chronological_violations,
            "warnings_count": len(res.warnings),
            "errors_count": len(res.errors),
            "warnings": res.warnings,
            "errors": res.errors,
        })

    # Referential Integrity & Orphan Records Check
    print("\n--- Auditing Referential Integrity (Orphan Records) ---")
    orphan_results = {}

    orders_df = loaded_dfs["orders"]
    order_items_df = loaded_dfs["order_items"]
    payments_df = loaded_dfs["order_payments"]
    reviews_df = loaded_dfs["order_reviews"]
    customers_df = loaded_dfs["customers"]
    products_df = loaded_dfs["products"]
    sellers_df = loaded_dfs["sellers"]

    # 1. orders -> customers
    order_cust_ids = set(orders_df["customer_id"].dropna())
    customer_cust_ids = set(customers_df["customer_id"].dropna())
    orphan_order_cust = len(order_cust_ids - customer_cust_ids)
    orphan_results["orders_without_customer"] = orphan_order_cust

    # 2. items -> orders
    item_order_ids = set(order_items_df["order_id"].dropna())
    order_ids = set(orders_df["order_id"].dropna())
    orphan_item_orders = len(item_order_ids - order_ids)
    orphan_results["order_items_without_order"] = orphan_item_orders

    # 3. items -> products
    item_prod_ids = set(order_items_df["product_id"].dropna())
    prod_ids = set(products_df["product_id"].dropna())
    orphan_item_products = len(item_prod_ids - prod_ids)
    orphan_results["order_items_without_product"] = orphan_item_products

    # 4. items -> sellers
    item_seller_ids = set(order_items_df["seller_id"].dropna())
    seller_ids = set(sellers_df["seller_id"].dropna())
    orphan_item_sellers = len(item_seller_ids - seller_ids)
    orphan_results["order_items_without_seller"] = orphan_item_sellers

    # 5. payments -> orders
    payment_order_ids = set(payments_df["order_id"].dropna())
    orphan_payment_orders = len(payment_order_ids - order_ids)
    orphan_results["payments_without_order"] = orphan_payment_orders

    # 6. reviews -> orders
    review_order_ids = set(reviews_df["order_id"].dropna())
    orphan_review_orders = len(review_order_ids - order_ids)
    orphan_results["reviews_without_order"] = orphan_review_orders

    print("Orphan Records Audit:")
    for k, v in orphan_results.items():
        print(f"  {k}: {v}")

    # Unique customers repeat rate inspection
    total_customers = len(customers_df)
    unique_buyers = customers_df["customer_unique_id"].nunique()
    orders_per_buyer = customers_df.groupby("customer_unique_id")["customer_id"].count()
    repeat_buyers = int((orders_per_buyer > 1).sum())
    repeat_pct = (repeat_buyers / unique_buyers) * 100

    print(f"\nCustomer Entity Audit:")
    print(f"  Total customer sessions (customer_id): {total_customers:,}")
    print(f"  Unique real customers (customer_unique_id): {unique_buyers:,}")
    print(f"  Repeat customers (>1 order): {repeat_buyers:,} ({repeat_pct:.2f}%)")

    # Order date range inspection
    min_order_date = orders_df["order_purchase_timestamp"].min()
    max_order_date = orders_df["order_purchase_timestamp"].max()
    print(f"\nOrder Timestamp Range: {min_order_date} to {max_order_date}")

    # Save profiling output to JSON for documentation and reports
    profile_out = {
        "summary": summary_records,
        "columns_catalog": columns_catalog,
        "orphan_records": orphan_results,
        "customer_entity_audit": {
            "total_customer_sessions": total_customers,
            "unique_real_customers": unique_buyers,
            "repeat_customers": repeat_buyers,
            "repeat_customer_pct": round(repeat_pct, 2),
        },
        "order_date_range": {
            "min_purchase": str(min_order_date),
            "max_purchase": str(max_order_date),
        }
    }

    out_file = REPO_ROOT / "artifacts" / "reports" / "raw_data_profile.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profile_out, f, indent=2)
    print(f"\nProfile successfully saved to: {out_file}")


if __name__ == "__main__":
    profile_all_tables()

