import sys
import time
import zmq
from funciones import *
#contexto para la creacion de sockets
context = zmq.Context()

# Socket para la comunicacion con el fan para recibir trabajo
w = context.socket(zmq.PULL)
w.connect("tcp://localhost:5000")

# Socket para enviar mas trabajo generado al sink
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:6000")

# Recibir trabajo
while True:
    
    s = w.recv_json()
    
    if s["n"] == None:
        tablero = s["tablero"]
        
        filtrar(tablero,sink)
    else:
        tablero = s["tablero"] 
        n = s["n"]
        x = s["x"]
        y = s["y"]
        poner_numero(tablero,n,x,y,sink)
    
   

