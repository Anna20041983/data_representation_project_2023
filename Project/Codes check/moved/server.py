from flask import Flask, jsonify, request, abort
from physicalDAO import physicalDAO

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return "Hello, World!"

## Correct usage
@app.route('/cso_data')
def getAll():
    results = physicalDAO.getAll()
    return results
    
    #import pdb; pdb.set_trace()
#curl "http://127.0.0.1:5000/books/2"
@app.route('/cso_data/<int:year>')
def findByYear(year):
    foundData = physicalDAO.findByYear(year)

    return jsonify(foundData)
    #import pdb; pdb.set_trace()
#curl  -i -H "Content-Type:application/json" -X POST -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books
@app.route('/cso_data', methods=['POST'])
def create():
    try:
        if not request.json:
            abort(400)
        # other checking 
        cso_data = {
            "year": request.json['year'],
            "age_group": request.json['age_group'],
            "county": request.json['county'],
            "sex": request.json['sex'],
            "type_of_disability": request.json['type_of_disability'],
            "no_of_children": request.json['no_of_children'],
        }
        values =(cso_data['year'],cso_data['age_group'],cso_data['county'],cso_data['sex'],cso_data['type_of_disability'],cso_data['no_of_children'])
        newId = physicalDAO.create(values)
        cso_data['year'] = newId
        return jsonify(cso_data)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    #import pdb; pdb.set_trace()

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books/1
@app.route('/cso_data/<int:year>', methods=['PUT'])
def update(year):
    foundData = physicalDAO.findByYear(year)
    if not foundData:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    ##if 'price' in reqJson and type(reqJson['price']) is not int:
        ##abort(400)

    if 'Year' in reqJson:
        foundData['year'] = reqJson['year']
    if 'Age Group' in reqJson:
        foundData['age_group'] = reqJson['age_group']
    if 'County' in reqJson:
        foundData['county'] = reqJson['county']
    if 'Sex' in reqJson:
        foundData['sex'] = reqJson['sex']
    if 'Type of Disability' in reqJson:
        foundData['type_of_disability'] = reqJson['type_of_disability']
    values = (foundData['year'],foundData['age_group'],foundData['county'],foundData['sex'],foundData['type_of_disability'],foundData['no_of_children'])
    physicalDAO.update(values)
    
    return jsonify(foundData)
    #import pdb; pdb.set_trace() 

    

@app.route('/cso_data/<int:year>' , methods=['DELETE'])
def delete(year):
    physicalDAO.delete(year)
    
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