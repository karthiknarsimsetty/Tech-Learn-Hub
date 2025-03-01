from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

EXCEL_FILE = "users.xlsx"

# Function to initialize the Excel file if it doesn't exist
def initialize_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=["Email", "Password"])
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Users", index=False)

# Function to read users from Excel
def read_users_from_excel():
    df = pd.read_excel(EXCEL_FILE, sheet_name="Users")
    return df.to_dict(orient="records")

# Initialize Excel on startup
initialize_excel()

# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    users = read_users_from_excel()
    for user in users:
        if user["Email"] == email and user["Password"] == password:
            return jsonify({"success": True, "message": "Login successful"})
    
    return jsonify({"success": False, "message": "Invalid email or password"}), 401

# Signup API
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    users = read_users_from_excel()
    
    # Check if user already exists
    if any(user["Email"] == email for user in users):
        return jsonify({"success": False, "message": "User already exists"}), 400
    
    # Add new user
    new_user = {"Email": email, "Password": password}
    users.append(new_user)
    
    df = pd.DataFrame(users)
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Users", index=False)
    
    return jsonify({"success": True, "message": "Account created successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
