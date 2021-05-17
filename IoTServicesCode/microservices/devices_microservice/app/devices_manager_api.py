from flask import Flask, request
from flask_cors import CORS

from devices_manager import *

app = Flask(__name__)
CORS(app)
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


@app.route('/devices/register/', methods=['POST'])
def save_device_info():
    parameters = request.get_json()
    device_register(parameters)
    return {"result": "record inserted"}, 201


@app.route('/devices/retrieve/')
def retrieve_devices():
    return devices_retriever()


app.run(host=HOST, port=PORT)
