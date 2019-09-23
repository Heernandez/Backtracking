
class Pila:
    '''
    En esta pila se guardara el trabajo 
    que genere cada worker y que recibe el fan 
    a traves del sink en un formato json
    '''
    def __init__(self):
        self.items = []
        self.copia = []
    
    def agregar(self,elemento):
        self.items.append(elemento)
        self.copia.append(elemento)
    
    def sacar(self):
        if len(self.items) != 0:
            return self.items.pop()
        else:
            return False
    
    def vacia(self):
        if len(self.items) > 0:
            return False
        else:
            return True