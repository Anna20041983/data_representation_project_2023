from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_api_data():
    url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/HIS51/JSON-stat/2.0/en"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        dimensions = data['dimension']
        headers = {key: value['category']['label'] for key, value in dimensions.items()}
        values = data['value']
        rows = [values[i:i+4] for i in range(0, len(values), 4)]

        return jsonify(headers=headers, rows=rows)
    else:
        return jsonify(error=f"Error fetching data from API: {response.status_code}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)

