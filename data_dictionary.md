# Data Dictionary — E-Commerce Orders Dataset (India)

**Dataset Name:** `ecommerce_orders.csv`  
**Domain:** Indian E-Commerce (B2C Retail)  
**Period Covered:** January 2023 – December 2024  
**Total Records (raw):** 5,080 rows | **After Cleaning:** 5,000 rows  
**Total Columns (raw):** 22 | **After Feature Engineering:** 30  

---

## Original Columns

| # | Column Name | Data Type | Description | Business Relevance |
|---|-------------|-----------|-------------|-------------------|
| 1 | `order_id` | String | Unique identifier for each order (e.g., `ORD10001`) | Primary key; used to join or count orders |
| 2 | `customer_id` | String | Unique identifier for each customer (e.g., `CUST1042`) | Enables customer-level analysis; repeat purchase tracking |
| 3 | `product_id` | String | Unique identifier for each product (e.g., `PROD0234`) | SKU-level revenue & return analysis |
| 4 | `order_date` | Date (YYYY-MM-DD after cleaning) | Date the order was placed | Trend analysis, seasonality, cohort formation |
| 5 | `delivery_date` | Date (YYYY-MM-DD) | Actual delivery date; NULL if not yet delivered | SLA tracking; correlates with customer satisfaction |
| 6 | `category` | String (Categorical) | Top-level product category (e.g., Electronics, Clothing) | Revenue segmentation; category performance |
| 7 | `sub_category` | String (Categorical) | More granular product type within a category | Detailed merchandise analysis |
| 8 | `product_name` | String | Human-readable product name | Display / filtering; not used for aggregations |
| 9 | `unit_price` | Float (₹) | Listed price of one unit before discount | Revenue calculation; price elasticity studies |
| 10 | `quantity` | Integer | Number of units ordered | Volume metrics; basket size analysis |
| 11 | `discount` | Float (0.0–1.0) | Fractional discount applied (e.g., 0.20 = 20% off) | Margin impact; promotional effectiveness |
| 12 | `revenue` | Float (₹) | Actual revenue = unit_price × quantity × (1 – discount) | Core KPI; P&L basis |
| 13 | `payment_method` | String (Categorical) | Mode of payment (Credit Card, UPI, COD, etc.) | Payment trend; fraud signal; operational cost |
| 14 | `order_status` | String (Categorical) | Current status: Delivered / Shipped / Cancelled / Returned / Processing | Operations KPI; cancellation & return rate |
| 15 | `city` | String | Customer's city | Geographic demand analysis |
| 16 | `state` | String | Customer's state (derived from city) | Regional reporting; logistics planning |
| 17 | `customer_age` | Integer | Customer's age in years (4% missing → median-imputed) | Demographic segmentation |
| 18 | `customer_gender` | String (Categorical) | Male / Female / Other (standardised from multiple raw formats) | Gender-based purchase pattern analysis |
| 19 | `customer_rating` | Float (1–5) | Post-delivery satisfaction rating (3% missing → median-imputed) | NPS proxy; product/service quality signal |
| 20 | `acquisition_channel` | String (Categorical) | How the customer first arrived (Mobile App, Website, etc.) | Marketing attribution; CAC analysis |
| 21 | `is_first_order` | Boolean | True if this is the customer's very first order | New vs. returning customer segmentation |
| 22 | `return_reason` | String (Categorical) | Reason for return if applicable: Defective / Wrong Item / Not as Described | Returns analysis; quality improvement |

---

## Engineered Columns (Added During Cleaning)

| # | Column Name | Derived From | Description | Business Use |
|---|-------------|-------------|-------------|--------------|
| 23 | `age_group` | `customer_age` | Bucketed age band: 18-25 / 26-35 / 36-45 / 46-55 / 56+ | Generational marketing |
| 24 | `days_to_delivery` | `delivery_date` – `order_date` | Number of calendar days from order to delivery | Logistics KPI; customer experience |
| 25 | `order_year` | `order_date` | Extracted year (2023 or 2024) | Year-over-year comparison |
| 26 | `order_month` | `order_date` | Extracted month (1–12) | Seasonality; monthly trend |
| 27 | `order_quarter` | `order_date` | Extracted quarter (Q1–Q4) | Quarterly business review |
| 28 | `revenue_band` | `revenue` | Low (<₹500) / Medium (₹500–2K) / High (₹2K–10K) / Premium (₹10K+) | Basket value segmentation |
| 29 | `is_cancelled` | `order_status` | Boolean flag — True if order_status == 'Cancelled' | Quick cancellation filter |
| 30 | `is_price_outlier` | `unit_price` | True if unit_price > 99th percentile (₹14,936) | Outlier-aware analysis |

---

## Data Quality Issues Found & Resolved

| Issue | Column(s) | Count | Resolution |
|-------|-----------|-------|-----------|
| Duplicate rows | All | 80 | Removed |
| Inconsistent date formats (DD/MM/YYYY, YYYY/MM/DD) | `order_date` | ~857 rows | Parsed flexibly → standardised to YYYY-MM-DD |
| Missing delivery dates | `delivery_date` | 897 (17.7%) | Kept as NaT — orders not yet delivered |
| Missing ages | `customer_age` | 204 (4.0%) | Imputed with category-group median |
| Missing ratings | `customer_rating` | 153 (3.0%) | Imputed with global median (4.0) |
| Inconsistent gender labels (M, F, male, FEMALE, o) | `customer_gender` | ~278 rows | Mapped to Male / Female / Other |
| Negative discounts (data entry errors) | `discount` | 20 | Clamped to 0.0 |
| Zero-revenue rows | `revenue` | 15 | Recalculated from unit_price × qty × (1–discount) |
| Extreme price outliers (>₹50,000) | `unit_price` | 30 raw | Flagged via `is_price_outlier`; retained (may be genuine high-value items) |

---

## Categorical Value Enumerations

| Column | Valid Values |
|--------|-------------|
| `category` | Electronics, Clothing, Home & Kitchen, Books, Sports, Beauty, Toys |
| `payment_method` | Credit Card, Debit Card, UPI, Net Banking, Wallet, COD |
| `order_status` | Delivered, Shipped, Cancelled, Returned, Processing |
| `acquisition_channel` | Mobile App, Website, Social Media, Email Campaign, Referral |
| `age_group` | 18-25, 26-35, 36-45, 46-55, 56+ |
| `revenue_band` | Low (<500), Medium (500-2K), High (2K-10K), Premium (10K+) |
| `return_reason` | Defective, Wrong Item, Not as Described, N/A (non-returned orders) |

---

*Prepared as part of ApexPlanet Data Analytics Internship — Task 1: Data Immersion & Wrangling*
