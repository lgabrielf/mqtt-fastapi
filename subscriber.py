import time
import random
import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi.responses import Response

# envia informações ao tópico
def send_data():
    client = mqtt.Client("Python")
    conn = client.connect("localhost", 1883, 60)
    msg = random.randint(0,100)
    client.publish("topico/teste", msg)
    client.disconnect()

# enviando a cada 500ms
while True:
    send_data()
    time.sleep(0.5)

# função padrão para se conectar a um tópico específico
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    mqttc.subscribe("topico/teste")

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)