🧹 Task 1: Data Immersion & Wrangling - Sales Dataset
📌 Objective
The objective of this project is to understand, clean, and prepare a real-world sales dataset for analysis. Data wrangling is an essential first step in any data analytics workflow.

📊 Dataset
This project uses a Sales Transactions Dataset, which contains business-related data such as:

Customer information (Name, Gender, Date of Birth, Age)
Product details (Product, Category)
Sales and revenue data (Unit Price, Quantity, Discount, Net Revenue)
Geographic data (Region)
Transaction details (Date, Payment Method, Customer Rating)


🔍 Steps Performed
1. Data Understanding

Loaded dataset using Python
Explored structure and column details
Analyzed dataset using .head(), .info(), .describe()

2. Data Quality Assessment

Checked for missing values (Gender 6%, Region 6%, Quantity 3.7%, Unit Price 4.5%)
Identified and counted duplicate records (8 duplicates found)
Detected inconsistent formatting in text and date columns

3. Data Cleaning

Removed 8 duplicate rows
Standardized inconsistent text values (M/F → Male/Female, mixed casing in Category, Region)
Filled missing values with median or default values
Parsed multiple date formats into a single standard format

4. Feature Engineering

Created new columns:

Customer_Age = Derived from Date of Birth
Age_Group = Binned age categories (18–25, 26–35, 36–45, 46–60, 60+)
Gross_Revenue = Quantity × Unit Price
Discount_Amount = Gross Revenue × Discount Percentage
Net_Revenue = Gross Revenue − Discount Amount
Transaction_Year, Month, Quarter, DayOfWeek = Extracted from Transaction Date
Is_High_Value = True if Net Revenue > 75th percentile




🛠️ Tools & Technologies

Python
Pandas
NumPy


📁 Project Structure
Task1-DataWrangling/
│
├── data/
│   └── raw_sales_data.csv
│
├── scripts/
│   ├── generate_dataset.py
│   └── data_cleaning.py
│
├── output/
│   ├── cleaned_sales_data.csv
│   └── summary_statistics.csv
│
├── data_dictionary.md
├── task1.py
└── README.md

📈 Output

Cleaned dataset with 507 rows × 24 columns ready for analysis
Summary statistics of key numerical columns
Organized project structure for reproducibility


🚀 Conclusion
This project demonstrates the importance of data preprocessing and cleaning before performing any analysis. It ensures that the dataset is accurate, consistent, and ready for further steps like EDA and visualization.

🔗 Author
Devi Sri

*ApexPlanet Software Pvt. Ltd. | www.apexplanet.in*
