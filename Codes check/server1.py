from flask import Flask, jsonify, request, abort
from disabilityDAO import disabilityDAO

app = Flask(__name__, static_url_path='', static_folder='.')



@app.route('/')
def index():
    return "Hello, World!"

## Correct usage
@app.route('/data')
def getAll():
    results = disabilityDAO.getAll()
    return results
    
    #import pdb; pdb.set_trace()
#curl "http://127.0.0.1:5000/books/2"
@app.route('/data/<int:year>')
def findByYear(year):
    foundData = disabilityDAO.findByYear(year)

    return jsonify(foundData)
    #import pdb; pdb.set_trace()
#curl  -i -H "Content-Type:application/json" -X POST -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books
@app.route('/data', methods=['POST'])
def create():
    try:
        if not request.json:
            abort(400)
        # other checking 
        data = {
            "year": request.json['year'],
            "age_group": request.json['age_group'],
            "county": request.json['county'],
            "sex": request.json['sex'],
            "severity_of_disability": request.json['severity_of_disability'],
            "no_of_children": request.json['no_of_children'],
        }
        values =(data['year'],data['age_group'],data['county'],data['sex'],data['severity_of_disability'],data['no_of_children'])
        newId = disabilityDAO.create(values)
        data['year'] = newId
        return jsonify(data)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    #import pdb; pdb.set_trace()

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books/1
@app.route('/data/<int:year>', methods=['PUT'])
def update(year):
    foundData = disabilityDAO.findByYear(year)
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
    if 'Severity of Disability' in reqJson:
        foundData['severity_of_disability'] = reqJson['severity_of_disability']
    values = (foundData['year'],foundData['age_group'],foundData['county'],foundData['sex'],foundData['severity_of_disability'],foundData['no_of_children'])
    disabilityDAO.update(values)
    
    return jsonify(foundData)
    #import pdb; pdb.set_trace() 

    

@app.route('/data/<int:year>' , methods=['DELETE'])
def delete(year):
    disabilityDAO.delete(year)
    
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