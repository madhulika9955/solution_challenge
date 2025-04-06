from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pandas as pd

app = Flask(__name__)

# ✅ Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# ✅ Function to Fetch and Display Full Table
def display_users_table():
    with app.app_context():
        users = User.query.all()

        if not users:
            print("No users found in the database.")
        else:
            # Convert to a structured table using Pandas
            user_data = [{
                "ID": user.id,
                "Name": user.name,
                "Age": user.age,
                "Sex": user.sex,
                "Phone": user.phone_number,
                "Email": user.email,
                "Voter ID": user.voter_id,
                "Aadhar Number": user.aadhar_number,
                "Address": user.address
            } for user in users]

            # Create DataFrame and Print
            df = pd.DataFrame(user_data)
            print("\nFull User Table:\n")
            print(df.to_string(index=False))  # Print full table without index

# ✅ Run the function
if __name__ == "__main__":
    print("Fetching full user table...\n")
    display_users_table()
