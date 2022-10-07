import base64
from io import BytesIO
import folium
from matplotlib import pyplot as plt


def create_map(lat, lon, df, zoom=12):
    m = folium.Map(location=[lat, lon],
                   min_zoom=7,
                   max_zoom=16,
                   zoom_start=10)

    folium.TileLayer('cartodb dark_matter').add_to(m)

    style_1 = {'fillColor': '#dd1c77',  'color': '#dd1c77', "fillOpacity": 0.5}
    style_2 = {'fillColor': '#bdbdbd',  'color': '#756bb1', "fillOpacity": 0.5}

    if df is not None:

        flood = folium.FeatureGroup(name='Flooded area', show=True)
        m.add_child(flood)

        flood_no = folium.FeatureGroup(name='Warning no longer active', show=True) # noqaE501
        m.add_child(flood_no)

        warning_df = df[df['severity'] == 'Flood warning']
        warning_df.reset_index(inplace=True, drop=True)

        no_df = df[df['severity'] != 'Flood warning']
        no_df.reset_index(inplace=True, drop=True)

        for i in range(len(warning_df)):
            geo_json = folium.GeoJson(warning_df['coordinates'][i], style_function = lambda x:style_1) # noqaE501
            geo_json.add_child(folium.Popup('Status: {} \n Description: {} \n Severity: {}' .format(warning_df['severity'][i], # noqaE501
                                            warning_df['description'][i],
                                            warning_df['severity_level'][i])))
            geo_json.add_to(flood)

        for i in range(len(no_df)):
            geo_json2 = folium.GeoJson(no_df['coordinates'][i], style_function=lambda x:style_2) # noqaE501
            geo_json2.add_child( folium.Popup('Status: {} \n Description: {} \n Severity: {} \n Date changed: {}' .format(no_df['severity'][i], # noqaE501
            no_df['description'][i], no_df['severity_level'][i], no_df['time_changed'][i]))) # noqaE501
            geo_json2.add_to(flood_no)

    folium.LayerControl(collapsed=False).add_to(m)

    return (m)


def sparkline(data, figsize=(1.5, 0.75), **kwargs):
    """
    creates a sparkline
    """
    if data['type'] == 'Polygon':
        data = data['coordinates'][0]
        xs, ys = zip(*data)  # create lists of x and y values
    else:
        data = data['coordinates'][0][0]
        xs, ys = zip(*data)  # create lists of x and y values

    *_, ax = plt.subplots(1, 1, figsize=figsize, **kwargs)
    ax.plot(xs, ys, color='navy')
    ax.fill(xs, ys, color='navy', alpha=0.5)
    ax.axis('off')

    # save the figure to html
    bio = BytesIO()
    plt.savefig(bio, transparent=True)
    plt.close()
    html = """<img src="data:image/png;base64,%s"/>""" % base64.b64encode(bio.getvalue()).decode('utf-8') # noqaE501
    return html
