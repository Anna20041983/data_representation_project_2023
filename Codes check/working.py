from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # Make a request to the API
    url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/HIS51/JSON-stat/2.0/en"
    response = requests.get(url)

    if response.status_code == 200:
        # Print the response content to understand its structure
        print(response.json())

        # Modify the code based on the actual structure of the API response
        # ...

        # Render the HTML template with the data
        return render_template('index.html')
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
                <th>Headers</th>
                {% for header in headers %}
                    <th>{{ header }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Values</td>
                {% for value in values %}
                    <td>{{ value }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</body>
</html>
