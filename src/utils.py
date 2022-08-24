
import folium 
import requests

def get_coord(x):
    r3 = requests.get(x).json()
    coords = r3['features'][0]['geometry']
    return coords

def create_map(lat, lon, df):
    m = folium.Map(location=[lat, lon],
                min_zoom=7, 
                max_zoom=16,
                zoom_start=12)

    folium.TileLayer('cartodb dark_matter').add_to(m)

    style_0 = {'fillColor': '#2ca25f',  'color': '#2ca25f', "fillOpacity": 0.1, "weight": 1.7}
    style_1 = {'fillColor': '#dd1c77',  'color': '#dd1c77', "fillOpacity": 0.5}
    style_2 = {'fillColor': '#bdbdbd',  'color': '#756bb1', "fillOpacity": 0.5}

    if df is not None:

        flood = folium.FeatureGroup(name='Flooded area', show=True)
        m.add_child(flood)

        flood_no = folium.FeatureGroup(name='Warning no longer active', show=True)
        m.add_child(flood_no)

        warning_df = df[df['severity']=='Flood warning']
        warning_df.reset_index(inplace=True, drop=True)

        no_df = df[df['severity']!='Flood warning']
        no_df.reset_index(inplace=True, drop=True)

        for i in range(len(warning_df)):
            geo_json = folium.GeoJson(warning_df['coords'][i], style_function = lambda x:style_1)
            geo_json.add_child( folium.Popup('Status: {} \n Description: {} \n Severity: {}' .format(warning_df['severity'][i],
            warning_df['description'][i], warning_df['severity_level'][i])))
            geo_json.add_to(flood)

        for i in range(len(no_df)):
            geo_json2 = folium.GeoJson(no_df['coords'][i], style_function = lambda x:style_2)
            geo_json2.add_child( folium.Popup('Status: {} \n Description: {} \n Severity: {} \n Date changed: {}' .format(no_df['severity'][i],
            no_df['description'][i], no_df['severity_level'][i], no_df['time_changed'][i])))
            geo_json2.add_to(flood_no)
    
    folium.LayerControl(collapsed = False).add_to(m)

    return (m)