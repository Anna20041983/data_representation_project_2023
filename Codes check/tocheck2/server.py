from flask import Flask, render_template, jsonify, request, abort
from dataDAO import dataDAO

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return render_template('login.html')

## Correct usage
@app.route('/cso_data')
def getAll():
    results = dataDAO.getAll()
    return results
    
    #import pdb; pdb.set_trace()
#curl "http://127.0.0.1:5000/cso_data/2"
@app.route('/cso_data/<int:year>')
def findByYear(year):
    foundData = dataDAO.findByYear(year)

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
        }
        values =(cso_data['year'],cso_data['sex'],cso_data['age_group'],cso_data['average_height'])
        newId = dataDAO.create(values)
        cso_data['year'] = newId
        return jsonify(cso_data)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    #import pdb; pdb.set_trace()

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/cso_data/1
@app.route('/cso_data/<int:year>', methods=['PUT'])
def update(year):
    foundData = dataDAO.findByYear(year)
    if not foundData:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    ##if 'price' in reqJson and type(reqJson['price']) is not int:
        ##abort(400)

    if 'Year' in reqJson:
        foundData['year'] = reqJson['year']
    if 'Sex' in reqJson:
        foundData['sex'] = reqJson['sex']
    if 'Age Group' in reqJson:
        foundData['age_group'] = reqJson['age_group']
    if 'Average Height' in reqJson:
        foundData['average_height'] = reqJson['average_height']

    values = (foundData['year'],foundData['sex'],foundData['age_group'],foundData['average_height'])
    dataDAO.update(values)
    
    return jsonify(foundData)
    #import pdb; pdb.set_trace() 

    

@app.route('/cso_data/<int:year>' , methods=['DELETE'])
def delete(year):
    dataDAO.delete(year)
    
    return jsonify({"done":True})
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