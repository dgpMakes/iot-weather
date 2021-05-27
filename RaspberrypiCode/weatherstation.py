import random
import paho.mqtt.client as mqtt
import adafruit_dht
import RPi.GPIO as GPIO
import threading
import uuid
import serial
import time
import string
import pynmea2

from RPLCD import CharLCD

from publisher import *
from utils.load_preferences import getPreferences
from board import *


#GPIO.setmode(GPIO.BCM)
SENSOR_PIN = D4
DHT_SENSOR = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)

client = mqtt.Client()

params = getPreferences("conf.yaml")

# Initalize global variables to store last temperature
last_measured_temp = None
last_measured_humidity = None

# To use the LED screen

LCD_RS = 25
LCD_E  = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 18
LCD_D7 = 22

temperatureToReturn = 0
humidityToReturn = 0

#button setup
mode = 0
def changeDisplayMode():
    if mode == 0:
        mode = 1
    if mode == 1:
        mode = 0

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(16,GPIO.RISING,callback=changeDisplayMode) # Setup event on pin 16 rising edge



def temperatureAndHumiditySensor():
    while True:
        try:
            global last_measured_temp
            global last_measured_humidity

            measured_temp = DHT_SENSOR.temperature
            if measured_temp != last_measured_temp \
                    or (last_measured_temp is None and measured_temp is not None):
                print("Temperature: " + str(measured_temp) + "ºC ")
                temperatureToReturn = measured_temp
                send_temperature(measured_temp)
                last_measured_temp = measured_temp

            measured_humidity = DHT_SENSOR.humidity
            if measured_humidity != last_measured_humidity \
                    or (last_measured_humidity is None and measured_humidity is not None):
                print("Humidity: " + str(measured_humidity) + "%")
                humidityToReturn = measured_humidity
                send_humidity(measured_humidity)
                last_measured_humidity = measured_humidity

            time.sleep(10)
        except RuntimeError:
            pass


def sendLocation():
    while True:
        port = "/dev/ttyAMA0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        try:
            newdata = ser.readline().decode("utf-8")
        except UnicodeDecodeError:
            continue

        if newdata[0:6] == "$GPRMC":
            newmsg = pynmea2.parse(newdata)
            lat = newmsg.latitude
            lng = newmsg.longitude
            location = str(lat) + ", " + str(lng)
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
    # Make mqtt connection and register device in datab
    initializeWeatherSensor()

    # Initialize automatic sensor measurer
    print("Starting threads")
    sensors = threading.Thread(target=temperatureAndHumiditySensor)
    location = threading.Thread(target=sendLocation)
    print("Starting location")
    location.start()
    print("Starting sensors")
    sensors.start()

    lcd = CharLCD(cols=16, rows=2, pin_rs=LCD_RS, pin_e=LCD_E, pins_data=[LCD_D4, LCD_D5, LCD_D6, LCD_D7],
                  numbering_mode=GPIO.BCM)

    while True:
        print("Display funcionando!")

        if mode == 0:

            if temperatureToReturn >=5 or temperatureToReturn <= 50:
                lcd.write_string(u'Temperature: ' + str(temperatureToReturn) + 'ºC ')
            else:
                lcd.write_string(u'Temperature: ERROR')

        if mode == 1:
            if humidityToReturn >= 0 or humidityToReturn <= 100:
                lcd.write_string(u'Humidity: ' + str(humidityToReturn) + '% ')
            else:
                lcd.write_string(u'Humidity: ERROR')

        time.sleep(5)
        lcd.clear()








