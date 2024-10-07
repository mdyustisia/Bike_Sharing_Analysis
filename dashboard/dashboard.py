import streamlit as stpip
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('dashboard/main_data.csv')

# Mengubah season number menjadi nama musim
season_map = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
df['season'] = df['season'].map(season_map)

# Convert 'dteday' kolom dengan datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Mengambil tahun dan bulan
df['year'] = df['dteday'].dt.year
df['month'] = df['dteday'].dt.month

st.set_page_config(page_title='Data Analisis Bike Sharing', layout='wide')

st.title('Data Analisis Bike Sharing')

st.sidebar.header('Filter Data')
seasons = st.sidebar.multiselect('Select Seasons', df['season'].unique(), default=df['season'].unique())
year = st.sidebar.selectbox('Select Year', [2011, 2012])

filtered_df = df[(df['season'].isin(seasons)) & (df['year'] == year)]

st.sidebar.header('Temperature Filter')
temp_min, temp_max = st.sidebar.slider('Select Temperature Range', min_value=float(df['temp'].min()),
                                       max_value=float(df['temp'].max()), value=(float(df['temp'].min()), float(df['temp'].max())))

# Filter data berdasarkan range suhu
filtered_df = filtered_df[(filtered_df['temp'] >= temp_min) & (filtered_df['temp'] <= temp_max)]

# Bar Chart: Total Bike Sharing by Season
st.header(f'Total Bike Sharing by Season in {year}')
season_sharing = filtered_df.groupby('season')['cnt'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
season_sharing.plot(kind='barh', ax=ax, color=['#66B3FF', '#D3D3D3', '#D3D3D3', '#D3D3D3'])
ax.set_title('Bike Rentals by Season')
ax.set_ylabel(None)
ax.invert_yaxis()
st.pyplot(fig)

# Line Chart: Bike Rentals by Month
st.header(f'Bike Rentals by Month in {year}')
monthly_sharing = df[df['year'] == year].groupby('month')['cnt'].sum()

fig, ax = plt.subplots(figsize=(10, 5))
monthly_sharing.plot(kind='line', marker='o', color='#66B3FF', ax=ax)
ax.set_title(f'Bike Rentals by Month in {year}')
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(fig)

# Scatter Plot: Temperature vs. Bike Sharing
colors_ = ['#66B3FF', '#FD151B', '#FFB30F', '#25FF50']
st.header(f'Temperature vs. Bike Sharing in {year}')
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_df, x='temp', y='cnt', hue='season', palette=colors_, ax=ax)
ax.set_title('Temperature vs. Total Bike Rentals')
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)
