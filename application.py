from flask import Flask, render_template, request, redirect
import folium
import pandas as pd
from folium.plugins import HeatMap

app = Flask(__name__, static_url_path = "", static_folder = "assets")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/marker_map_plot', methods=['GET', 'POST'])
def coordinates_map_plot():
    #Marker map object
    marker_map = folium.Map(
        location=[-25.2744, 133.7751],
        zoom_start=4)

    if request.method == 'POST':
        f = request.files['marker_plot_csvfile']
        data = pd.read_csv(f)         
        for index, row in data.iterrows():
            folium.Marker(location=[row['latitude'], row['longitude']],
                popup=row['location']).add_to(marker_map)

    return marker_map.get_root().render() 

#Display map for bush fire spread based on a heat map
@app.route('/bushfire_spread_map', methods=['GET', 'POST'])
def bushfire_spread_map():
    #Heat map object
    heat_map = folium.Map(
        location=[-25.2744, 133.7751],
        zoom_start = 4)
    
    if request.method == 'POST':
        f = request.files['bushfire_csvfile']
        data = pd.read_csv(f)  
        lat_lon_data = data[['latitude','longitude']]
        HeatMap(lat_lon_data, radius=9).add_to(heat_map)

    return heat_map.get_root().render()

if __name__ == '__main__':
    app.run(debug=True)