# import relevant files
from venv import create
import os
import streamlit as st
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
import requests
from datetime import datetime, date
from src.utils import create_map, get_coord

# making wide layout default
st.set_page_config(layout="wide")

"# Flood Data from the Environment Agency"

# get source data
df = pd.read_csv('https://raw.githubusercontent.com/jbuffer/flood-actions/main/data/flood-data.csv')

#format date and set parameters
df['date'] = pd.to_datetime(df['date']).dt.date
max_date = date.today()
min_date = df['date'].min()

# add sidebar logo and input
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'blue_logo/logo_water.png')
st.sidebar.image(filename, caption='MilaAdam, CC BY-SA 4.0, via Wikimedia Commons')

# sidebar postcode input
st.sidebar.write('''
**Postcode** \n
Enter a postcode in the "Postcode finder" widget 
to change the focus of the map
''')

try:
    latlon = st.sidebar.text_input('Postcode finder:', value='SW1A 2AA', max_chars=8, key=None, type='default')
    r = requests.get('https://api.postcodes.io/postcodes/{}'.format(latlon))
    lat = r.json()['result']['latitude']
    lon = r.json()['result']['longitude']
    lsoa = r.json()['result']['lsoa']
    
except:
    st.sidebar.write('*This is not a valid postcode. Please try again* :sunglasses:')
    r = requests.get('https://api.postcodes.io/postcodes/{}'.format('WC1B3HF'))
    lat = r.json()['result']['latitude']
    lon = r.json()['result']['longitude']
    lsoa = r.json()['result']['lsoa']

# sidebar date
st.sidebar.write(f''' 
**Date selection** \n
Historical data goes back to {min_date}
''')
date_in= st.sidebar.date_input('Select date of interest', 
    min_value=min_date,
    max_value=max_date, 
    value=date.today())

df = df[df['date'] == date_in]
df.reset_index(inplace=True, drop=True)

if df['flood_area_id'].hasnans == True:
    # create map
    m = create_map(lat, lon, df = None)
    st.header('No floods or recent flooding on this date')
    
else:
    coords_list = map(get_coord, df['polygon_url'])
    df['coords'] = list(coords_list) 
    m = create_map(lat, lon, df)

    table_df = df[['county', 'severity', 'riverorsea', 'description' ]]
    table_df = table_df.drop_duplicates()
    table_df.rename(columns={
    'County':'county',
    'Warning': 'severity',
    'River or Sea': 'riverorsea',
    'Description': 'description'
    })

    with st.expander('Details', True):
        st.table(table_df)


# call to render Folium map in Streamlit

st.write("Use the 'Postcode finder' widget in the sidebar to focus on a place, or zoom out to see a country-wide view:")
# add map
folium_static(m)

