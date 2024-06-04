
import math
import openpyxl
import conexaoMqtt
import json
import instaladorPIP


def CalcularLitro():
    instaladorPIP.install("openpyxl")
    instaladorPIP.install("python-math")
    radio=float(Planilha('D4'))
    volumeTotal=float(Planilha('E3'))
    comprimento= float(Planilha('D5'))

    dados = conexaoMqtt.run()
    dados = json.loads(dados)

    volume = float(dados.get('Modbus_1_4X161'))  #Volume é o dado que o sensor coleta


    angulo=math.acos((radio-volume)/radio)
    area= radio**2*angulo-(radio-volume)*radio*math.sin(angulo)

    m3= round(comprimento * area,4)
    litros=round(m3*1000,2)
    totalTanque=round(volumeTotal-litros,2)
    print(f"{radio} / {volumeTotal}  / {comprimento} / {volume}")
    print(f"Com base nesses dados\nm3={m3}\nEstá faltando {litros}L\nO tanque possui {totalTanque}")




def Planilha(celula):
    arquivoExcel=openpyxl.load_workbook("arquemanto de tanques1.xlsx",data_only = True)
    aba= arquivoExcel['Horizontal']
    sheet= arquivoExcel.active
    dados=sheet[celula]
    valor= float(dados.value)
    return valor

CalcularLitro()