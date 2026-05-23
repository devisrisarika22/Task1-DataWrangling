# Task 1 — Data Immersion & Wrangling
### ApexPlanet Software Pvt. Ltd. | Data Analytics Internship (60 Days)

---

## Overview

This repository contains all deliverables for **Task 1** of the ApexPlanet Data Analytics Internship. The objective is to acquire a real-world dataset, profile it for quality issues, clean it systematically, perform feature engineering, and produce an analysis-ready output.

**Timeline:** 10 Days  
**Dataset:** Indian E-Commerce Orders — 2023 to 2024  

---

## Repository Structure

```
task1-data-immersion/
│
├── data/
│   └── ecommerce_orders.csv          ← Raw dataset (5,080 rows × 22 cols)
│
├── outputs/
│   ├── cleaned_ecommerce_orders.csv  ← Final cleaned dataset (5,000 rows × 30 cols)
│   └── cleaning_report.txt           ← Detailed log of every cleaning step
│
├── scripts/
│   └── data_cleaning.py              ← Main Python/Pandas cleaning script
│
├── data_dictionary.md                ← Column definitions, types & business relevance
└── README.md                         ← This file
```

---

## Dataset Description

| Property | Value |
|----------|-------|
| Domain | Indian B2C E-Commerce |
| Time Period | Jan 2023 – Dec 2024 |
| Raw Rows | 5,080 |
| Raw Columns | 22 |
| Cleaned Rows | 5,000 |
| Cleaned Columns | 30 (8 engineered) |

### Key Columns
- **Transactional:** `order_id`, `order_date`, `delivery_date`, `order_status`
- **Product:** `category`, `sub_category`, `product_name`, `unit_price`, `quantity`, `discount`, `revenue`
- **Customer:** `customer_id`, `customer_age`, `customer_gender`, `customer_rating`
- **Geographic:** `city`, `state`
- **Marketing:** `acquisition_channel`, `payment_method`, `is_first_order`

---

## Data Quality Issues Found

| Issue | Count | Action Taken |
|-------|-------|-------------|
| Duplicate rows | 80 | Removed |
| Inconsistent date formats | ~857 rows | Standardised to YYYY-MM-DD |
| Missing customer ages | 204 | Imputed with category-group median |
| Missing ratings | 153 | Imputed with global median (4.0) |
| Non-standard gender labels | ~278 | Mapped to Male / Female / Other |
| Negative discounts | 20 | Clamped to 0.0 |
| Zero-revenue rows | 15 | Recalculated from formula |
| Extreme price outliers | 30 | Flagged (`is_price_outlier`) — kept |

---

## How to Run

### Prerequisites
```bash
pip install pandas numpy
```

### Execute Cleaning Script
```bash
cd scripts/
python3 data_cleaning.py
```
Output files are written to `outputs/`.

---

## Key Engineered Features

| Feature | Description |
|---------|-------------|
| `age_group` | Customer age bucketed: 18-25, 26-35, 36-45, 46-55, 56+ |
| `days_to_delivery` | Calendar days from order to delivery |
| `order_year / month / quarter` | Date parts for time-series analysis |
| `revenue_band` | Low / Medium / High / Premium basket value |
| `is_cancelled` | Boolean flag for cancelled orders |
| `is_price_outlier` | Flags extreme unit prices (> 99th percentile) |

---

## Skills Demonstrated

- Pandas data loading and profiling
- Multi-format date parsing
- Categorical value standardisation
- Outlier detection and treatment
- Missing value imputation (group-based and global)
- Feature engineering (binning, date parts, flags)
- Reproducible, documented Python scripting

---

## Next Steps (Task 2 Preview)

With the cleaned dataset, Task 2 will focus on:
- Descriptive statistics and univariate distributions
- SQL-style business questions using Pandas
- Multivariate correlation analysis
- Static KPI dashboard mock-up

---

*ApexPlanet Software Pvt. Ltd. | www.apexplanet.in*
