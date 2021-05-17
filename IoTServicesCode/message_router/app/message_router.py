import os
import paho.mqtt.client as paho
from device_register_interface import *
from measurement_register_interface import *
import json

my_json = []
current_temperature = "0"
current_humidity = "0"

TEMP_TOPIC = "/uc3m/classrooms/leganes/myclass/temperature"
HUMIDITY_TOPIC = "/uc3m/classrooms/leganes/myclass/humidity"
DEVICE_INFO_TOPIC = "/uc3m/classrooms/leganes/myclass/device_info"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado correctamente")
        client.subscribe(TEMP_TOPIC)
        client.subscribe(HUMIDITY_TOPIC)
        client.subscribe(DEVICE_INFO_TOPIC)
    else:
        print("Error de conexión: ", rc)


def on_message(client, userdata, message):
    global current_temperature, current_humidity
    print("Received message =", str(message.payload.decode("utf-8")))

    if message.topic == TEMP_TOPIC:
        payload = json.loads(message.payload.decode("utf-8"))
        current_temperature = float(payload["data"])
        device_id = payload["device_id"]
        data = {"temperature": current_temperature, "humidity": current_humidity, "device_id": device_id}
        submit_data_to_store(data)

    if message.topic == HUMIDITY_TOPIC:
        payload = json.loads(message.payload.decode("utf-8"))
        current_humidity = float(payload["data"])
        device_id = payload["device_id"]
        data = {"temperature": current_temperature, "humidity": current_humidity, "device_id": device_id}
        submit_data_to_store(data)

    if message.topic == DEVICE_INFO_TOPIC:
        r = message.payload.decode("utf-8")
        data = {"device_id": r}
        submit_device_info_to_store(data)


if __name__ == "__main__":
    BROKER_ADDRESS = os.getenv("BROKER_ADDRESS")
    BROKER_PORT = os.getenv("BROKER_PORT")
    BROKER_KEEP_ALIVE = os.getenv("BROKER_KEEP_ALIVE")
    BROKER_USER = os.getenv("BROKER_USER")
    BROKER_PASSWORD = os.getenv("BROKER_PASSWORD")


    client = paho.Client()
    client.username_pw_set(username=BROKER_USER, password=BROKER_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    print("connecting to broker ", BROKER_ADDRESS)
    client.connect(host=BROKER_ADDRESS, port=int(BROKER_PORT), keepalive=int(BROKER_KEEP_ALIVE))

    client.loop_forever()
