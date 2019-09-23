import random
import zmq
import time
import json

context = zmq.Context()

# Socket para recibir respuestas de los workers
respuesta = context.socket(zmq.PULL)
respuesta.bind("tcp://*:6000")

# Socket para enviar nuevo trabajo al fan
fan = context.socket(zmq.PUSH)
fan.connect("tcp://localhost:7000")

y = respuesta.recv()

# Recibir resultados
s = respuesta.recv_json()
fan.send_json(s)
    
    
