import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

n = 5000

def rand_date(start, end, n):
    delta = (end - start).days
    return [start + timedelta(days=random.randint(0, delta)) for _ in range(n)]

categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys']
subcategories = {
    'Electronics':    ['Smartphones', 'Laptops', 'Headphones', 'Cameras', 'Tablets'],
    'Clothing':       ['Men Shirts', 'Women Tops', 'Jeans', 'Dresses', 'Jackets'],
    'Home & Kitchen': ['Cookware', 'Bedding', 'Furniture', 'Lighting', 'Decor'],
    'Books':          ['Fiction', 'Non-Fiction', 'Educational', 'Comics', 'Biography'],
    'Sports':         ['Gym Equipment', 'Cycling', 'Swimming', 'Running', 'Yoga'],
    'Beauty':         ['Skincare', 'Haircare', 'Makeup', 'Fragrance', 'Wellness'],
    'Toys':           ['Action Figures', 'Board Games', 'Educational', 'Dolls', 'Outdoor'],
}
payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Wallet', 'COD']
cities = ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Surat']
states = {'Mumbai':'Maharashtra','Delhi':'Delhi','Bengaluru':'Karnataka','Chennai':'Tamil Nadu',
          'Hyderabad':'Telangana','Pune':'Maharashtra','Kolkata':'West Bengal',
          'Ahmedabad':'Gujarat','Jaipur':'Rajasthan','Surat':'Gujarat'}
statuses = ['Delivered', 'Shipped', 'Cancelled', 'Returned', 'Processing']
status_probs = [0.65, 0.12, 0.10, 0.08, 0.05]
channels = ['Mobile App', 'Website', 'Social Media', 'Email Campaign', 'Referral']
genders = ['Male', 'Female', 'Other']

cats = [random.choice(categories) for _ in range(n)]
subcats = [random.choice(subcategories[c]) for c in cats]
order_dates = rand_date(datetime(2023, 1, 1), datetime(2024, 12, 31), n)
delivery_dates = [d + timedelta(days=random.randint(1, 10)) if random.random() > 0.18 else None for d in order_dates]
city_choices = [random.choice(cities) for _ in range(n)]

unit_prices = np.round(np.random.uniform(50, 15000, n), 2)
unit_prices[np.random.choice(n, 30, replace=False)] = np.round(np.random.uniform(50000, 200000, 30), 2)

quantities = np.random.randint(1, 6, n)
discounts = np.round(np.random.uniform(0, 0.4, n), 2)
discounts[np.random.choice(n, 20, replace=False)] = -0.05

revenue = np.round(unit_prices * quantities * (1 - discounts), 2)
revenue[np.random.choice(n, 15, replace=False)] = 0

ages = np.random.randint(18, 70, n).astype(float)
ages[np.random.choice(n, 200, replace=False)] = np.nan

ratings = np.random.choice([1,2,3,4,5], n, p=[0.05,0.10,0.20,0.35,0.30]).astype(float)
ratings[np.random.choice(n, 150, replace=False)] = np.nan

customer_ids = ['CUST' + str(np.random.randint(1000, 4000)).zfill(4) for _ in range(n)]
product_ids  = ['PROD' + str(np.random.randint(100, 600)).zfill(4) for _ in range(n)]
order_ids    = ['ORD' + str(i+10000) for i in range(n)]

dup_idx = np.random.choice(n, 80, replace=False)

order_date_strs = []
for i, d in enumerate(order_dates):
    if i % 7 == 0:
        order_date_strs.append(d.strftime('%d/%m/%Y'))
    elif i % 11 == 0:
        order_date_strs.append(d.strftime('%Y/%m/%d'))
    else:
        order_date_strs.append(d.strftime('%Y-%m-%d'))

delivery_date_strs = [d.strftime('%Y-%m-%d') if d else None for d in delivery_dates]

gender_raw = [random.choice(genders) for _ in range(n)]
for i in range(n):
    if random.random() < 0.05:
        gender_raw[i] = random.choice(['M', 'F', 'male', 'FEMALE', 'o'])

df = pd.DataFrame({
    'order_id':        order_ids,
    'customer_id':     customer_ids,
    'product_id':      product_ids,
    'order_date':      order_date_strs,
    'delivery_date':   delivery_date_strs,
    'category':        cats,
    'sub_category':    subcats,
    'product_name':    [f"{sc} - Model {random.randint(100,999)}" for sc in subcats],
    'unit_price':      unit_prices,
    'quantity':        quantities,
    'discount':        discounts,
    'revenue':         revenue,
    'payment_method':  [random.choice(payment_methods) for _ in range(n)],
    'order_status':    np.random.choice(statuses, n, p=status_probs),
    'city':            city_choices,
    'state':           [states[c] for c in city_choices],
    'customer_age':    ages,
    'customer_gender': gender_raw,
    'customer_rating': ratings,
    'acquisition_channel': [random.choice(channels) for _ in range(n)],
    'is_first_order':  [random.choice([True, False]) for _ in range(n)],
    'return_reason':   [random.choice(['Defective', 'Wrong Item', 'Not as Described', None, None, None]) for _ in range(n)],
})

dups = df.iloc[dup_idx].copy()
df = pd.concat([df, dups], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

import os
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ecommerce_orders.csv')
df.to_csv(out_path, index=False)
print(f"Dataset: {len(df)} rows x {len(df.columns)} cols")
print(f"Saved to: {out_path}")
