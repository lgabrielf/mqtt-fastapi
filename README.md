# fastapi-mqtt

Projeto para comunicação com MQTT Broker utilizando FastAPI como intermediador.

---

### 🔨 Instalação

Iniciando o broker MQTT

```sh
 $ docker run --name fastapi_mqtt -p 1883:1883 -p 9001:9001 -d eclipse-mosquitto:1.6.15
```

Copiando arquivos de configuração

```sh
 $ docker cp config\mosquitto.conf fastapi_mqtt:/mosquitto/config/mosquitto.conf
```

### ⚙ How to run

```sh
 pip install -r requirements.txt 
```

```sh
 python main.py
 python subscriber.py
```
E na pasta frontend

```sh
 npm start
```
