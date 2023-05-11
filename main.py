from fastapi import FastAPI
import paho.mqtt.client as mqtt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Variável global para armazenar a última mensagem recebida
ultima_mensagem = ""

# Função para atualizar a variável global quando uma nova mensagem é recebida
def on_message(client, userdata, msg):
    global ultima_mensagem
    ultima_mensagem = msg.payload.decode()

def on_connect(client, userdata, flags, rc):
    print("Conectado com sucesso ao broker MQTT.")
    client.subscribe("topico/teste")

# Cria um cliente MQTT
client = mqtt.Client()

# Define a função de callback para recebimento de mensagens
client.on_message = on_message
client.on_connect = on_connect

# Conecta-se ao broker MQTT
client.connect("localhost", 1883)

# Inicia o loop de recebimento de mensagens
client.loop_start()

@app.get("/mensagem")
async def obter_mensagem():
    global ultima_mensagem
    return {"mensagem": ultima_mensagem}


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