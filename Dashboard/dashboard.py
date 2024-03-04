import pandas as pd
import pickle
from PIL import Image
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from IPython.display import display

px.defaults.template = 'plotly_dark'
px.defaults.color_continuous_scale = 'reds'

img = Image.open("Dashboard/grocery.jpg")
st.sidebar.image(img)

# Membuka file
csv_path = "Dashboard/all_data.csv"
data = pd.read_csv(csv_path)

datetime_columns = ["order_delivered_customer_date", "order_delivered_carrier_date"]
data.sort_values(by="order_delivered_customer_date", inplace=True)
data.reset_index(inplace=True)
 
for column in datetime_columns:
    data[column] = pd.to_datetime(data[column])

min_date = data["order_delivered_customer_date"].min()
max_date = data["order_delivered_customer_date"].max()
start_date, end_date = st.sidebar.date_input(
    label='Order Delivered Customer Date', min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

orders = data[(data["order_delivered_customer_date"] >= str(start_date)) & 
                (data["order_delivered_customer_date"] <= str(end_date))]


st.header('Dicoding Orders Dataset Dashboard :sparkles:')

st.subheader('Category of Shipping')
def sum_order_items_df(orders):
    sum_order_items_df = orders.groupby("Category").Delivery_time.sum().sort_values(ascending=False).reset_index()
    sum_order_items_df.head()

sum_order_items_df = orders.groupby("Category").Delivery_time.sum().sort_values(ascending=False).reset_index()
sum_order_items_df.head()
display(sum_order_items_df)

df = pd.DataFrame({
    'Category': ['Overtime Shipping', 'Standard Shipping', 'No Shipping'],
    'Delivery_time': [769291, 159397, -372207],
})
st.table(data=df)


st.subheader("Plot Based on Shipping Category")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3"]

sns.barplot(x="Delivery_time", y="Category", data=sum_order_items_df.head(), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Left Side", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="Delivery_time", y="Category", data=sum_order_items_df.sort_values(by="Delivery_time", ascending=True).head(), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Right Side", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.subheader("Delivery Times Trended")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    orders['Delivery_time'],
    marker='o',
    linewidth=10,
    color="#90CAF9"
)
ax.tick_params(axis='y')
ax.tick_params(axis='x')
 
st.pyplot(fig)
