import sys
import time
import zmq
from funciones import *

# Socket para la comunicacion con el fan para recibir trabajo
w = context.socket(zmq.PULL)
w.connect("tcp://localhost:5000")

# Recibir trabajo
while True:
    
    s = w.recv_json()
    
    if s["n"] == None:
        tablero = s["tablero"]
        filtrado(s)
    else:
        tablero = s["tablero"] 
        n = s["n"]
        x = s["x"]
        y = s["y"]
        poner_numero(tablero,n,x,y)
    
  

