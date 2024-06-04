from paho.mqtt import client as mqqt_client
import random 
import instaladorPIP
#pip install paho-mqtt

broker = "broker.emqx.io"
port = 1883
topic = "data/TesteSensor/statusSensor/+"
client_id = f'subscribe-{random.randint(0,100)}'
mensagem = []

def connect_mqtt() -> mqqt_client:

    def on_connect(client,userdata,flags,rc,properties):
        if rc == 0:
            print("Conexão realizada")
        else:
            print(f"Conexão falhou\n Codigo de erro:{rc}")
    client = mqqt_client.Client(mqqt_client.CallbackAPIVersion.VERSION2,client_id)
    client.on_connect = on_connect
    client.connect(broker,port,60)
    return client

def subscribe(client:mqqt_client):
    def on_message(client,userdata,msg):
      global mensagem 
      mensagem = msg.payload.decode()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    instaladorPIP.install("paho-mqtt")
    client=connect_mqtt()
    subscribe(client)
    client.loop_start()
    while len(mensagem) < 2: 
        pass
    client.loop_stop()
    client.disconnect()
    return mensagem

