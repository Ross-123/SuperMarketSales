#!/usr/bin/env python
# coding: utf-8

# In[2]:


from email.policy import default
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime


# In[ ]:


st.set_page_config(page_title = "Sales Dashboard", page_icon=":bar_char:", layout="wide")


# In[3]:


##Read excel file
df = pd.read_excel(r"C:\Users\HP\Downloads\supermarket_sales.xlsx")
engine = "openpyxl"
sheet_name = "Orders"
skiprows = 2
usecols = "A:Q"

#Create month column to separate month from Datetime
df['Month'] = df['Date'].dt.month
df.head()


#--Sidebars--
st.sidebar.header("Please Filter Here")
City = st.sidebar.multiselect(
    "Select the city:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

Customer_Type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_Type"].unique(),
    default=df["Customer_Type"].unique()
)

Gender= st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @City & Customer_Type == @Customer_Type & Gender == @Gender"
)

# KPI on MAin Page
st.title("Bar_Chart: Sales Dashboard")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean())
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("________")

st.dataframe(df_selection)


#Total sales group by city & month
df1=df.groupby(['City','Month'])['Total'].sum().reset_index()

st.dataframe(df1)

#Create the plot
fig = px.bar(df1, x='City', y='Total',
                 title= "Sales by City", color="City", hover_name="City",
                 animation_frame="Month",animation_group="City")
                

fig.update_layout(showlegend=True, width=800,legend_title_font_color="black",title_font_color="blue",title_font_size=26,
legend=dict(
        x=0,
        y=1,
        traceorder="reversed",
        title_font_family="Times New Roman",
        font=dict(
            family="Courier",
            size=12,
            color="black"
        ),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2
    )
)
st.write(fig)



