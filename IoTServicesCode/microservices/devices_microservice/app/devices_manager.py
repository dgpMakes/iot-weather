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


def device_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO devices (device_id) VALUES (%s)"
        val = params["device_id"]
        device_id = (val,)
        try:
            mycursor.execute(sql, device_id)
        except mysql.connector.Error as error:
            print("Database error: " + str(error), file=sys.stderr)
        mydb.commit()
        mydb.close()
        return "record inserted"


def device_status_update(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        if params["event"] == "active":
            query = "UPDATE devices SET STATUS = " + "'active'" + " WHERE DEVICE_ID = '" + params["device_id"] + "';"
            mycursor.execute(query)
        elif params["event"] == "inactive":
            query = "UPDATE devices SET STATUS = " + "'inactive'" + " WHERE DEVICE_ID = '" + params["device_id"] + "';"
            mycursor.execute(query)

        print(query, file=sys.stderr)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.", file=sys.stderr)
        mydb.close()


def devices_retriever(device=None):
    mydb = connect_database()
    r = []
    with mydb.cursor() as mycursor:
        if device is None:
            query = "SELECT device_id, status, location, date FROM devices ORDER BY date DESC;"
        else:
            query = "SELECT device_id, status, location, date FROM devices WHERE device_id = '" + unquote(device) +\
                    "'  ORDER BY date DESC;"
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        for device_id, status, location, date in myresult:
            r.append({"device_id": device_id, "status": status, "location": location, "date": date})
        mydb.commit()
        mydb.close()

    return {"data": r}


def register_location(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "UPDATE devices set location = '" + params["location"] \
              + "'  WHERE device_id = '" + params["device_id"] + "';"
        print(sql, file=sys.stderr)
        mycursor.execute(sql)
        mydb.commit()
        print("record inserted.", file=sys.stderr)
        mydb.close()
