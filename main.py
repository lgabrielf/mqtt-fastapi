from fastapi import FastAPI, BackgroundTasks, APIRouter
from fastapi_mqtt import FastMQTT, MQTTConfig
from fastapi.responses import Response
import asyncio

app = FastAPI()

# Parâmetros de conexão ao Mosquitto
mqtt_config = MQTTConfig(
    host="localhost",
    port="1883",
    keepalive=60,
    username="lucas",
    password="teste123"
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)

data = [] # Armazenar dados recebido do CLP

# Gerador assíncrono para envio ao cliente
async def sse_generator():
    while True:
        if data:
            yield f"data: {data[-1]}\n\n"
        await asyncio.sleep(1)  # Intervalo de tempo

router = APIRouter()

@router.get("/stream")
async def stream(response: Response):
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    async def send_events():
        async for event in sse_generator():
            response.body.send(event.encode("utf-8"))
    
    return await response.start_send(send_events())


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #assinando tópico mqtt
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    data.append(payload.decode()) # Armazenando dados recebidos do CLP

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
async def func(background_tasks: BackgroundTasks):
    mqtt.publish("/mqtt", "Hello world!")  # publicando tópico mqtt
    background_tasks.add_task(send_data_to_clients)
    return {"result": True, "message": "Published"}

def send_data_to_clients():
    # Enviar dados atualizados para os clientes conectados SSE
    # Usar alguma lógica para enviar dados específicos aos clientes apropriados
    while True:
        if data:
            mqtt.publish("/stream", data[-1]) # Publicar dados para o tópico SSE (stream)
        asyncio.sleep(1)


app.include_router(router, prefix="/sse")