from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS
from dataDAO import DataDAO

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='.')
CORS(app)  # Enable CORS for all routes

dataDAO_instance = DataDAO()

@app.route('/')
def index():
    return render_template('dataviewer.html')

## Correct usage
@app.route('/cso_data')
def getAll():
    results = dataDAO_instance.getAll()
    return jsonify(results)

@app.route('/cso_data_weight')
def getAllWeight():
    results = dataDAO_instance.getAllWeight()
    return jsonify(results)

    #import pdb; pdb.set_trace()
#curl "http://127.0.0.1:5000/cso_data/2"
@app.route('/cso_data/<int:year>')
def findByYear(year):
    foundData = dataDAO_instance.findByYear(year)

    return jsonify(foundData)
    #import pdb; pdb.set_trace()
#curl  -i -H "Content-Type:application/json" -X POST -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/cso_data
@app.route('/cso_data', methods=['POST'])
def create():
    try:
        if not request.json:
            abort(400)
        # other checking 
        cso_data = {
            "year": request.json['year'],
            "sex": request.json['sex'],
            "age_group": request.json['age_group'],
            "average_height": request.json['average_height'],
            "average_weight": request.json['average_weight'],
        }
        print("Received data:", cso_data) 
        values =(cso_data['year'],cso_data['sex'],cso_data['age_group'],cso_data['average_height'],cso_data['average_weight'])
        newId = dataDAO_instance.create(values)
        cso_data['year'] = newId
        return jsonify(cso_data)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    #import pdb; pdb.set_trace()

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/cso_data/1
@app.route('/cso_data/<int:year>', methods=['PUT'])
def update(year):
    print("Updating data for year:", year)
    
    try:
        # Use the findByYear method to get the data as a dictionary
        foundData = dataDAO_instance.findByYear(year)
        print("Found data:", foundData)

        if not foundData:
            abort(404)

        if not request.json:
            abort(400)
        
        reqJson = request.json

        # Update the foundData dictionary with the new values
        if 'year' in reqJson:
            foundData['year'] = reqJson['year']
        if 'sex' in reqJson:
            foundData['sex'] = reqJson['sex']
        if 'age_group' in reqJson:
            foundData['age_group'] = reqJson['age_group']
        if 'average_height' in reqJson:
            foundData['average_height'] = reqJson['average_height']
        if 'average_weight' in reqJson:
            foundData['average_weight'] = reqJson['average_weight']

        values = (foundData['year'], foundData['sex'], foundData['age_group'], foundData['average_height'], foundData['average_weight'])
        dataDAO_instance.update(values)

        return jsonify(foundData)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

    

@app.route('/cso_data/<int:year>' , methods=['DELETE'])
def delete(year):
    dataDAO_instance.delete(year)
    
    return jsonify({"done": True})
    #import pdb; pdb.set_trace()

# Correct usage
@app.route('/')
def correct_route():
    # Create a dictionary or use other serializable data
    data = {'message': 'This is a JSON-serializable response'}

    # Return the data using jsonify
    return jsonify(data)


if __name__ == '__main__' :
    app.run(debug= True)