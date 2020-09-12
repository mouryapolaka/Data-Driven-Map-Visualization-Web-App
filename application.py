from flask import Flask, render_template, request
import folium
import pandas as pd

app = Flask(__name__, static_url_path = "", static_folder = "assets")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/marker_map_plot', methods=['GET', 'POST'])
def map_plot():
    #Map object
    map = folium.Map(
        location=[-31.840233, 145.612793],
        zoom_start=6)

    if request.method == 'POST':
        f = request.form['csvfile']
        with open(f) as file:
            data = pd.read_csv(file)         
            for index, row in data.iterrows():
                folium.Marker(location=[row['lat'], row['long']],
                    popup=row['suburb']).add_to(map)

        map.save('templates/marker_map.html')

        return render_template('marker_map.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)