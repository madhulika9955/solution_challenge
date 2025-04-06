from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# ✅ Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"

db = SQLAlchemy(app)

# ✅ Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    voter_id = db.Column(db.String(20), nullable=False, unique=True)
    aadhar_number = db.Column(db.String(20), nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# ✅ Create database tables if they do not exist
if not os.path.exists("users2.db"):
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully!")

# ✅ Serve Registration Page
@app.route('/')
def index():
    return render_template('registration.html')

# ✅ Registration API
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        required_fields = ["name", "age", "sex", "phone_number", "email", "voter_id", "aadhar_number", "address", "password"]
        if not all(data.get(field) for field in required_fields):
            return jsonify({"error": "All fields are required!"}), 400

        # ✅ Check if user already exists
        existing_user = User.query.filter(
            (User.email == data['email']) | 
            (User.phone_number == data['phone_number']) | 
            (User.voter_id == data['voter_id']) | 
            (User.aadhar_number == data['aadhar_number'])
        ).first()

        if existing_user:
            return jsonify({"error": "User with given details already exists!"}), 400

        # ✅ Hash Password
        hashed_password = generate_password_hash(data['password'])

        # ✅ Create new user
        new_user = User(
            name=data['name'],
            age=int(data['age']),
            sex=data['sex'],
            phone_number=data['phone_number'],
            email=data['email'],
            voter_id=data['voter_id'],
            aadhar_number=data['aadhar_number'],
            address=data['address'],
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ✅ Login API
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        aadhar_number = data.get('aadhar')
        password = data.get('password')

        if not aadhar_number or not password:
            return jsonify({"error": "Aadhar number and password are required!"}), 400

        user = User.query.filter_by(aadhar_number=aadhar_number).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return jsonify({"message": "Login successful!", "user": {"id": user.id, "name": user.name, "email": user.email}}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Logout API
@app.route('/api/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

# ✅ Run Server
if __name__ == '__main__':
    app.run(debug=True)
