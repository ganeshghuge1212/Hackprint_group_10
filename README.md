# 📊 Retail Sales Intelligence & Profitability Analysis

## 🔍 Project Overview
This project builds a **comprehensive analytical framework** to extract actionable business insights from retail sales data.  
It demonstrates **data engineering, exploratory data analysis (EDA), feature engineering, and business intelligence visualization** using Python.

The analysis focuses on:
- Revenue & profit calculation
- Category and item-level performance
- Loss and wastage analysis
- Correlation and outlier detection
- Interactive dashboard using Streamlit

---

## 📁 Dataset Description
The project uses **four CSV files**:

| File Name | Description |
|---------|------------|
| `annex1.csv` | Item master data (Item Code, Item Name, Category) |
| `annex2.csv` | Daily retail sales transactions |
| `annex3.csv` | Wholesale prices by item and date |
| `annex4.csv` | Loss rate (%) per item |

---

## ⚙️ Tech Stack
- **Python**
- **Pandas & NumPy** – Data processing
- **Matplotlib & Seaborn** – Visualization
- **Streamlit** – Interactive dashboard

---

## 🧱 Project Workflow

### 1️⃣ Data Ingestion & Cleaning
- Load multiple CSV datasets
- Convert date columns to datetime format
- Remove invalid sales records (zero or negative quantity)
- Handle missing values implicitly during merging

---

### 2️⃣ Data Integration (Core Step)
Merged datasets using:
- `Item Code`
- `Date`
- `Item Name`

Final integrated dataset includes:
- Item details
- Sales data
- Wholesale prices
- Loss rates

---

### 3️⃣ Feature Engineering
Derived business-critical metrics:
- **Revenue**
- **Cost**
- **Profit**
- **Loss Quantity**

Formulas used:
```text
Revenue = Quantity Sold × Unit Selling Price
Cost    = Quantity Sold × Wholesale Price
Profit  = Revenue − Cost
Loss Qty = Quantity Sold × Loss Rate
