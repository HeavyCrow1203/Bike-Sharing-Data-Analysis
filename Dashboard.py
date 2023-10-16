import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

hour_df = pd.read_csv('dataset/hour.csv')
print(hour_df.head())

st.set_page_config(
    page_title="Dashboard Bike Share Dataset",
    layout="wide"
)

# merubah nama kolom agar mudah terbaca
hour_df.rename(columns = {
    'instant' : 'rec_in',
    'dteday' : 'date',
    'yr' : 'year',
    'mnth' : 'month',
    'hr' : 'hour',
    'weathersit' : 'weather_condition',
    'temp' : 'temperature',
    'hum' : 'humidity',
    'cnt' : 'count'
}, inplace=True)

print(hour_df.head())

st.title("Dashboard Number Of Bike Rentals")

# informasi jumlah pengguna sepeda
col1, col2, col3 = st.columns(3)
col1.metric("Number Of Bike", hour_df['count'].sum(), label_visibility='visible')
col2.metric("Casual", hour_df['casual'].sum())
col3.metric("Registered", hour_df['registered'].sum())

year_map = {0 : '2011', 1 : '2012'}

col1, col2, col3 = st.columns(3)
# diagram total bike by hour
hour_result = hour_df.groupby(['year','hour'])[['count']].sum().reset_index()
hour_result['year'] = hour_result['year'].map(year_map)
hour_result_df = pd.DataFrame(hour_result)
fig = px.line(hour_result_df, x='hour', y='count', color='year', title='Number of Bike Rentals by Hour', color_discrete_map={'2011': 'purple', '2012': 'white'})
fig.update_xaxes(range=[0, 23])
fig.update_layout(title_x=0.25, title_y=0.95)
col1.plotly_chart(fig, use_container_width=True)

season_map = {1 : "springer", 2 : "summer", 3 : "fall", 4 : "winter"}

season_result = hour_df.groupby(['year', 'season'])[['count']].sum().reset_index()
season_result['year'] = season_result['year'].map(year_map)
season_result['season'] = season_result['season'].map(season_map)
season_result_df = pd.DataFrame(season_result)
fig = px.bar(season_result_df, x='season', y='count', color='year', title='Number of Bike Rentals by season', color_discrete_map={'2011': 'green', '2012': 'orange'})
fig.update_layout(title_x=0.25, title_y=0.95)
col2.plotly_chart(fig, use_container_width=True)

month_map = {1 : 'january',
             2 : 'february',
             3 : 'march',
             4 : 'april',
             5 : 'may',
             6 : 'june',
             7 : 'july',
             8 : 'august',
             9 : 'september',
             10 : 'october',
             11 : 'november',
             12 : 'december'}

month_result = hour_df.groupby(['year', 'month'])[['count']].sum().reset_index()
month_result['year'] = month_result['year'].map(year_map)
month_result['month'] = month_result['month'].map(month_map)
month_result_df = pd.DataFrame(month_result)
# Membuat plotly bar chart horizontal dengan hue berdasarkan tahun
fig = px.bar(month_result_df, x='count', y='month', color='year', title='Number of Bike Rentals by Month', color_discrete_map={'2011': 'red', '2012': 'blue'})
fig.update_layout(title_x=0.25, title_y=0.95)  # Mengatur judul di tengah
fig.update_yaxes(categoryorder="total ascending")
col3.plotly_chart(fig, use_container_width=True)

k1, k2, k3 = st.columns(3)

holiday_result = hour_df.groupby('holiday')['count'].sum().reset_index()
holiday_result['holiday'] = holiday_result['holiday'].replace({1: 'Holiday', 0: 'Not Holiday'})
fig, ax = plt.subplots()
ax.pie(holiday_result['count'], labels=holiday_result['holiday'], autopct='%1.1f%%', startangle=90)
ax.set_title("Percentage Of Bike Rentals by Holiday Status")
k1.pyplot(fig)

workingday_result = hour_df.groupby('workingday')['count'].sum().reset_index()
workingday_result['workingday'] = workingday_result['workingday'].replace({1: 'workingday', 0: 'Not workingday'})
fig, ax = plt.subplots()
ax.pie(workingday_result['count'], labels=workingday_result['workingday'], autopct='%1.1f%%', startangle=90)
ax.set_title("Percentage of Bike Rentals by workingday Status")
k3.pyplot(fig)

weather_result = hour_df.groupby(['year','weather_condition'])['count'].sum().reset_index()
weather_map = {1 : 'Clear',
               2 : 'Mist + Cloudy',
               3 : 'Light Snow',
               4 : 'Heavy Rain'}
weather_result['year'] = weather_result['year'].map(year_map)
weather_result['weather_condition'] = weather_result['weather_condition'].map(weather_map)
fig = px.bar(weather_result, x='weather_condition', y='count', color='year', title='Number of Bike Rentals by Weather Condition', color_discrete_map={'2011': 'green', '2012': 'orange'})
fig.update_layout(title_x=0.15, title_y=0.95)
k2.plotly_chart(fig, use_container_width=True)

weekday_map = {0 : 'saturday',
               6 : 'sunday',
               1 : 'monday',
               2 : 'tuesday',
               3 : 'wednesday',
               4 : 'thursday',
               5 : 'friday'}

holiday_map = {0 : 'no',
               1 : 'holiday'}

workingday_map = {0 : 'no',
                  1 : 'workingday'}

hour_df['holiday'] = hour_df['holiday'].map(holiday_map)
hour_df['workingday'] = hour_df['workingday'].map(workingday_map)
hour_df['weather_condition'] = hour_df['weather_condition'].map(weather_map)

a1, a2 = st.columns(2)

weekday_result = hour_df.groupby(['year','weekday'])['count'].sum().reset_index()
weekday_result['year'] = weekday_result['year'].map(year_map)
weekday_result['weekday'] = weekday_result['weekday'].map(weekday_map)
fig = px.bar(weekday_result, x='weekday', y='count', color='year', title='Number of Bike Rentals by Weekday', color_discrete_map={'2011': 'blue', '2012': 'orange'})
fig.update_layout(title_x=0.25, title_y=0.95)
a1.plotly_chart(fig, use_container_width=True)

hour_df['temperature'] = (hour_df['temperature'] * 41).round(2)
hour_df['atemp'] = (hour_df['atemp']*50).round(2)
hour_df['windspeed'] = (hour_df['windspeed']*67).round(2)
hour_df['humidity'] = (hour_df['humidity']*100).round(2)
hour_df['weekday'] = hour_df['weekday'].map(weekday_map)
hour_df['season'] = hour_df['season'].map(season_map)
hour_df['year'] = hour_df['year'].map(year_map)
hour_df['month'] = hour_df['month'].map(month_map)

a2.dataframe(hour_df)





