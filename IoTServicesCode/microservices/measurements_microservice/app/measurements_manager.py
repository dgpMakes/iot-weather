import mysql.connector
import os


DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")


def connect_database ():
    mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    return mydb


def measurements_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        try:
            sql = "INSERT INTO sensor_data (temperature, humidity, device_id) VALUES (%s, %s, %s)"
            val = (params["temperature"], params["humidity"], params["device_id"])
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount,"record inserted.")
        except:
            print("Error inserting the device")

def measurements_retriever():
    mydb = connect_database()
    r = []
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT temperature, humidity, date, device_id FROM sensor_data ORDER BY date DESC;")
        myresult = mycursor.fetchall()
        for temperature, humidity, date, device_id in myresult:
            r.append({"temperature": temperature, "humidity": humidity, "date": date, "device_id": device_id})
        mydb.commit()
    return {"data": r}

