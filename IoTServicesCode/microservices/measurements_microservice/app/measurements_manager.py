import mysql.connector
import os
import sys
from urllib.parse import unquote

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


def measurements_register(params):
    print("connecting to database", file=sys.stderr)
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO sensor_data (temperature, humidity, device_id) VALUES (%s, %s, %s)"
        print("Received info from " + params["device_id"], file=sys.stderr)
        val = (params["temperature"], params["humidity"], params['device_id'])
        mycursor.execute(sql, val)
        mydb.commit()
        print("record inserted.", file=sys.stderr)
        mydb.close()


def measurements_retriever(device=None, start=None, end=None):
    mydb = connect_database()
    r = []
    print("device requested -> " + str(device), file=sys.stderr)
    with mydb.cursor() as mycursor:
        if device == None:
            mycursor.execute("SELECT temperature, humidity, date, device_id FROM sensor_data ORDER BY date DESC;")
        elif device is not None and start is not None and end is not None:
            query = ("SELECT temperature, humidity, date, device_id" +
                     " FROM sensor_data" +
                     " WHERE date BETWEEN STR_TO_DATE('{start}','%d-%m-%Y %h:%i')"
                     " AND STR_TO_DATE('{end}','%d-%m-%Y %h:%i')" +
                     " ORDER BY date DESC;").format(start=start, end=end)
            mycursor.execute(query)

            print(query)
        else:
            mycursor.execute("SELECT temperature, humidity, date, device_id FROM sensor_data WHERE device_id='"
                             + unquote(device) + "' ORDER BY date DESC;")

        myresult = mycursor.fetchall()
        for temperature, humidity, date, device_id in myresult:
            r.append({"temperature": temperature, "humidity": humidity, "date": date, "device_id": device_id})
        mydb.commit()
        mydb.close()
    return {"data": r}
