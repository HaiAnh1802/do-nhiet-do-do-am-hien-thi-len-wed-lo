import paho.mqtt.client as mqtt
import time
import mysql.connector
import json

from datetime import datetime


############

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "haianh123",
    database = "iot_mcb"
)
mycursor = mydb.cursor()

def on_connect(client, userdata, flags, rc):
    client.subscribe("haianh/data")


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    
    dulieu = str(message.payload.decode("utf-8"))
    data_in = json.loads(dulieu)

    temp = str(data_in["temp"])
    humi = str(data_in["humi"])

    now = datetime.now()
    cur_time = now.strftime("%Y-%m-%d %H:%M:%M")
    

    #sql = "INSERT INTO test(temp, humi, light) VALUES(" + temp + "," + humi + "," + light +")"
    sql = "INSERT INTO sensor(temp, humi, updtime) VALUES(%s, %s, %s)"
    val = (temp, humi, cur_time)

    mycursor.execute(sql, val)
    mydb.commit()
    
    
########################################
broker_address="broker.hivemq.com"
#broker_address="iot.eclipse.org"

client = mqtt.Client("mangcbthayuy") 


print("Subscribing to topic","haianh/data")

client.on_connect = on_connect

client.on_message=on_message
    
client.connect(broker_address, 1883) #connect to broker

client.loop_forever()


    







