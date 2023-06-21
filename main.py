from fastapi import FastAPI, WebSocket
import paho.mqtt.client as mqtt
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI()

ultima_mensagem = None

def on_message(client, userdata, msg):
    global ultima_mensagem
    ultima_mensagem = msg.payload.decode("utf-8")

def on_connect(client, userdata, flags, rc):
    print("Conectado com sucesso ao broker MQTT.")
    client.subscribe("topic/clptest")

client = mqtt.Client()

# callback
client.on_message = on_message
client.on_connect = on_connect
client.connect("localhost", 1883)
client.loop_start()


@app.get("/clp_test")
async def clp_test():
    mensagem_dict = json.loads(ultima_mensagem.replace("'", "\""))
    return mensagem_dict

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Accepting Connection")
    await websocket.accept()
    print("Accepted")
    while True:
        await websocket.send_json(ultima_mensagem)
        await asyncio.sleep(0.5)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)