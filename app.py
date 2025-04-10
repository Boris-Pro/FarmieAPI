from flask import Flask, request, jsonify, session
import mysql.connector
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print("DB_USER:", os.getenv("DB_USER"))
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Secret key for session management

# Database connection
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

@app.route('/signup', methods=['POST'])
def create_user():
    data = request.json
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    query = "INSERT INTO User (user_name, email, password) VALUES (%s, %s, %s)"
    values = (data['user_name'], data['email'], hashed_password)
    cursor.execute(query, values)
    conn.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    query = "SELECT user_id FROM User WHERE email = %s AND password = %s"
    values = (data['email'], hashed_password)
    cursor.execute(query, values)
    user = cursor.fetchone()
    if user:
        session['user_id'] = user[0]
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200

@app.route('/farms', methods=['POST'])
def add_farm():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    data = request.json
    query = "INSERT INTO Farm (user_id, location) VALUES (%s, %s)"
    values = (session['user_id'], data['location'])
    cursor.execute(query, values)
    conn.commit()
    return jsonify({"message": "Farm added successfully"}), 201

@app.route('/crops', methods=['POST'])
def add_crop():
    data = request.json
    query = "INSERT INTO Crop (crop_name, crop_family) VALUES (%s, %s)"
    values = (data['crop_name'], data['crop_family'])
    cursor.execute(query, values)
    conn.commit()
    return jsonify({"message": "Crop added successfully"}), 201

@app.route('/cultivate', methods=['POST'])
def cultivate_crop():
    data = request.json
    query = "INSERT INTO Cultivate (crop_id, farm_id, quantity) VALUES (%s, %s, %s)"
    values = (data['crop_id'], data['farm_id'], data['quantity'])
    cursor.execute(query, values)
    conn.commit()
    return jsonify({"message": "Crop cultivated successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
