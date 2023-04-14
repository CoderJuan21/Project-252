from flask import Flask, jsonify, render_template, request
import os
import datetime
from firebase_admin import credentials, initialize_app, firestore
from key import creds
import firebase_admin

app = Flask(__name__)

if not firebase_admin._apps:
    cred = credentials.Certificate(creds)
    default_app = initialize_app(cred)

firebase_db = firestore.client()

@app.route("/add-data", methods=["POST"])
def add_data():
    try:
        temperature = request.json.get("temperature")
        humidity = request.json.get("humidity")
        pressure = request.json.get("pressure")
        altitude = request.json.get("altitude")
        document_ref = firebase_db.collection("data")
        add_values = document_ref.document().create(dict(temperature = temperature, humidty = humidity, altitude = altitude, pressure = pressure, date = datetime.datetime.utcnow()))
        
        return jsonify({
            "status": "success"
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route("/")
def index():
    try:
        document_ref = firebase.db.collection("data")
        data = document_ref.order_by("date", direction = 'DESCENDING').limit(1).get()[0].to_dict()
        return render_template("/home/home.html", data=data)
    except Exception as e:
        print(str(e))
        return jsonify({
            "status":"error",
            "message":"no data in database yet"
        }), 400
   
   
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='http://192.168.43.103:5000/', port=5000)