import random
import zmq
import time
import hashlib
from pila import Pila

context = zmq.Context()

# Socket para enviar trabajo a los workers
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5000")

# Socket para confirmar conexion con el sink
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:6000")

# Socket para recibir trabajo desde el sink para ser distribuido
newWork = context.socket(zmq.REP)
newWork.bind("tcp://*:7000")

print("Press enter when workers are ready ...")
_ = input()

#sink.send(b'0')

pila = Pila()
tablero = [
        [8,0,0,   0,0,0,   9,0,0],
        [0,0,0,   0,9,5,   6,0,0],
        [7,0,1,   0,6,0,   0,0,0],
        
        [5,0,0,   3,0,0,   0,7,0],
        [0,3,0,   0,0,8,   0,0,2],
        [0,0,0,   0,0,4,   0,3,0],
           
        [0,0,0,   0,0,6,   0,9,0],
        [0,0,0,   0,0,0,   0,0,5],
        [1,0,8,   4,0,0,   0,0,0]
    ]
dic = { "tablero" : tablero,
        "n" : None,
        "x" : None,
        "y" : None,
        "prof" : 0
        }
pila.agregar(dic)

poller = zmq.Poller()
poller.register(newWork, zmq.POLLIN)
while True:
    try:
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break

    if newWork in socks:
        m = newWork.recv_json()
        pila.agregar(m)
        newWork.send(b'0')
                
    if not pila.vacia():
        workers.send_json(pila.sacar())
    else:
        print("no hay")
    
   
        
             
    

