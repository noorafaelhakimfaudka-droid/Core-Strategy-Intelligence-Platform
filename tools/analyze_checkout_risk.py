import pandas as pd
from pathlib import Path

raw_dir = Path('data/raw')
if not raw_dir.exists():
    raw_dir = Path('data')

orders = pd.read_csv(list(raw_dir.glob('*orders*.csv'))[0])
items = pd.read_csv(list(raw_dir.glob('*items*.csv'))[0])
payments = pd.read_csv(list(raw_dir.glob('*payments*.csv'))[0])
reviews = pd.read_csv(list(raw_dir.glob('*reviews*.csv'))[0])

print("Total orders in raw:", len(orders))
print("Status breakdown:\n", orders['order_status'].value_counts())

canceled = orders[orders['order_status'] == 'canceled']
unavailable = orders[orders['order_status'] == 'unavailable']

print("\nCanceled total:", len(canceled))
canceled_items = items[items['order_id'].isin(canceled['order_id'])]
print(f"Canceled with items: {canceled_items['order_id'].nunique()} ({len(canceled_items)} items)")
canceled_payments = payments[payments['order_id'].isin(canceled['order_id'])]
print(f"Canceled with payments: {canceled_payments['order_id'].nunique()}")
canceled_reviews = reviews[reviews['order_id'].isin(canceled['order_id'])]
print(f"Canceled with reviews: {canceled_reviews['order_id'].nunique()}")

print("\nUnavailable total:", len(unavailable))
unavail_items = items[items['order_id'].isin(unavailable['order_id'])]
print(f"Unavailable with items: {unavail_items['order_id'].nunique()} ({len(unavail_items)} items)")
unavail_payments = payments[payments['order_id'].isin(unavailable['order_id'])]
print(f"Unavailable with payments: {unavail_payments['order_id'].nunique()}")
unavail_reviews = reviews[reviews['order_id'].isin(unavailable['order_id'])]
print(f"Unavailable with reviews: {unavail_reviews['order_id'].nunique()}")

# Missing reviews in delivered orders
delivered = orders[orders['order_status'] == 'delivered']
delivered_with_rev = reviews[reviews['order_id'].isin(delivered['order_id'])]
missing_rev_count = len(delivered) - delivered_with_rev['order_id'].nunique()
print(f"\nDelivered orders total: {len(delivered):,}")
print(f"Delivered with review: {delivered_with_rev['order_id'].nunique():,}")
print(f"Missing reviews in delivered orders: {missing_rev_count:,} ({missing_rev_count/len(delivered)*100:.2f}%)")

