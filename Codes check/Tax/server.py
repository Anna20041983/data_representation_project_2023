from flask import Flask, jsonify, request, abort
from incomeDAO import incomeDAO

app = Flask(__name__, static_url_path='', static_folder='.')



@app.route('/')
def index():
    return "Hello, World!"

## Correct usage
@app.route('/api/incomes')
def getAll():
    results = incomeDAO.getAll()
    return results
    
    #import pdb; pdb.set_trace()
#curl "http://127.0.0.1:5000/books/2"
@app.route('/api/incomes/<int:id>')
def findById(id):
    foundData = incomeDAO.findById(id)

    return jsonify(foundData)
    #import pdb; pdb.set_trace()
#curl  -i -H "Content-Type:application/json" -X POST -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books
@app.route('/api/incomes', methods=['POST'])
def create():
    try:
        if not request.json:
            abort(400)
        # other checking 
        income = {
            "type": request.json['type'],
            "range": request.json['range'],
            "status": request.json['status'],
            "year": request.json['year'],
            "distribution": request.json['distribution'],
        }
        values =(income['type'],income['range'],income['status'],income['year'],income['distribution'])
        newId = incomeDAO.create(values)
        income['id'] = newId
        return jsonify(income)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    #import pdb; pdb.set_trace()

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books/1
@app.route('/api/incomes/<int:id>', methods=['PUT'])
def update(id):
    foundIncome = incomeDAO.findById(id)
    if not foundIncome:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    ##if 'price' in reqJson and type(reqJson['price']) is not int:
        ##abort(400)

    if 'Type of Gross Income' in reqJson:
        foundIncome['type'] = reqJson['type']
    if 'Range of Gross Income' in reqJson:
        foundIncome['range'] = reqJson['range']
    if 'Marital Status' in reqJson:
        foundIncome['status'] = reqJson['status']
    if 'Year' in reqJson:
        foundIncome['year'] = reqJson['year']
    if 'Distribution of Income Tax' in reqJson:
        foundIncome['distribution'] = reqJson['type_of_disability']
    values = (foundIncome['type'],foundIncome['range'],foundIncome['status'],foundIncome['year'],foundIncome['distribution'])
    incomeDAO.update(values)
    
    return jsonify(foundIncome)
    #import pdb; pdb.set_trace() 

    

@app.route('/api/incomes/<int:id>' , methods=['DELETE'])
def delete(id):
    incomeDAO.delete(id)
    
    return jsonify({"done":True})
    #import pdb; pdb.set_trace()

# Correct usage
@app.route('/')
def correct_route():
    # Create a dictionary or use other serializable data
    income = {'message': 'This is a JSON-serializable response'}

    # Return the data using jsonify
    return jsonify(income)


if __name__ == '__main__' :
    app.run(debug= True)