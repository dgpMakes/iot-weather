import requests
from load_preferences import getPreferences


def submit_device_info_to_store(data):
    params = getPreferences("devices_microservice_connector.yaml")
    r = requests.post('http://' + str(params["server"]) + ':' + str(params["port"]) + '/devices/register', json=data)

