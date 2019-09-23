import json
from copy import deepcopy

def esqueleto():
    posibles = [
            [0,0,0,   0,0,0,   0,0,0],
            [0,0,0,   0,0,0,   0,0,0],
            [0,0,0,   0,0,0,   0,0,0],
            
            [0,0,0,   0,0,0,   0,0,0],
            [0,0,0,   0,0,0,   0,0,0],
            [0,0,0,   0,0,0,   0,0,0],
            
            [0,0,0,   0,0,0,   0,0,0],
            [0,0,0,   0,0,0,   0,0,0],
            [0,0,0,   0,0,0,   0,0,0]
        ] 
    return posibles

def espacio_vacio(posibles):
    #retorna la primera casilla vacia que encuentre con menor numero de posibles 
    menor = 9
    x = None
    y = None
    for i in range(len(posibles)):
        for j in range(len(posibles[i])):
            elemento = posibles[i][j]
            if isinstance(elemento,list):
                if len(elemento) > 1 and len(elemento) < menor:
                    menor = len(elemento)
                    x,y = i,j
    #print("las posibilidades mas pocas posibles son de ",menor," en x, y :",x,y)
    return x,y

def mostrar_tablero(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

def verificar_columna(tablero,j):
    numeros = []
    # sacar los numeros en una columna que se quiere verificar
    for i in range(len(tablero)):
        n = tablero[i][j]
        if n != 0:
            numeros.append(n)
    #set elimina las repeticiones y deja elementos unicos
    repeticiones = list( set(numeros))
    if len(numeros) != len(repeticiones):
        #si las listas no coinciden es porque en la columna habia un numero repetido
        return False
    else:
        return True
    
def verificar_fila(tablero,i):
    numeros = []
    #Sacar los numeros en un fila que se quiere verificar
    for n in tablero[i]:
        if n != 0:
            numeros.append(n)
    # set elimina las repeticiones y deja elementos unicos
    repeticiones = list( set(numeros))
    if len(numeros) != len(repeticiones):
        #si las listas no coinciden es porque en la fila habia un numero repetido
        return False
    else:
        return True

def verificar_cuadro(tablero,i,j):
    '''
        calcular el punto inicial del cuadro al que pertenece la coordenada i,j 
        donde se va a a hacer comprobacion de cuadro 
         
    '''
    x = (i // 3)*3
    y = (j // 3)*3

    numeros = []
    # recorrer el cuadro especifico por fila y guardando los numeros que esten fijos
    for f in range(x,x+3):
        for c in range(y,y+3):
            n = tablero[f][c] 
            if n != 0:
                numeros.append(n)

    # set elimina las repeticiones y deja elementos unicos
    repeticiones = list( set(numeros))
    if len(numeros) != len(repeticiones):
        #si las listas no coinciden es porque en el cuadro habia un numero repetido
        return False
    else:
        return True

def validar_marcado(tablero,x,y):
    '''
        para una coordenana donde se hizo un marcado 
        hace verificacion de fila, columna y cuadro

    '''
    return verificar_fila(tablero,x) and verificar_columna(tablero,y) and verificar_cuadro(tablero,x,y)

def verificar_completo(tablero):
    # devuelve true cuando el tablero ya ha sido completado, sin verificar si esta correcto
    for i in tablero:
        for j in i:
            if j == 0:
                return False
    return True

def aparicion_columna(tablero,posibles):
    # buscando por unica aparicion
    # fijar un numero que solo aparezca una vez en una fila de posibles
    #print("Vamos a verificar faciles en columnas")
    for c in range(len(posibles)):
        unico = []
        rep = []
        for f in range(len(posibles[c])):
            elemento = posibles[f][c]
            if isinstance(elemento,list):
                for k in elemento:
                    if k not in unico:
                        unico.append(k)
                    else:
                        rep.append(k)
        
        dif = list(set(unico) - set(rep))

        for f in range(len(posibles[c])):
            elemento = posibles[f][c]
            if isinstance(elemento,list):
                for k in elemento:
                    if k in dif:
                        aux =  tablero[f][c]
                        aux2 = posibles[f][c]
                        tablero[f][c] = k
                        posibles[f][c] = 11
                                    
                        if validar_marcado(tablero,f,c):
                            #print("por columna")
                            #print("el numero ",k, "ubicado en ",f,c)
                            return True,tablero
                        else:
                            tablero[f][c] = aux
                            posibles[f][c] = aux2
                                         
        
    return False,None

def aparicion_fila(tablero,posibles):
    # buscando por unica aparicion
    # fijar un numero que solo aparezca una vez en una fila de posibles
    #print("Vamos a verificar faciles en filas")

    for f in range(len(posibles)):
        unico = []
        rep = []
        for c in range(len(posibles[f])):
            elemento = posibles[f][c]
            if isinstance(elemento,list):
                for k in elemento:
                    if k not in unico:
                        unico.append(k)
                    else:
                        rep.append(k)
        
        dif = list(set(unico) - set(rep))

        for c in range(len(posibles[f])):
            elemento = posibles[f][c]
            if isinstance(elemento,list):
                for k in elemento:
                    if k in dif:
                        aux =  tablero[f][c]
                        aux2 = posibles[f][c]
                        tablero[f][c] = k
                        posibles[f][c] = 11
                                    
                        if validar_marcado(tablero,f,c):
                            
                            #print("por fila")
                            #print("el numero ",k, "ubicado en ",f,c)
                            return True,tablero
                        else:
                            tablero[f][c] = aux
                            posibles[f][c] = aux2
                            
        
    return False,None

def verificar_unica_posibilidad(tablero,posibles):
    # verificar si ese numero es unica posibilidad en ese punto
    # buscando por una posiblilidad
    
    for f in range(len(posibles)):
        for c in range(len(posibles[f])):
            elemento = posibles[f][c]
            if isinstance(elemento,list):
                if len(elemento) == 1:
                    aux =  tablero[f][c]
                    aux2 = posibles[f][c]
                    tablero[f][c] = aux2[0]
                    posibles[f][c] = 11
                    if validar_marcado(tablero,f,c):
                        #print("por unica opcion ","el numero ",aux2[0], "en ",f,c)
                        return True,tablero
                    else:
                        tablero[f][c] = aux
                        posibles[f][c] = aux2
    
    var,t = aparicion_fila(tablero,posibles)
    if var == True:
        return var,t
    else:
        var,t = aparicion_columna(tablero,posibles)
        if var == True:
            return var,t
        else:
            return False,None

def llenar_posibles(tablero):
    # creo una lista de posibles inicializada en ceros 
    posibles = esqueleto()
    '''
        recorrer el tablero, en posibles se marca 11 donde hay un valor en tablero
        y donde no hay valor fijo(es decir, hay  un cero 0),en posibles se llena 
        con un listado de posibles candidatos validos
    '''
    # marco en posibles, los valorea fijos de tablero
    for i in range(len(tablero[0]) ):
        for j in range(len(tablero[0])):
            n = tablero[i][j]
            if n != 0:
                posibles[i][j] = 11
    
    t = tablero.copy()
    for i in range(9):
        for j in range(9):
            
            n = tablero[i][j]
        
            if n == 0: 
                candidatos = []   
                # revisar que numeros podrian estar en esa celda
                
                for num in range(1,10):
                    
                    t[i][j] = num

                    if validar_marcado(t,i,j):
                        candidatos.append(num)
                    
                    t[i][j] = 0
                #print(" para la posicion {},{} tengo posibles a {}".format(i,j,candidatos))
                #_ = input("------")
                posibles[i][j] = candidatos       

    #mostrar_tablero(posibles)
    return posibles

def inferencia(tablero):
    
    posibles = llenar_posibles(tablero)
    #Busco un espacio con pocas opciones de marcado
    x,y = espacio_vacio(posibles)
    # si x y y son None, no habian posibles o hay una lista de posibles vacia(lo que seria un posible error)
    if x != None and y != None and isinstance(posibles[x][y],list):
        
        #print("candidatos ",posibles[x][y])
        #ct = deepcopy(tablero)
        #cp = deepcopy(llenar_posibles(ct))
        for k in posibles[x][y]:
            ct = deepcopy(tablero)
            cp = deepcopy(llenar_posibles(ct))
            #print("para x: {} y:{}  el posible candidato {}".format(x,y,k))
            #_ = input("-------------")
            #aqui creo las ramificaciones, una a la vez para asegurar dfs
            resultado = trabajar(x,y,k,ct,cp)
            
            if resultado == True:
                #solucion final
                tablero = ct
                posibles = llenar_posibles(tablero)
                return True
                
            else:
                pass
                #print("--------------------")
                #print("el camino x:{}  y:{}  con {} no era".format(x,y,k) )
                #print("el tablero que se va a usar ahora va a ser")
                #mostrar_tablero(tablero)
                #print("--------------------")
                
        # si el for anterior finaliza sin haber dado una respuesta significa que recorrio las posibles ramas y ninguna cumplio 
        #print("No hay solucion ni puelchiras")
        return False
        
    #No se hallo solucion
    # Si se viene por este camino, es posible que por un mal marcado, haya en
    #la lista de posibles, para una coordenana una lista de posibles vacia
    elif not verificar_completo(tablero):
        #print("No hay solucion, posiblemente por un mal llenado")
        return False
    
def filtrar(mitablero):
    #mitablero = copiar(tablero)
    #mitablero = deepcopy(tablero)
    #mitablero = tablero
    #mostrar_tablero(tablero)
    var = True
    while var:
        resp,t = verificar_unica_posibilidad(mitablero,llenar_posibles(mitablero))
        if resp :
            # Hubo filtrado
            mitablero = t
        else:
            #el filtrado ya no encuentra mas opciones, hay que pasar a la siguiente fase
            var = False
    
    #print("--------------------------------")
    #print("termino el filtrado")
    
    if verificar_completo(mitablero):
        print("Encontro solucion")
        tablero = mitablero
        mostrar_tablero(mitablero)
        return True
    else:
        resp = inferencia(mitablero)
        if not resp:
            #print("No hay solucion en esta rama")
            return False
        else:
            #print("Tenemos Solucion papi")
            return True

def trabajar(x,y,k,tablero,posibles):
    
    #print("funcion trabajo")
    #num = int( input("ingrese num"))
    num = k
    # intenta poner el numero que le envie
    tablero  [x][y] = num
    posibles [x][y] = 11
    #print("al poner {} quedo".format(num))
    #mostrar_tablero(tablero)
  
    if validar_marcado(tablero,x,y):
        posibles = llenar_posibles(tablero)
        #print("poniendo el {} en {},{} ".format(num,x,y))
        return filtrar(tablero)
    else:
        #print("poniendo el {} en {},{} fallo y me regreso".format(num,x,y))
        return False
            #muere


if __name__ == "__main__":
  
    
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
    print("Problema a Solucionar")
    mostrar_tablero(tablero)
    _ = input("Iniciar")
    resp = filtrar(tablero)
    if not resp :
        print("No tiene solucion")

    