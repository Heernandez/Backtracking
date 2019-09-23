import random
import zmq
import time
import json
from funciones import mostrar_tablero

context = zmq.Context()

# Socket para recibir respuestas de los workers
respuesta = context.socket(zmq.PULL)
respuesta.bind("tcp://*:6000")

# Socket para enviar nuevo trabajo al fan
fan = context.socket(zmq.PUSH)
fan.bind("tcp://*:7000")

y = respuesta.recv()

# Recibir resultados
i = 1
while True:
    s = respuesta.recv_json()
    if s["n"] == 100:
        print("Solucion")
        mostrar_tablero(s["tablero"])
        break
    print("rama",i)
    i+=1
    fan.send_json(s)
    
while True:
    s = respuesta.recv_json()
    
