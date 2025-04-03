from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="farm_db"
)
cursor = conn.cursor()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    query = "INSERT INTO User (user_name, email, password) VALUES (%s, %s, %s)"
    values = (data['user_name'], data['email'], data['password'])
    cursor.execute(query, values)
    conn.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/farms', methods=['POST'])
def add_farm():
    data = request.json
    query = "INSERT INTO Farm (user_id, location) VALUES (%s, %s)"
    values = (data['user_id'], data['location'])
    cursor.execute(query, values)
    conn.commit()
    return jsonify({"message": "Farm added successfully"}), 201

@app.route('/crops', methods=['POST'])
def add_crop():
    data = request.json
    query = "INSERT INTO Crop (crop_name, crop_type) VALUES (%s, %s)"
    values = (data['crop_name'], data['crop_type'])
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
