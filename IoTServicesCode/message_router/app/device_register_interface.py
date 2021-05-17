import requests
import os

DEVICES_MICROSERVICE_ADDRESS = os.getenv("DEVICES_MICROSERVICE_ADDRESS")
DEVICES_MICROSERVICE_PORT = os.getenv("DEVICES_MICROSERVICE_PORT")


def submit_device_info_to_store(data):
    r = requests.post('http://' + str(DEVICES_MICROSERVICE_ADDRESS) + ':' + str(DEVICES_MICROSERVICE_PORT) + '/devices/register/', json=data)
