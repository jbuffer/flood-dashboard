from ast import literal_eval
import os
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
from src.utils import create_map, sparkline

# making wide layout default
st.set_page_config(layout="wide")

"# Flood Data from the Environment Agency"

# get source data
df = pd.read_csv('https://raw.githubusercontent.com/jbuffer/flood-actions/main/data/flood-data.csv') # noqaE501

# format date and set parameters
df['date'] = pd.to_datetime(df['date']).dt.date
max_date = df['date'].max()
min_date = df['date'].min()

# add sidebar logo and input
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'blue_logo/logo_water.png')
st.sidebar.image(filename, caption='MilaAdam, CC BY-SA 4.0, via Wikimedia Commons') # noqaE501

# sidebar date
st.sidebar.write(f'''
**Date selection** \n
Historical data goes back to {min_date}
''')
date_in= st.sidebar.date_input('Select date of interest', min_value=min_date, max_value=max_date, value=max_date) # noqaE501

df = df[df['date'] == date_in]
df.reset_index(inplace=True, drop=True)

if df['flood_area_id'].hasnans is True:
    # create map
    m = create_map(52.486244, -1.890401, df=None)
    st.header('No floods or recent flooding on this date')

else:
    # create options
    option = st.selectbox('Select your flooded area of interest:', (df['description'])) # noqaE501
    lat = df['lat'][df['description'] == option][0]
    lon = df['long'][df['description'] == option][0]
    st.write(f'''You selected an area in:
    {df['county'][df['description'] == option][0]} County''')

    # apply create_map function for mapping
    df['coordinates'] = df['coords'].apply(literal_eval)
    m = create_map(lat, lon, df)

    # apply sparklines function for table
    df['area'] = df['coordinates'].apply(sparkline)
    table_df = df[['county', 'severity', 'riverorsea', 'description', 'area']]
    table_df = table_df.drop_duplicates()

    with st.expander('Details', True):
        st.write(table_df.to_html(escape=False, index=False), unsafe_allow_html=True) # noqaE501

# add map
folium_static(m)
