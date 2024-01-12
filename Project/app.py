from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

# Define the data model
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    range = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    distribution = db.Column(db.String(50), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/incomes', methods=['GET'])
def get_all():
    incomes = Income.query.all()
    return jsonify([income.serialize() for income in incomes])

@app.route('/api/incomes/<int:id>', methods=['GET'])
def get_one(id):
    income = Income.query.get(id)
    if income:
        return jsonify(income.serialize())
    return jsonify({'error': 'Income not found'}), 404

@app.route('/api/incomes', methods=['POST'])
def create():
    data = request.get_json()
    income = Income(**data)
    db.session.add(income)
    db.session.commit()
    return jsonify(income.serialize()), 201

@app.route('/api/incomes/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    income = Income.query.get(id)
    if income:
        for key, value in data.items():
            setattr(income, key, value)
        db.session.commit()
        return jsonify(income.serialize())
    return jsonify({'error': 'Income not found'}), 404

@app.route('/api/incomes/<int:id>', methods=['DELETE'])
def delete(id):
    income = Income.query.get(id)
    if income:
        db.session.delete(income)
        db.session.commit()
        return jsonify({'message': 'Income deleted successfully'})
    return jsonify({'error': 'Income not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
