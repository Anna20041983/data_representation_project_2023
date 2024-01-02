from flask import Flask, jsonify, request, abort
from disabilityDAO import disabilityDAO
from physicalDAO import physicalDAO

app = Flask(__name__, static_url_path='', static_folder='.')

# Creating an instance of the disabilityDAO class
#disability_data = disabilityDAO.getAll()
#physical_data = physicalDAO.getAll()

# Define a single DAO (you may need to adapt this based on your actual DAO implementation)
class CombinedDAO:
    @staticmethod
    def getAll():
        disability_data = disabilityDAO.getAll()
        physical_data = physicalDAO.getAll()

        # Assuming both disability and physical data have the same structure
        results = disability_data + physical_data
        return jsonify(results)
    
    #import pdb; pdb.set_trace()

    @staticmethod
    def findByYear(year):
        foundData = disabilityDAO.findByYear(year) + physicalDAO.findByYear(year)

        return jsonify(foundData)
    # Other methods (findByYear, create, update, delete) go here...

    #import pdb; pdb.set_trace()

    @staticmethod
    def create(values):

        cso_data = {
            "year": request.json['year'],
            "age_group": request.json['age_group'],
            "county": request.json['county'],
            "sex": request.json['sex'],
            "type_of_disability": request.json['type_of_disability'],
            "no_of_children": request.json['no_of_children'],
        }
        values =(cso_data['year'],cso_data['age_group'],cso_data['county'],cso_data['sex'],cso_data['type_of_disability'],cso_data['no_of_children'])
        newId = disabilityDAO.create(values) + physicalDAO.create(values)
        cso_data['year'] = newId
        return jsonify(cso_data)
        return jsonify({"message": "Data created successfully"})

    #import pdb; pdb.set_trace()

    @staticmethod
    def updatePhysical(values):
        foundData = physicalDAO.findByYear(year)
        if not foundData:
            abort(404)
    
        if not request.json:
            abort(400)
        reqJson = request.json

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
        if 'Children and Young People registered as having a Physical and/or Sensory Disability' in reqJson:
            foundData['no_of_children'] = reqJson['no_of_children']
        values = (foundData['year'],foundData['age_group'],foundData['county'],foundData['sex'],foundData['type_of_disability'],foundData['no_of_children'])
        physicalDAO.update(values)
        return jsonify(foundData)
        return jsonify({"message": "Data updated successfully"})
    #import pdb; pdb.set_trace()

    @staticmethod
    def updateDisability(values):
        foundData = disabilityDAO.findByYear(year)
        if not foundData:
            abort(404)
    
        if not request.json:
            abort(400)
        reqJson = request.json

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
        if 'Children and Young People having an Intellectual Disability' in reqJson:
            foundData['no_of_children'] = reqJson['no_of_children']
        values = (foundData['year'],foundData['age_group'],foundData['county'],foundData['sex'],foundData['severity_of_disability'],foundData['no_of_children'])
        disabilityDAO.update(values)
        return jsonify(foundData)
        return jsonify({"message": "Data updated successfully"})


    #import pdb; pdb.set_trace()

    @staticmethod
    def update(values):
        # Choose which DAO to update based on some condition, e.g., type_of_data
        if request.json.get('type_of_data') == 'disability':
            return self.updateDisability(year)
        elif request.json.get('type_of_data') == 'physical':
            return self.updatePhysical(year)
        else:
            abort(400)
        return jsonify({"message": "Data updated successfully"})
    #import pdb; pdb.set_trace()
    @staticmethod
    def delete(year):
        disabilityDAO.delete(year)
        physicalDAO.delete(year)
        return jsonify({"done":True})
        return jsonify({"message": "Data deleted successfully"})
    #import pdb; pdb.set_trace()




## Correct usage
@app.route('/cso_data')
def getAll():
    combined_dao_instance = CombinedDAO()
    results = combined_dao_instance.getAll()
    return results
    
    #import pdb; pdb.set_trace()
#curl "http://127.0.0.1:5000/books/2"
@app.route('/cso_data/<int:year>')
def findByYear(year):
    foundData = CombinedDAO.findByYear(year)

    return foundData
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
        newId = CombinedDAO.create(values)
        cso_data['year'] = newId
        return jsonify(cso_data)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    #import pdb; pdb.set_trace()

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books/1
@app.route('/cso_data/<int:year>', methods=['PUT'])
def update(year):
    foundData = CombinedDAO.update(year)
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
    CombinedDAO.update(values)
    
    return jsonify(foundData)
    #import pdb; pdb.set_trace() 

    

@app.route('/cso_data/<int:year>' , methods=['DELETE'])
def delete(year):
    CombinedDAO.delete(year)
    
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