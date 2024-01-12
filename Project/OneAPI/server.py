from flask import Flask, render_template, jsonify, request, abort, redirect, url_for, session
from flask_cors import CORS
from dataDAO import dataDAO

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='.')
CORS(app)  # Enable CORS for all routes

app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Dummy user for demonstration purposes
dummy_user = {'username': 'demo', 'password': 'password'}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        # Redirect to login page if not logged in
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == dummy_user['username'] and password == dummy_user['password']:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # Redirect to the failed page on incorrect login
            return redirect(url_for('failed'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Failed login route
@app.route('/failed')
def failed():
    return render_template('failed.html')

## Correct usage
@app.route('/cso_data')
def getAll():
    results = dataDAO.getAll()
    return jsonify(results)

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
        print("Received data:", cso_data) 
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
    print("Updating data for year:", year)
    foundData = dataDAO.findByYear(year)
    print("Found data:", foundData)
    try:
        if not foundData:
            abort(404)
    
        if not request.json:
            abort(400)
        reqJson = request.json
    ##if 'price' in reqJson and type(reqJson['price']) is not int:
        ##abort(400)

        if 'year' in reqJson:
            foundData['year'] = reqJson['year']
        if 'sex' in reqJson:
            foundData['sex'] = reqJson['sex']
        if 'age_group' in reqJson:
            foundData['age_group'] = reqJson['age_group']
        if 'average_height' in reqJson:
            foundData['average_height'] = reqJson['average_height']

        values = (foundData['year'],foundData['sex'],foundData['age_group'],foundData['average_height'])
        dataDAO.update(values)
    
        return jsonify(foundData)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
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