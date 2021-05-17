import paho.mqtt.client as mqtt
import time

TEMP_TOPIC = "/uc3m/classrooms/leganes/myclass/temperature"
HUMIDITY_TOPIC = "/uc3m/classrooms/leganes/myclass/humidity"
DEVICE_INFO_TOPIC = "/uc3m/classrooms/leganes/myclass/device_info"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected !!!!")
    else:
        print("Connection fail:", {rc})


client = mqtt.Client()


def make_connection():
    client.username_pw_set(username="dso_server", password="dso_password")
    client.on_connect = on_connect

    client.will_set(DEVICE_INFO_TOPIC, '{"status": "Off"}')
    client.connect("34.89.255.226", 1883, 60)
    print ("Connection has been made.")


def send_temperature(temperature):
    client.publish(TEMP_TOPIC, payload=temperature, qos=0, retain=False)
    time.sleep(1)


def send_humidity(humidity):
    client.publish(HUMIDITY_TOPIC, payload=humidity, qos=0, retain=False)
    time.sleep(1)


def send_id(id):
    client.publish(DEVICE_INFO_TOPIC, payload=id, qos=0, retain=False)
    time.sleep(1)
