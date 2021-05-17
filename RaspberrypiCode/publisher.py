import uuid
import load_preferences
import paho.mqtt.client as mqtt
import time
import utils.load_preferences

TEMP_TOPIC = "/uc3m/classrooms/leganes/myclass/temperature"
HUMIDITY_TOPIC = "/uc3m/classrooms/leganes/myclass/humidity"
DEVICE_INFO_TOPIC = "/uc3m/classrooms/leganes/myclass/device_info"

# Get parameters from config file
params = load_preferences.getPreferences("conf.yaml")


raspberry_id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
raspberry_id += " - Raspberry"
client = mqtt.Client(client_id=raspberry_id)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected !!!!")
    else:
        print("Connection fail:", {rc})


def make_connection():

    client.username_pw_set(params["dso_server"], params["dso_password"])
    client.on_connect = on_connect

    client.will_set(DEVICE_INFO_TOPIC, '{"status": "off"}')
    client.connect(params["broker_address"], params["broker_port"], params["broker_keep_alive"])
    print("Connection has been made.")


def send_temperature(temperature):
    client.publish(TEMP_TOPIC, payload=temperature, qos=0, retain=False)
    time.sleep(1)


def send_humidity(humidity):
    client.publish(HUMIDITY_TOPIC, payload=humidity, qos=0, retain=False)
    time.sleep(1)


def send_id():
    client.publish(DEVICE_INFO_TOPIC, payload=raspberry_id, qos=0, retain=False)
    time.sleep(1)
