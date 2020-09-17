from flask import Flask, render_template, request, send_file
import folium
import pandas as pd
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
from datetime import datetime, date

app = Flask(__name__, static_url_path = "", static_folder = "assets")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#Display map for bush fire spread based on a heat map
@app.route('/bushfire_spread_map', methods=['GET', 'POST'])
def bushfire_spread_map():
    #Heat map object for bush fire
    bush_fire_map = folium.Map(
        location=[-25.2744, 133.7751],
        zoom_start = 4)
    
    if request.method == 'POST':
        f = request.files['bushfire_csvfile']
        df = pd.read_csv(f)
        
        #group by all the rows according to date so that the map visualizes bush fires according to date
        date_groupby_list = df.groupby('date').apply(lambda x: x[['latitude','longitude']].values.tolist())
        dt_obj = [datetime.strptime(i,'%Y-%m-%d') for i in date_groupby_list.index]
        date_index = [x.strftime('%Y-%m-%d') for x in dt_obj]
        date_hour_date = date_groupby_list.tolist()

        HeatMapWithTime(date_hour_date, index = date_index).add_to(bush_fire_map)

    return bush_fire_map.get_root().render()

#Display map marker_plot based on coordinates
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

if __name__ == '__main__':
    app.run(debug=True)