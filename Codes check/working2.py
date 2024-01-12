from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # Make a request to the API
    url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/HIS51/JSON-stat/2.0/en"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information from the data
        dimensions = data['dimension']
        headers = {key: value['category']['label'] for key, value in dimensions.items()}
        values = data['value']

        # Organize the values into rows with appropriate dimensions
        rows = [values[i:i+4] for i in range(0, len(values), 4)]

        # Render the HTML template with the data
        return render_template('index.html', headers=headers, rows=rows)
    else:
        return f"Error fetching data from API: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Data Table</title>
</head>
<body>
    <table border="1">
        <thead>
            <tr>
                <th>Average Height (Centimetres)</th>
                <th>Year</th>
                <th>Sex</th>
                <th>Age Group</th>
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ headers['TLIST(A1)'][row[1]] }}</td>
                    <td>{{ headers['C02199V02655'][row[2]] }}</td>
                    <td>{{ headers['C02076V03371'][row[3]] }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
