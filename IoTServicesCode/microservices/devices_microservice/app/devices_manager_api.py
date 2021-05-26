from flask import Flask, request
from flask_cors import CORS

from devices_manager import *

app = Flask(__name__)
CORS(app)
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


@app.route('/devices/register', methods=['POST'])
def register_device_info():
    parameters = request.get_json()
    result = device_register(parameters)
    return {"result": result}, 201


@app.route("/devices/status", methods=['PUT'])
def update_device_state():
    parameters = request.get_json()
    device_status_update(parameters)
    return {"result": "status updated"}, 201


@app.route('/devices/retrieve')
def retrieve_devices():
    return devices_retriever()


@app.route('/devices/location', methods=['PUT'])
def update_device_location():
    parameters = request.get_json()
    register_location(parameters)
    return {"result": "location updated"}, 201


app.run(host=HOST, port=PORT, debug=False)
