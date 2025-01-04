from flask import Flask, jsonify, request
from processor import Processor, bcrypt
from database import db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost/supermarket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Create all tables within the app context
with app.app_context():
    db.create_all()


processor = Processor()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    response = processor.signup(data)
    return jsonify(response), response.get('status_code', 500)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    response = processor.login(data)
    return jsonify(response), response.get('status_code', 500)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    response = processor.add_product(data)
    return jsonify(response), response.get('status_code', 500)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    response = processor.delete_product(product_id)
    return jsonify(response), response.get('status_code', 500)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product_rate(product_id):
    data = request.json
    response = processor.update_product_rate(product_id, data)
    return jsonify(response), response.get('status_code', 500)

@app.route('/purchases', methods=['GET'])
def get_purchases():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    response = processor.get_purchases(start_date, end_date)
    return jsonify(response), response.get('status_code', 500)

@app.route('/users', methods=['GET'])
def get_users():
    response = processor.get_users()
    # Convert each row (tuple) in the response to a dictionary
    response_dict = [{"first_name": r[0], "last_name": r[1],  "total_purchase_amount": r[2]} for r in response]
    return jsonify(response_dict), 200


@app.route('/shampoo', methods=['GET'])
def get_shampoo_sales():
    response = processor.get_shampoo_sales()
    return jsonify(response), response.get('status_code', 500)


if __name__ == '__main__':
    app.run(debug=True)


    
