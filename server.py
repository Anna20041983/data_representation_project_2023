from flask import Flask, jsonify, request, abort
from disabilityDAO import disabilityDAO
from physicalDAO import physicalDAO


app = Flask(__name__, static_url_path='', static_folder='.')

# Define a single DAO (you may need to adapt this based on your actual DAO implementation)
class CombinedDAO:
    @staticmethod
    def getAll():
        # Combine results from both DAOs
        results = disabilityDAO.getAll() + physicalDAO.getAll()
        return results

    def findByYear(year):
        foundData = disabilityDAO.findByYear(year) + physicalDAO.findByYear(year)

        return jsonify(foundData)
    # Other methods (findByYear, create, update, delete) go here...

    def create():

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

    def update(year):
        foundBook1 = physicalDAO.findByYear(year)
        if not foundData1:
            abort(404)
    
        if not request.json:
            abort(400)
        reqJson = request.json

        if 'Year' in reqJson:
            foundData1['year'] = reqJson['year']
        if 'Age Group' in reqJson:
            foundData1['age_group'] = reqJson['age_group']
        if 'County' in reqJson:
            foundData1['county'] = reqJson['county']
        if 'Sex' in reqJson:
            foundData1['sex'] = reqJson['sex']
        if 'Type of Disability' in reqJson:
            foundData1['type_of_disability'] = reqJson['type_of_disability']
        values1 = (foundData1['year'],foundData1['age_group'],foundData1['county'],foundData1['sex'],foundData1['type_of_disability'],foundData1['no_of_children'])
        physicalDAO.update(values1)
        return jsonify(foundData1)

        foundBook2 = disabilityDAO.findByYear(year)
        if not foundData2:
            abort(404)
    
        if not request.json:
            abort(400)
        reqJson = request.json

        if 'Year' in reqJson:
            foundData2['year'] = reqJson['year']
        if 'Age Group' in reqJson:
            foundData2['age_group'] = reqJson['age_group']
        if 'County' in reqJson:
            foundData2['county'] = reqJson['county']
        if 'Sex' in reqJson:
            foundData2['sex'] = reqJson['sex']
        if 'Severity of Disability' in reqJson:
            foundData2['severity_of_disability'] = reqJson['severity_of_disability']
        values2 = (foundData2['year'],foundData2['age_group'],foundData2['county'],foundData2['sex'],foundData2['severity_of_disability'],foundData2['no_of_children'])
        disabilityDAO.update(values2)
        return jsonify(foundData2)

        foundData = foundData1 + foundData2

    def delete(year):
        disabilityDAO.delete(year)
        physicalDAO.delete(year)
        return jsonify({"done":True})


#curl "http://127.0.0.1:5000/books"
@app.route('/cso_data')
def getAll():
    #print("in getall")
    results = CombinedDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/books/2"
@app.route('/cso_data/<int:year>')
def findByYear(year):
    foundData = CombinedDAO.findByYear(year)

    return jsonify(foundData)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books
@app.route('/cso_data', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    cso_data = {
        "year": request.json['year'],
        "age_group": request.json['age_group'],
        "county": request.json['county'],
        "sex": request.json['sex'],
        "type_of_disability": request.json['type_of_disability']['severity_of_disability'],
        "no_of_children": request.json['no_of_children'],
    }
    values =(cso_data['year'],cso_data['age_group'],cso_data['county'],cso_data['sex'],cso_data['type_of_disability']['severity_of_disability'],cso_data['no_of_children'])
    newId = CombinedDAO.create(values)
    cso_data['year'] = newId
    return jsonify(cso_data)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books/1
@app.route('/cso_data/<int:year>', methods=['PUT'])
def update(year):
    foundBook = CombinedDAO.findByYear(year)
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
        foundData['type_of_disability'] = reqJson['type_of_disability']['severity_of_disability']
    values = (foundData['year'],foundData['age_group'],foundData['county'],foundData['sex'],foundData['type_of_disability']['severity_of_disability'],foundData['no_of_children'])
    CombinedDAO.update(values)
    
    return jsonify(foundData)
        

    

@app.route('/cso_data/<int:year>' , methods=['DELETE'])
def delete(year):
    CombinedDAO.delete(year)
    
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)