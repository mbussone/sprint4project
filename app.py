#Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('vehicles_us.csv')

#convert date_posted to date type
df['date_posted']=pd.to_datetime(df['date_posted'])

#get manufacturer
df['manufacturer'] = df['model'].apply(lambda x:x.split()[0])


# Title
st.title("Car Sales Dashboard")

fig_hist = px.histogram(df, x='price', title='Price Distribution', color='condition')
st.plotly_chart(fig_hist)

fig = px.histogram(df, x='days_listed', title='Days Listed Distribution', color='condition')
st.plotly_chart(fig)

fig = px.histogram(df, x='model_year', title='Model Year Distribution', color='condition')
st.plotly_chart(fig)

st.header("Manufacturer", anchor=None, help=None, divider="blue")
fig = px.histogram(df, x='manufacturer', title='Manufacturer Distribution')
st.write(fig)
st.header('Vehicle types by Manufacturer')
fig = px.histogram(df, x='manufacturer', color='type')
st.write(fig)
fig_scatter = px.scatter(df, x='manufacturer', y='price', title='Price vs Manufacturer')
st.plotly_chart(fig_scatter)
fig_scatter = px.scatter(df, x='manufacturer', y='days_listed', title='Days Listed vs Manufacturer')
st.plotly_chart(fig_scatter)


fig_scatter = px.scatter(df, x='odometer', y='price', title='Price vs Odometer')
st.plotly_chart(fig_scatter)

st.header('Histogram of condition vs model year')
fig = px.histogram(df, x='model_year', color='condition')
st.write(fig)

st.header('Compare price distribution between manufacturers')
# get a list of car manufacturers
manufac_list = sorted(df['manufacturer'].unique())
# get user's inputs from a dropdown menu
manufacturer_1 = st.selectbox(
                              label='Select manufacturer 1', # title of the select box
                              options=manufac_list, # options listed in the select box
                              index=manufac_list.index('chevrolet') # default pre-selected option
                              )
# repeat for the second dropdown menu
manufacturer_2 = st.selectbox(
                              label='Select manufacturer 2',
                              options=manufac_list, 
                              index=manufac_list.index('hyundai')
                              )
# filter the dataframe 
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay')

# display the figure with streamlit
st.write(fig)

if st.checkbox('Influence of Color'):
    st.header("Influence of Color", anchor=None, help=None, divider="blue")
    fig = px.histogram(df, x='paint_color', title='Color Distribution')
    st.plotly_chart(fig)
    fig_scatter = px.scatter(df, x='paint_color', y='price', title='Price vs Color')
    st.plotly_chart(fig_scatter)
    fig_scatter = px.scatter(df, x='paint_color', y='days_listed', title='Days Listed vs Color')
    st.plotly_chart(fig_scatter)

if st.checkbox('Show raw data'):
    st.header("Raw Data", anchor=None, help=None, divider="gray")
    st.write(df)