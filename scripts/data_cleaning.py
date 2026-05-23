"""
=============================================================
ApexPlanet Data Analytics Internship - Task 1
Data Immersion & Wrangling — Cleaning Script
Dataset: E-Commerce Orders (India) 2023-2024
=============================================================
"""

import pandas as pd
import os
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(BASE_DIR, 'outputs'), exist_ok=True)
import numpy as np
import re
from datetime import datetime

# ── 1. LOAD ────────────────────────────────────────────────
RAW_PATH     = os.path.join(BASE_DIR, 'data',    'ecommerce_orders.csv')
OUTPUT_PATH  = os.path.join(BASE_DIR, 'outputs', 'cleaned_ecommerce_orders.csv')
REPORT_PATH  = os.path.join(BASE_DIR, 'outputs', 'cleaning_report.txt')

df_raw = pd.read_csv(RAW_PATH)
report_lines = []

def log(msg):
    print(msg)
    report_lines.append(msg)

log("=" * 60)
log("DATA CLEANING REPORT — E-Commerce Orders Dataset")
log(f"Run timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log("=" * 60)
log(f"\n[RAW]  Shape : {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")

df = df_raw.copy()

# ── 2. INITIAL PROFILING ───────────────────────────────────
log("\n--- 2. INITIAL PROFILING ---")
log(f"\nColumn dtypes:\n{df.dtypes.to_string()}")

missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
log(f"\nMissing values:\n{pd.concat([missing, missing_pct], axis=1, keys=['Count','%']).to_string()}")

dup_count = df.duplicated().sum()
log(f"\nDuplicate rows : {dup_count}")

log(f"\nNumerical summary:\n{df.describe().T.to_string()}")

# ── 3. REMOVE DUPLICATES ───────────────────────────────────
log("\n--- 3. DUPLICATES ---")
before = len(df)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
log(f"Removed {before - len(df)} duplicate rows. Remaining: {len(df)}")

# ── 4. STANDARDISE DATE COLUMNS ───────────────────────────
log("\n--- 4. DATE STANDARDISATION ---")

def parse_date_flexible(val):
    if pd.isnull(val):
        return pd.NaT
    val = str(val).strip()
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%m-%d-%Y'):
        try:
            return datetime.strptime(val, fmt)
        except ValueError:
            continue
    return pd.NaT

df['order_date']    = df['order_date'].apply(parse_date_flexible)
df['delivery_date'] = pd.to_datetime(df['delivery_date'], errors='coerce')

bad_dates = df['order_date'].isna().sum()
log(f"order_date unparseable (set to NaT): {bad_dates}")
log(f"delivery_date missing (NaN / not yet delivered): {df['delivery_date'].isna().sum()}")

# ── 5. STANDARDISE GENDER ─────────────────────────────────
log("\n--- 5. GENDER STANDARDISATION ---")
gender_map = {
    'male': 'Male', 'm': 'Male',
    'female': 'Female', 'f': 'Female',
    'other': 'Other', 'o': 'Other',
}

def clean_gender(val):
    if pd.isnull(val):
        return np.nan
    return gender_map.get(str(val).strip().lower(), str(val).strip().title())

before_vals = df['customer_gender'].value_counts().to_dict()
df['customer_gender'] = df['customer_gender'].apply(clean_gender)
after_vals  = df['customer_gender'].value_counts().to_dict()
log(f"Before: {before_vals}")
log(f"After : {after_vals}")

# ── 6. FIX DISCOUNT OUTLIERS ──────────────────────────────
log("\n--- 6. DISCOUNT CLEANING ---")
neg_disc = (df['discount'] < 0).sum()
df.loc[df['discount'] < 0, 'discount'] = 0.0
log(f"Negative discount rows corrected: {neg_disc}")

above_disc = (df['discount'] > 1).sum()
df.loc[df['discount'] > 1, 'discount'] = 1.0
log(f"Discount > 1 clamped: {above_disc}")

# ── 7. FIX PRICE / REVENUE OUTLIERS ──────────────────────
log("\n--- 7. PRICE & REVENUE CLEANING ---")
price_q99 = df['unit_price'].quantile(0.99)
price_outliers = (df['unit_price'] > price_q99).sum()
log(f"unit_price 99th pct threshold : ₹{price_q99:,.2f}")
log(f"Extreme price outliers (>99th pct) : {price_outliers} rows")
# Flag but keep — may be genuine high-value electronics
df['is_price_outlier'] = df['unit_price'] > price_q99

zero_rev = (df['revenue'] == 0).sum()
log(f"Zero-revenue rows : {zero_rev}  → recalculating revenue")
df['revenue'] = np.round(df['unit_price'] * df['quantity'] * (1 - df['discount']), 2)

# ── 8. HANDLE MISSING VALUES ──────────────────────────────
log("\n--- 8. MISSING VALUE IMPUTATION ---")
# customer_age → fill with median grouped by category
age_before = df['customer_age'].isna().sum()
df['customer_age'] = df.groupby('category')['customer_age'].transform(
    lambda x: x.fillna(x.median())
)
df['customer_age'] = df['customer_age'].fillna(df['customer_age'].median())
df['customer_age'] = df['customer_age'].round(0).astype(int)
log(f"customer_age: filled {age_before} NaNs with group/global median")

rating_before = df['customer_rating'].isna().sum()
df['customer_rating'] = df['customer_rating'].fillna(df['customer_rating'].median())
log(f"customer_rating: filled {rating_before} NaNs with global median ({df['customer_rating'].median()})")

# return_reason → fill N/A for non-returned orders
df['return_reason'] = df.apply(
    lambda r: r['return_reason'] if r['order_status'] == 'Returned' else 'N/A',
    axis=1
)
log("return_reason: set to 'N/A' for non-Returned orders")

# ── 9. FEATURE ENGINEERING ────────────────────────────────
log("\n--- 9. FEATURE ENGINEERING ---")

# Age group
bins   = [0, 25, 35, 45, 55, 100]
labels = ['18-25', '26-35', '36-45', '46-55', '56+']
df['age_group'] = pd.cut(df['customer_age'], bins=bins, labels=labels, right=True)
log("Created: age_group")

# Days to delivery
df['days_to_delivery'] = (df['delivery_date'] - df['order_date']).dt.days
log("Created: days_to_delivery")

# Order month / year / quarter
df['order_year']    = df['order_date'].dt.year
df['order_month']   = df['order_date'].dt.month
df['order_quarter'] = df['order_date'].dt.quarter
log("Created: order_year, order_month, order_quarter")

# Revenue band
rev_bins   = [0, 500, 2000, 10000, 1_000_000]
rev_labels = ['Low (<500)', 'Medium (500-2K)', 'High (2K-10K)', 'Premium (10K+)']
df['revenue_band'] = pd.cut(df['revenue'], bins=rev_bins, labels=rev_labels)
log("Created: revenue_band")

# Is_cancelled flag
df['is_cancelled'] = df['order_status'] == 'Cancelled'
log("Created: is_cancelled")

# ── 10. DATA TYPE ENFORCEMENT ─────────────────────────────
log("\n--- 10. DATA TYPES ---")
df['is_first_order'] = df['is_first_order'].astype(bool)
df['is_cancelled']   = df['is_cancelled'].astype(bool)
df['quantity']       = df['quantity'].astype(int)
log("Enforced bool for is_first_order, is_cancelled; int for quantity")

# ── 11. FINAL STATE ───────────────────────────────────────
log("\n--- 11. FINAL DATASET ---")
log(f"Shape : {df.shape[0]} rows × {df.shape[1]} columns")
log(f"Remaining NaNs:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string()}")
log(f"\nNew columns added: {set(df.columns) - set(df_raw.columns)}")

df.to_csv(OUTPUT_PATH, index=False)
log(f"\n✅ Cleaned dataset saved → {OUTPUT_PATH}")

with open(REPORT_PATH, 'w') as f:
    f.write('\n'.join(report_lines))
log(f"✅ Cleaning report saved → {REPORT_PATH}")
