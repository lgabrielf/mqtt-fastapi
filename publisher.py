import time
import random
import paho.mqtt.client as mqtt
import json

# simula comportamento do CLP para teste via websocket
client = mqtt.Client("Python")
client.connect("localhost", 1883)

def simulate_cpl():

    while True:
        
        hole_depth = random.randint(100, 109)
        bit_diam = 12.25
        caliper = round(random.uniform(12.0, 13.5), 3)
        GR = round(random.uniform(30.0, 160.0), 2)
        RES = round(random.uniform(30.0, 200.0), 2)
        Sonic = round(random.uniform(30.0, 200.0), 2)
        MSE = round(random.uniform(2000.0, 16000.0), 1)
        dxc = round(random.uniform(0.2, 0.9), 4)
        ECD = round(random.uniform(10.0, 20.0), 2)
        lag_time = round(random.uniform(1.0, 10.0), 2)
        flow = round(random.uniform(20.0, 40.0), 2)
        lag_depth = round(random.uniform(20.0, 40.0), 2)
        c1 = random.randint(0, 100)
        c2 = random.randint(0, 2000)

        payload = {
            "hole_depth": hole_depth,
            "bit_diam": bit_diam,
            "caliper": caliper,
            "GR": GR,
            "RES": RES,
            "Sonic": Sonic,
            "MSE": MSE,
            "dxc": dxc,
            "ECD": ECD,
            "lag_time": lag_time,
            "flow": flow,
            "lag_depth": lag_depth,
            "c1": c1,
            "c2": c2
        }

        # json_payload = json.dumps(payload)
        client.publish("topic/clptest", payload=str(payload))
        print(f"Published: {payload}")
        time.sleep(0.5)
    

simulate_cpl()
