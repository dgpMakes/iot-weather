import mysql.connector
import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")


def connect_database():
    mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    return mydb


def device_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO devices (device_id) VALUES (%s)"
        val = params["device_id"]
        device_id = (val,)

        try:
            mycursor.execute(sql, device_id)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except:
            print("Error inserting the device")


def devices_retriever():
    mydb = connect_database()
    r = {}
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT device_id FROM devices ORDER BY id DESC LIMIT 1;")
        myresult = mycursor.fetchall()
        for device_id in myresult:
            r = {"device_id": device_id}
        mydb.commit()
    return r
