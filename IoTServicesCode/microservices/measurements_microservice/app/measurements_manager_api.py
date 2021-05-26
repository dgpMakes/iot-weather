import os

from flask import Flask, request
from flask_cors import CORS
from measurements_manager import *

app = Flask(__name__)
CORS(app)
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


@app.route('/measurements/register', methods=['POST'])
def register_measurement():
    params = request.get_json()
    measurements_register(params)
    return {"result": "record inserted"}, 201


@app.route('/measurements/retrieve')
def retrieve_measurements():
    return measurements_retriever()


@app.route('/measurements/retrieve/<device>')
def retrieve_measurements_by_device(device):
    return measurements_retriever(device=device,
                                  start=request.args.get("start", None),
                                  end=request.args.get("end", None))

app.run(host=HOST, port=PORT, debug=False)