import random
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


def sendLocation():
    while True:
        location = "spain"
        print("gps location -> " + location)
        send_location(location)
        time.sleep(10)


def initializeWeatherSensor():
    # Make connection with the mqtt broker
    make_connection()

    # Register device in database (in case the device is not registered)
    send_id()

    # Set the device to active mode
    send_active()


if __name__ == "__main__":
    # Make mqtt connection and register device in database
    initializeWeatherSensor()

    # Initialize automatic sensor measurer
    print("Starting threads")
    sensors = threading.Thread(target=temperatureAndHumiditySensor)
    location = threading.Thread(target=sendLocation)
    print("Starting location")
    location.start()
    print("Starting sensors")
    sensors.start()

