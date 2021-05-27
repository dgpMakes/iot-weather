import os
from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
PROTOCOL = "http://"

DEVICES_MICROSERVICE_SERVER = os.getenv("DEVICES_MICROSERVICE_SERVER")
DEVICES_MICROSERVICE_PORT = os.getenv("DEVICES_MICROSERVICE_PORT")
MEASUREMENTS_MICROSERVICE_SERVER = os.getenv("MEASUREMENTS_MICROSERVICE_SERVER")
MEASUREMENTS_MICROSERVICE_PORT = os.getenv("MEASUREMENTS_MICROSERVICE_PORT")
PORT = os.getenv("PORT")
HOST = os.getenv("HOST")


@app.route('/dso/measurements')
def get_sensor_data():
    response = requests.get(PROTOCOL + MEASUREMENTS_MICROSERVICE_SERVER + ":" +
                            MEASUREMENTS_MICROSERVICE_PORT + "/measurements/retrieve")
    return response.content


@app.route('/dso/devices')
def get_device_list():
    response = requests.get(PROTOCOL + DEVICES_MICROSERVICE_SERVER + ":" +
                            DEVICES_MICROSERVICE_PORT + "/devices/retrieve")
    return response.content


@app.route('/dso/devices/<device>')
def get_device_data(device):
    start = request.args.get("start", None)
    end = request.args.get("end", None)
    params = {"start": start,
              "end": end}
    response = requests.get(PROTOCOL + MEASUREMENTS_MICROSERVICE_SERVER + ":" +
                            MEASUREMENTS_MICROSERVICE_PORT + "/measurements/retrieve/" + device,
                            params=params)
    return response.content


app.run(host=HOST, port=PORT, debug=False)
