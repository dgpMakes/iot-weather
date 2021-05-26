import requests
import os

MEASUREMENTS_MICROSERVICE_ADDRESS = os.getenv("MEASUREMENTS_MICROSERVICE_ADDRESS")
MEASUREMENTS_MICROSERVICE_PORT = os.getenv("MEASUREMENTS_MICROSERVICE_PORT")


def submit_data_to_store(data):
    r = requests.post('http://' + str(MEASUREMENTS_MICROSERVICE_ADDRESS) + ':' + str(MEASUREMENTS_MICROSERVICE_PORT) + '/measurements/register', json=data)
