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
        sql = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"
        val = (params["temperature"], params["humidity"])
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount,"record inserted.")