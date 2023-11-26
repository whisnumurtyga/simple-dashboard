# ===>  Import   <===
import pandas as pd
import matplotlib
matplotlib.use('agg')  # Menggunakan backend non-interactive
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_style('white')
# ===>  End Import   <===



# ===>  Function   <===
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_approved_at').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return daily_orders_df


def create_category_product_trend_df(df):
    category_product_trend_df = df.groupby('product_category_name_english').size().reset_index(name='total')
    category_product_trend_df.rename(columns={'product_category_name_english': 'product_category_name'}, inplace=True)
    
    category_product_trend_df = category_product_trend_df.reset_index()
    category_product_trend_df.rename(columns={
        'product_category_name_english' : 'product_category_name',
        'count' : 'total'
    }, inplace=True)
    
    return category_product_trend_df


def create_customer_demography_df(df):
    category_product_trend_df = df.groupby('customer_state').size().reset_index(name='total')
    return category_product_trend_df
# ===>  End Function   <===



# ===>  Setup   <===
all_df = pd.read_csv("../Dashboard/main_data.csv")

datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()
# ===>  End Setup   <===



# ===>  Dashboard   <=== 
# =>  Sidebar   <=
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/94/Old_Nike_logo.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
# =>  End Sidebar   <=


# =>    Filter      <=
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                (all_df["order_approved_at"] <= str(end_date))]
# =>  End Filter   <=


# =>  Call Function   <=
daily_orders_df = create_daily_orders_df(main_df)
category_product_trend_df = create_category_product_trend_df(main_df)
customer_demography_df = create_customer_demography_df(main_df)
# =>  End Call Function   <=


st.header('Final Project Whisnumurty :sparkles:')


# =>  Daily Order - Metric   <=
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), 'USD', locale='en_US')
    st.metric("Total Revenue", value=total_revenue)
# =>    End Daily Order - Metric   <=    


# =>    Daily Order Line Chart   <=
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=5,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)
# =>    End Daily Order Line Chart   <=


# =>    Trend Product   <=
plt.figure(figsize=(12, 8))
sns.barplot(x='total', y='product_category_name', data=category_product_trend_df.head(5), palette='viridis')
plt.xlabel('Total')
plt.ylabel('Product Category')
plt.title('Product Category Trend')

fig = plt.gcf()

st.subheader("Top 5 Trend Product")
st.pyplot(fig)
# =>    End Trend Product   <=

# =>    Demografi Pelanggan   <=
plt.figure(figsize=(12, 8))
sns.barplot(x='total', y='customer_state', data=customer_demography_df.head(5), palette='viridis')
plt.xlabel('Total')
plt.ylabel('State')
plt.title('Customer State')

fig = plt.gcf()

st.subheader("Customer Trend by State")
st.pyplot(fig)
# =>    End Demografi Pelanggan   <=
# ===>  End Dashboard   <===