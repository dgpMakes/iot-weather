from random import random

import paho.mqtt.client as mqtt
import adafruit_dht
import RPi.GPIO as GPIO
import threading
import uuid

from publisher import *
from utils.load_preferences import getPreferences
from board import *


SENSOR_PIN = D17
DHT_SENSOR = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)

client = mqtt.Client()

params = getPreferences("conf.yaml")



def temperatureAndHumiditySensor():
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


def fakeSensors():
    while True:
        try:
            measured_temp = random.randrange(15, 40)
            print("Temperature: " + str(measured_temp) + "ºC ")
            send_temperature(measured_temp)

            measured_humidity = random.randrange(15, 40)
            print("Humidity: " + str(measured_humidity) + "%")
            send_humidity(measured_humidity)

            time.sleep(10)
        except RuntimeError:
            pass

#def humiditySensor():
#    while True:
#        try:
#            measured_humidity = DHT_SENSOR.humidity
#            print("Humidity: " + str(measured_humidity) + "%")
#            send_humidity(measured_humidity)
#
#        except RuntimeError:
#            pass


def initializeWeatherSensor():
    # Make connection with the mqtt broker
    make_connection()

    # Register device in database (necessary before sending any sensor data)
    send_id()


if __name__ == "__main__":
    # Make mqtt connection and register device in database
    initializeWeatherSensor()

    # Initialize automatic sensor measurer
    sensors = threading.Thread(target=fakeSensors())
    sensors.start()

