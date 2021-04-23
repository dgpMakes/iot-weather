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

def device_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO devices (device_id) VALUES (%s)"
        val = params["device"]
        device_id = (val,)
        
        try:
            mycursor.execute(sql, device_id)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except:
            print("Error inserting the device")