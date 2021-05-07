import mysql.connector
from load_preferences import getPreferences

def connect_database ():
    file = 'db_conf.yaml'
    params = getPreferences(file)

    mydb = mysql.connector.connect(
        host = params["dbhost"],
        user = params["dbuser"],
        password = params["dbpassword"],
        database = params["dbdatabase"]
    )
    return mydb

def measurements_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        try:
            sql = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"
            val = (params["temperature"], params["humidity"])
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount,"record inserted.")
        except:
            print("Error inserting the device")

def measurements_retriever():
    mydb = connect_database()
    r = []
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT temperature, humidity, date, device_id FROM sensor_data ORDER BY id DESC;")
        myresult = mycursor.fetchall()
        for temperature, humidity, date, device_id in myresult:
            r.append({"temperature": temperature, "humidity": humidity, "date": date, "device": device_id})
        mydb.commit()
    return {"data": r}

