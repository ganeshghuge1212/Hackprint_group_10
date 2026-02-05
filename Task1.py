import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("📊 Retail Sales Intelligence Dashboard")

# ==============================
# DATA LOADING
# ==============================
@st.cache_data
def load_data():
    items = pd.read_csv("annex1.csv")
    sales = pd.read_csv("annex2.csv")
    wholesale = pd.read_csv("annex3.csv")
    loss = pd.read_csv("annex4.csv")

    sales['Date'] = pd.to_datetime(sales['Date'])
    wholesale['Date'] = pd.to_datetime(wholesale['Date'])

    # Remove zero or negative quantity
    sales = sales[sales['Quantity Sold (kilo)'] > 0]

    # Merge datasets
    df = sales.merge(items, on="Item Code", how="left")
    df = df.merge(wholesale, on=["Item Code", "Date"], how="left")
    df = df.merge(loss, on=["Item Code", "Item Name"], how="left")

    # Feature Engineering
    df['Revenue'] = df['Quantity Sold (kilo)'] * df['Unit Selling Price (RMB/kg)']
    df['Cost'] = df['Quantity Sold (kilo)'] * df['Wholesale Price (RMB/kg)']
    df['Profit'] = df['Revenue'] - df['Cost']
    df['Loss Quantity'] = df['Quantity Sold (kilo)'] * (df['Loss Rate (%)'] / 100)

    return df

df = load_data()

# ==============================
# BUSINESS METRICS
# ==============================
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue (RMB)", f"{df['Revenue'].sum():,.0f}")
col2.metric("Total Cost (RMB)", f"{df['Cost'].sum():,.0f}")
col3.metric("Total Profit (RMB)", f"{df['Profit'].sum():,.0f}")

# ==============================
# CATEGORY PERFORMANCE
# ==============================
st.subheader("Category Performance")

category_perf = df.groupby('Category Name')[['Revenue','Profit']].sum()
st.dataframe(category_perf.sort_values('Revenue', ascending=False))

# ==============================
# CORRELATION HEATMAP
# ==============================
st.subheader("Correlation Analysis")

num_cols = [
    'Quantity Sold (kilo)', 
    'Unit Selling Price (RMB/kg)', 
    'Wholesale Price (RMB/kg)', 
    'Profit'
]

fig, ax = plt.subplots()
sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# ==============================
# OUTLIER DETECTION
# ==============================
st.subheader("Outlier Detection")

Q1 = df['Quantity Sold (kilo)'].quantile(0.25)
Q3 = df['Quantity Sold (kilo)'].quantile(0.75)
IQR = Q3 - Q1

df_outliers = df[
    (df['Quantity Sold (kilo)'] < Q1 - 1.5*IQR) |
    (df['Quantity Sold (kilo)'] > Q3 + 1.5*IQR)
]

st.write("Outliers Found:", df_outliers.shape[0])
st.dataframe(df_outliers.head())

# ==============================
# LOSS ANALYSIS
# ==============================
st.subheader("Top Loss Items")

loss_analysis = df.groupby('Item Name')['Loss Quantity'].sum()\
                  .sort_values(ascending=False)\
                  .head(10)

st.bar_chart(loss_analysis)

# ==============================
# DAILY REVENUE TREND
# ==============================
st.subheader("Daily Revenue Trend")

daily_revenue = df.groupby('Date')['Revenue'].sum()

fig2, ax2 = plt.subplots()
daily_revenue.plot(ax=ax2)
st.pyplot(fig2)

# ==============================
# TOP PROFITABLE ITEMS
# ==============================
st.subheader("Top 10 Profitable Items")

top_items = df.groupby('Item Name')['Profit'].sum()\
              .sort_values(ascending=False)\
              .head(10)

st.bar_chart(top_items)

# ==============================
# INTERACTIVE FILTER
# ==============================
st.subheader("Interactive Category Dashboard")

category = st.selectbox("Select Category", df['Category Name'].unique())
filtered = df[df['Category Name'] == category]

st.bar_chart(filtered.groupby('Item Name')['Revenue'].sum())
