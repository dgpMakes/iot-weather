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