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

# Initalize global variables to store last temperature
last_measured_temp = None
last_measured_humidity = None


def temperatureAndHumiditySensor():
    while True:
        try:
            global last_measured_temp
            global last_measured_humidity

            measured_temp = DHT_SENSOR.temperature
            if measured_temp != last_measured_temp \
                    or (last_measured_temp is None and measured_temp is not None):
                print("Temperature: " + str(measured_temp) + "ºC ")
                send_temperature(measured_temp)
                last_measured_temp = measured_temp

            measured_humidity = DHT_SENSOR.humidity
            if measured_humidity != last_measured_humidity \
                    or (last_measured_humidity is None and measured_humidity is not None):
                print("Humidity: " + str(measured_humidity) + "%")
                send_humidity(measured_humidity)
                last_measured_humidity = measured_humidity

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

