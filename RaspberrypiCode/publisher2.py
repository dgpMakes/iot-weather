import adafruit_dht
import RPi.GPIO as GPIO
#import Adafruit_DHT
import datetime

import time
import threading

import uuid
from board import *
import time
from datetime import date
import paho.mqtt.client as mqtt

SENSOR_PIN = D17;
DHT_SENSOR = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
client = mqtt.Client()

def submit_data_to_store(data):
    params = getPreferences("")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected !!!!")
    else:
        print("Connection fail:", {rc})

def make_connection():
    client.username_pw_set(username="diego", password="superdiego")
    client.on_connect = on_connect
    client.connect("34.89.255.226", 1883, 60)

    print ("Connection has been made.")

def weatherSensor():

    make_connection()
    id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    print(id)
    send_id(id+" - Raspberry 1")

def send_temperature(temperature):
    client.publish('/uc3m/classrooms/leganes/myclass/temperature', payload = temperature, qos = 0,retain = False)
    time.sleep(1)

def send_humidity(humidity):
    client.publish('/uc3m/classrooms/leganes/myclass/humidity', payload = humidity, qos = 0,retain = False)
    time.sleep(1)

def send_id(id):
    client.publish('/uc3m/classrooms/leganes/myclass/device_info', payload = id, qos = 0, retain = False)
    time.sleep(1)

def temperatureSensor():
    while True:
        try:
            measured_temp = DHT_SENSOR.temperature
            print("Temperature: " + str(measured_temp) + "ºC ")
            send_temperature(measured_temp)

            measured_humidity = DHT_SENSOR.humidity
            print("Humidity: " + str(measured_humidity) + "%")
            send_humidity(measured_humidity)

            time.sleep(10)
        except RuntimeError:
            pass

def humiditySensor():
    while True:
        try:
            measured_humidity = DHT_SENSOR.humidity
            print("Humidity: " + str(measured_humidity) + "%")
            send_humidity(measured_humidity)

        except RuntimeError:
            pass

if __name__ == "__main__":
    weatherSensor()
    temperature = threading.Thread(target=temperatureSensor())
#    humidity = threading.Thread(target=humiditySensor())
    temperature.start()
#humidity.start()



