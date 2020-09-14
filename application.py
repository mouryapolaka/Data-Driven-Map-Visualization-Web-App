from flask import Flask, render_template, request
import folium
import pandas as pd
from folium.plugins import HeatMap

app = Flask(__name__, static_url_path = "", static_folder = "assets")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/marker_map_plot', methods=['GET', 'POST'])
def coordinates_map_plot():
    #Map object
    m = folium.Map(
        location=[-31.840233, 145.612793],
        zoom_start=6)

    if request.method == 'POST':
        f = request.form['csvfile']
        with open(f) as file:
            data = pd.read_csv(file)         
            for index, row in data.iterrows():
                folium.Marker(location=[row['latitude'], row['longitude']],
                    popup=row['location']).add_to(m)

    return m.get_root().render()

#Display map for bush fire spread based on a heat map
@app.route('/bushfire_spread_map', methods=['GET', 'POST'])
def bushfire_spread_map():
    #Map object
    m = folium.Map(
        location=[-25.2744, 133.7751],
        zoom_start = 4)
    
    if request.method == 'POST':
        f = request.form['csvfile']
        with open(f) as file:
            data = pd.read_csv(file)
            lat_lon_data = data[['latitude','longitude']]
            HeatMap(lat_lon_data, radius=10).add_to(m)

    #Save marker_map as HTML in templates folder
    #map.save('templates/bushfire_spread_map.html')

    return m.get_root().render()

if __name__ == '__main__':
    app.run(debug=True)