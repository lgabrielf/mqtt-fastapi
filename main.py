from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig

app = FastAPI()

mqtt_config = MQTTConfig(
    host="192.168.1.208",
    port="1883",
    keepalive=60,
    username="lucas",
    password="teste123"
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #assinando tópico mqtt
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

@mqtt.subscribe("my/mqtt/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

@app.get("/test")
async def func():
    mqtt.publish("/mqtt", "Hello world!")  # publicando tópico mqtt
    return {"result": True, "message": "Published"}

