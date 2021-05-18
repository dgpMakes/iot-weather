import uuid
from utils.load_preferences import getPreferences
import paho.mqtt.client as mqtt
import time
import json
import utils.load_preferences

TEMP_TOPIC = "/uc3m/classrooms/leganes/myclass/temperature"
HUMIDITY_TOPIC = "/uc3m/classrooms/leganes/myclass/humidity"
DEVICE_INFO_TOPIC = "/uc3m/classrooms/leganes/myclass/device_info"
LOCATION_TOPIC = "/uc3m/classrooms/leganes/myclass/location"

# Get parameters from config file
params = getPreferences("conf.yaml")


raspberry_id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
raspberry_id += " - Raspberry"


client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected !!!!")
    else:
        print("Connection fail:", {rc})


def make_connection():

    client.username_pw_set(params["broker_user"], params["broker_pwd"])
    client.on_connect = on_connect

    will = json.dumps({"device_id": raspberry_id, "event": "inactive"})
    client.will_set(DEVICE_INFO_TOPIC, will)
    client.connect(params["broker_address"], params["broker_port"], params["broker_keep_alive"])
    print("Connection has been made.")


def send_temperature(temperature):
    pl = json.dumps({"device_id": raspberry_id, "data": temperature})
    client.publish(TEMP_TOPIC, payload=pl, qos=0, retain=False)
    time.sleep(1)


def send_humidity(humidity):
    pl = json.dumps({"device_id": raspberry_id, "data": humidity})
    client.publish(HUMIDITY_TOPIC, payload=pl, qos=0, retain=False)
    time.sleep(1)


def send_id():
    pl = json.dumps({"device_id": raspberry_id, "event": "register"})
    client.publish(DEVICE_INFO_TOPIC, payload=pl, qos=0, retain=False)
    time.sleep(1)


def send_active():
    pl = json.dumps({"device_id": raspberry_id, "event": "active"})
    client.publish(DEVICE_INFO_TOPIC, payload=pl, qos=0, retain=False)
    time.sleep(1)


def send_location(location):
    pl = json.dumps({"device_id": raspberry_id, "location": location})
    client.publish(LOCATION_TOPIC, payload=pl, qos=0, retain=False)
    time.sleep(1)
