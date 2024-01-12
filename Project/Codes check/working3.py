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

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Data Table</title>
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
    <script>
        $(document).ready(function () {
            $.ajax({
                url: "/api/data",
                type: "GET",
                dataType: "json",
                success: function (data) {
                    renderTable(data);
                },
                error: function (error) {
                    console.log("Error fetching data:", error);
                }
            });
    
            function renderTable(data) {
                var headers = data.headers;
                var rows = data.rows;
    
                var table = '<table border="1"><thead><tr><th>Year</th><th>Sex</th><th>Age Group</th><th>Average Height (Centimetres)</th></tr></thead><tbody>';
    
                for (var i = 0; i < rows.length; i++) {
                    var row = rows[i];
                    table += '<tr><td>' + (headers['TLIST(A1)']['category'] ? headers['TLIST(A1)']['category']['label'][row[1]] : row[1]) + '</td>';
                    table += '<td>' + (headers['C02199V02655']['category'] ? headers['C02199V02655']['category']['label'][row[2]] : row[2]) + '</td>';
                    table += '<td>' + (headers['C02076V03371']['category'] ? headers['C02076V03371']['category']['label'][row[3]] : row[3]) + '</td>';
                    table += '<td>' + row[0] + '</td></tr>';
                }
    
                table += '</tbody></table>';
                $("#data-table").html(table);
            }
        });
    </script>
</head>
<body>
    <div id="data-table"></div>
</body>
</html>
