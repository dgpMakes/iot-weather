import requests
import os

DEVICES_MICROSERVICE_ADDRESS = os.getenv("DEVICES_MICROSERVICE_ADDRESS")
DEVICES_MICROSERVICE_PORT = os.getenv("DEVICES_MICROSERVICE_PORT")


def submit_device_info_to_store(data):
    requests.post('http://' + str(DEVICES_MICROSERVICE_ADDRESS) + ':' +
                      str(DEVICES_MICROSERVICE_PORT) + '/devices/register', json=data)


def submit_device_status_to_store(data):
    requests.put('http://' + str(DEVICES_MICROSERVICE_ADDRESS) + ':' +
                      str(DEVICES_MICROSERVICE_PORT) + '/devices/status', json=data)


def submit_location_to_store(data):
    requests.put('http://' + str(DEVICES_MICROSERVICE_ADDRESS) + ':' +
                     str(DEVICES_MICROSERVICE_PORT) + '/devices/location', json=data)

