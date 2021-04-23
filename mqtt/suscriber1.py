import paho.mqtt.client as mqtt
import yaml
import paho
import requests

my_json = []
current_temperature = "0"
current_humidity = "0"

TEMP_TOPIC = "/uc3m/classrooms/leganes/myclass/temperature"
HUMIDITY_TOPIC = "/uc3m/classrooms/leganes/myclass/humidity"
DEVICE_INFO_TOPIC = "/uc3m/classrooms/leganes/myclass/device_info"

def submit_data_to_store(data):
    params = get_preferences("measurements_microservice_connector.yaml")
    r = requests.post("http://" + params["server"] + ":" + params["port"] + "/measurements/register", json=data)

def submit_device_info_to_store(data):
    params = get_preferences("measurements_microservice_connector.yaml")
    r = requests.post("http://" + params["server"] + ":" + params["port"] + "/measurements/register", json=data)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado correctamente")
        client.subscribe(TEMP_TOPIC)
        client.subscribe(HUMIDITY_TOPIC)
        client.subscribe(DEVICE_INFO_TOPIC)
    else:
        print("Error de conexión: ", rc)

def get_preferences(file):
    with open(file, 'rb') as f:
        conf = yaml.load(f.read())
    return conf

def on_message(client, userdata, message):
    global current_temperature, current_humidity
    print("Received message =", str(message.payload.decode("utf-8")))

    if message.topic == TEMP_TOPIC:
        current_temperature = float(message.payload.decode("utf-8"))
        data = {"temperature": current_temperature, "humidity": current_humidity}
        submit_data_to_store(data)
        print(data)
    if message.topic == HUMIDITY_TOPIC:
        current_humidity = float(message.payload.decode("utf-8"))
        data = {"temperature": current_temperature, "humidity": current_humidity}
        submit_data_to_store(data)
        print(data)

    if message.topic == DEVICE_INFO_TOPIC:
        r = message.payload.decode("utf-8")
        data = {"device": r}
        submit_device_info_to_store(data)
        print(data)

if __name__ == "__main__":
    params = get_preferences("conf.yaml")
    client = paho.Client()
    client.username_pw_set(username=params["broker_user"], password=params["broker_pwd"])
    client.on_connect = on_connect
    client.on_connect = on_message

    print("connecting to broker ", params["broker_address"])
    client.connect(params["broker_address"], params["broker_port"], params["broker_keep_alive"])

    client.loop_forever()
