"""Run EDA visual analysis and generate figure artifacts."""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = REPO_ROOT / "artifacts" / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def generate_figures():
    orders_df = pd.read_parquet(REPO_ROOT / "data" / "interim" / "clean_orders.parquet")
    items_df = pd.read_parquet(REPO_ROOT / "data" / "interim" / "clean_order_items.parquet")
    reviews_df = pd.read_parquet(REPO_ROOT / "data" / "interim" / "clean_order_reviews.parquet")

    # 1. Asymmetric Delay vs Satisfaction
    ord_rev = orders_df.merge(
        reviews_df[["order_id", "review_score", "has_review_comment"]],
        on="order_id",
        how="inner"
    )

    ord_rev["delivery_delay_days"] = (
        ord_rev["order_delivered_customer_date"] - ord_rev["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400.0

    bins = [-40, -14, -7, -3, 0, 3, 7, 14, 40]
    labels = ["Early >14d", "Early 7-14d", "Early 3-7d", "Early 0-3d", "Late 0-3d", "Late 3-7d", "Late 7-14d", "Late >14d"]
    ord_rev["delay_bracket"] = pd.cut(ord_rev["delivery_delay_days"], bins=bins, labels=labels)

    delay_satisfaction = ord_rev.groupby("delay_bracket", observed=True)["review_score"].agg(["mean", "count"]).reset_index()

    fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
    bars = ax.bar(
        delay_satisfaction["delay_bracket"],
        delay_satisfaction["mean"],
        color=["#2b5c8f" if "Early" in str(x) else "#d9534f" for x in delay_satisfaction["delay_bracket"]],
        edgecolor="black",
        alpha=0.85
    )

    ax.axhline(y=4.0, color="gray", linestyle="--", linewidth=1, label="Batas Kepuasan Baik (4.0)")
    ax.set_title("Eksplorasi H2: Asymmetric Delay Penalty pada Kepuasan Pelanggan", fontsize=13, fontweight="bold")
    ax.set_xlabel("Braket Waktu Pengiriman Relatif terhadap Janji Estimasi", fontsize=11)
    ax.set_ylabel("Rata-rata Review Score (Skala 1-5)", fontsize=11)
    ax.set_ylim(1.0, 5.0)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend()

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f"{yval:.2f}", ha='center', va='bottom', fontsize=9)

    plt.xticks(rotation=25)
    plt.tight_layout()
    fig1_path = FIGURES_DIR / "eda_delay_vs_satisfaction.png"
    plt.savefig(fig1_path)
    plt.close()
    print(f"Generated: {fig1_path}")

    # 2. Weekly Trend
    orders_df["year_week"] = orders_df["order_purchase_timestamp"].dt.to_period("W").astype(str)
    weekly_volume = orders_df.groupby("year_week")["order_id"].count().reset_index()
    weekly_volume = weekly_volume[weekly_volume["year_week"] >= "2017-01"].sort_values("year_week")

    fig, ax = plt.subplots(figsize=(12, 4), dpi=120)
    ax.plot(weekly_volume["year_week"], weekly_volume["order_id"], marker="o", markersize=3, color="#1f77b4", linewidth=1.5)
    ax.set_title("Dinamika Volume Pesanan Mingguan (2017 - 2018)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Tahun-Minggu (Year-Week)", fontsize=10)
    ax.set_ylabel("Jumlah Pesanan", fontsize=10)
    ax.grid(True, linestyle=":", alpha=0.6)

    matches = [w for w in weekly_volume["year_week"] if "2017-11" in w]
    if matches:
        spike_idx = matches[-1]
        y_spike = weekly_volume.loc[weekly_volume["year_week"] == spike_idx, "order_id"].values[0]
        ax.annotate(
            "Black Friday 2017 Spike",
            xy=(spike_idx, y_spike),
            xytext=(spike_idx, y_spike + 400),
            arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=6),
            fontweight="bold", color="red"
        )

    plt.xticks(ticks=range(0, len(weekly_volume), 4), labels=weekly_volume["year_week"].iloc[::4], rotation=45)
    plt.tight_layout()
    fig2_path = FIGURES_DIR / "eda_weekly_order_trend.png"
    plt.savefig(fig2_path)
    plt.close()
    print(f"Generated: {fig2_path}")


if __name__ == "__main__":
    generate_figures()

