
# Projeto de Cálculo de Litros em Tanques

Este projeto calcula o volume de líquido em um tanque utilizando dados de sensores e informações contidas em uma planilha Excel. O projeto é composto por três arquivos principais: `instaladorPIP.py`, `calcLitro.py` e `conexaoMqtt.py`.

## Estrutura dos Arquivos

### 1. `instaladorPIP.py`

Este arquivo contém uma função para instalar pacotes Python utilizando o pip.

```python
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
```

### 2. `calcLitro.py`

Este arquivo realiza o cálculo do volume de líquido no tanque. Ele lê dados de uma planilha Excel e de um sensor MQTT.

```python
import math
import openpyxl
import conexaoMqtt
import json
import instaladorPIP

def CalcularLitro():
    instaladorPIP.install("openpyxl")
    instaladorPIP.install("python-math")

    radio = float(Planilha('D4'))
    volumeTotal = float(Planilha('E3'))
    comprimento = float(Planilha('D5'))

    dados = conexaoMqtt.run()
    dados = json.loads(dados)

    volume = float(dados.get('Modbus_1_4X161'))  # Volume é o dado que o sensor coleta

    angulo = math.acos((radio - volume) / radio)
    area = radio ** 2 * angulo - (radio - volume) * radio * math.sin(angulo)

    m3 = round(comprimento * area, 4)
    litros = round(m3 * 1000, 2)
    totalTanque = round(volumeTotal - litros, 2)
    
    print(f"{radio} / {volumeTotal}  / {comprimento} / {volume}")
    print(f"Com base nesses dados\nm3={m3}\nEstá faltando {litros}L\nO tanque possui {totalTanque}")

def Planilha(celula):
    arquivoExcel = openpyxl.load_workbook("arquemanto de tanques1.xlsx", data_only=True)
    aba = arquivoExcel['Horizontal']
    sheet = arquivoExcel.active
    dados = sheet[celula]
    valor = float(dados.value)
    return valor

CalcularLitro()
```

### 3. `conexaoMqtt.py`

Este arquivo conecta a um broker MQTT, subscreve a um tópico e recebe dados do sensor.

```python
from paho.mqtt import client as mqtt_client
import random 
import instaladorPIP

broker = "broker.emqx.io"
port = 1883
topic = "data/TesteSensor/statusSensor/+"
client_id = f'subscribe-{random.randint(0, 100)}'
mensagem = []

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Conexão realizada")
        else:
            print(f"Conexão falhou\nCodigo de erro: {rc}")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
    client.on_connect = on_connect
    client.connect(broker, port, 60)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global mensagem 
        mensagem = msg.payload.decode()

    client.subscribe(topic)
    client.on_message = on_message

def run():
    instaladorPIP.install("paho-mqtt")
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    while len(mensagem) < 2: 
        pass
    client.loop_stop()
    client.disconnect()
    return mensagem
```

## Como Executar o Projeto

1. **Instale os pacotes necessários**: O arquivo `instaladorPIP.py` é utilizado para instalar automaticamente os pacotes Python necessários (`openpyxl`, `python-math` e `paho-mqtt`).

2. **Configure e execute o script principal**: O script principal `calcLitro.py` faz o cálculo do volume do líquido no tanque. Ele lê dados de uma planilha Excel (`arquemanto de tanques1.xlsx`) e do sensor MQTT. Certifique-se de que a planilha Excel está no mesmo diretório que o script.

3. **Verifique a conexão MQTT**: O script `conexaoMqtt.py` configura a conexão com o broker MQTT, subscreve ao tópico e coleta dados do sensor.

## Observações

- Certifique-se de que a planilha `arquemanto de tanques1.xlsx` está corretamente preenchida com os dados necessários.
- A estrutura do broker MQTT e do tópico deve estar configurada corretamente para receber os dados do sensor.

## Dependências

- Python 3.x
- Pacotes: `openpyxl`, `paho-mqtt`, `math`

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias e correções.
