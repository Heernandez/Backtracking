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
newWork = context.socket(zmq.PULL)
newWork.bind("tcp://*:7000")

print("Press enter when workers are ready ...")
_ = input()


sink.send(b'0')

pila = Pila()


   
tablero = [
        [0,0,0,   7,0,0,   0,0,0],
        [1,0,0,   0,0,0,   0,0,0],
        [0,0,0,   4,3,0,   2,0,0],
            
        [0,0,0,   0,0,0,   0,0,6],
        [0,0,0,   5,0,9,   0,0,0],
        [0,0,0,   0,0,0,   4,1,8],
           
        [9,0,0,   0,8,1,   0,0,0],
        [0,0,2,   0,0,0,   0,5,0],
        [0,4,0,   0,0,0,   3,0,0]
    ]

dic = { "tablero" : tablero,
        "n" : None,
        "x" : None,
        "y" : None,
        "prof" : 0
        }

    
poller = zmq.Poller()
poller.register(newWork, zmq.POLLIN)
poller.register(sink, zmq.POLLIN)

workers.send_json(dic)

while True:

    #falta la parte de el dic del poller para recibir del socket newwork 
    # y lo que se reciba se agrega a la pila    
    resp = newWork.recv_json()

    print(resp)

     
    

