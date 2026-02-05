#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

items = pd.read_csv("annex1.csv")
sales = pd.read_csv("annex2.csv")
wholesale = pd.read_csv("annex3.csv")
loss = pd.read_csv("annex4.csv")


# In[3]:


items.info()
print("******************")
sales.info()
print("******************")
wholesale.info()
print("******************")
loss.info()


# In[4]:


sales['Date'] = pd.to_datetime(sales['Date'])
wholesale['Date'] = pd.to_datetime(wholesale['Date'])


# In[5]:


# Check missing values
sales.isnull().sum()


# In[6]:


# Remove zero or negative quantity
sales = sales[sales['Quantity Sold (kilo)'] > 0]


# ## Data Integration (MOST IMPORTANT STEP)

# In[7]:


# Merge item info
df = sales.merge(items, on="Item Code", how="left")

# Merge wholesale price
df = df.merge(wholesale, on=["Item Code", "Date"], how="left")

# Merge loss rate
df = df.merge(loss, on=["Item Code", "Item Name"], how="left")


# ## Feature Engineering

# In[8]:


# Revenue
df['Revenue'] = df['Quantity Sold (kilo)'] * df['Unit Selling Price (RMB/kg)']

# Cost
df['Cost'] = df['Quantity Sold (kilo)'] * df['Wholesale Price (RMB/kg)']

# Profit
df['Profit'] = df['Revenue'] - df['Cost']

# Loss quantity
df['Loss Quantity'] = df['Quantity Sold (kilo)'] * (df['Loss Rate (%)'] / 100)


# ## EXPLORATORY DATA ANALYSIS (EDA)

# In[9]:


# Overall Business Metrics

# In[11]:


df[['Revenue', 'Cost', 'Profit']].sum()


# In[12]:


# Category-Level Performance
category_perf = df.groupby('Category Name')[['Revenue','Profit']].sum()
category_perf.sort_values('Revenue', ascending=False)


# Note : Leaf vegetables generate highest revenue but lower margins.

# ## Correlation Analysis

# In[13]:


import seaborn as sns
import matplotlib.pyplot as plt

num_cols = ['Quantity Sold (kilo)', 
            'Unit Selling Price (RMB/kg)', 
            'Wholesale Price (RMB/kg)', 
            'Profit']

sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Analysis")
plt.show()


# Note : 
# Hypothesis:
# 
# Higher selling price → higher profit
# 
# Wholesale price strongly impacts margin

# In[15]:


## Outlier Detection (IQR Method)
Q1 = df['Quantity Sold (kilo)'].quantile(0.25)
Q3 = df['Quantity Sold (kilo)'].quantile(0.75)
IQR = Q3 - Q1

df_outliers = df[
    (df['Quantity Sold (kilo)'] < Q1 - 1.5*IQR) |
    (df['Quantity Sold (kilo)'] > Q3 + 1.5*IQR)
]


# Note : ✔ Explain:
# 
# “Extreme bulk purchases or data errors are flagged as anomalies.”

# ## Loss Analysis 

# In[16]:


loss_analysis = df.groupby('Item Name')['Loss Quantity'].sum()\
                  .sort_values(ascending=False)\
                  .head(10)
loss_analysis


# Note : ✔ Business Meaning:
# 
# High-loss items need supply chain or pricing intervention.

# # 3️⃣ STRATEGIC INSIGHTS & VISUALIZATION

# ### Revenue Trend Over Time

# In[17]:


daily_revenue = df.groupby('Date')['Revenue'].sum()

daily_revenue.plot(figsize=(10,4), title="Daily Revenue Trend")
plt.ylabel("Revenue (RMB)")
plt.show()


# ### Top 10 Profitable Items

# In[18]:


top_items = df.groupby('Item Name')['Profit'].sum()\
              .sort_values(ascending=False)\
              .head(10)

top_items.plot(kind='barh', title="Top 10 Profitable Items")
plt.show()


# ### Interactive Dashboard

# In[19]:


import streamlit as st

st.title("📊 Retail Sales Intelligence Dashboard")

st.metric("Total Revenue (RMB)", f"{df['Revenue'].sum():,.0f}")
st.metric("Total Profit (RMB)", f"{df['Profit'].sum():,.0f}")

category = st.selectbox("Select Category", df['Category Name'].unique())
filtered = df[df['Category Name'] == category]

st.bar_chart(filtered.groupby('Item Name')['Revenue'].sum())


# In[ ]:



