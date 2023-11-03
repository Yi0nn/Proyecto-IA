import os
import sys
import time
import numpy as np
from main import *
import easygui as eg
from copy import deepcopy
from graphviz import Digraph
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

if __name__ == '__main__':
    main()

def amplitud(matriz):

    colores = ['white', 'gray', 'orange', 'red', 'pink', 'green', 'blue']
    cmap = ListedColormap(colores)

    nodosExpandidos = 0
    profundidadArbol = 0
    costo = 0
    arrayExpansion = []
    timeInitial = time.time()

    for i in range(len(matriz)):#para recorrer las lineas de la matriz
        for j in range(len(matriz[i])):# para recorrer espacios de la matriz 
            if matriz[i][j] == 5: # posicion inicial
                positionGoku = [i, j]#posicion x y 

    class Nodo:
        # nuevohijo = Nodo(self.costo+costo, self.profundidad+1, self, posicionAMover_y, posicionAMover_x,
                #[], matrizNueva,  self.fuego+fuego ,self.cubetas+cubetas, ultimacubeta)
        def __init__(self, costo, profundidad, padre, posicion_y, posicion_x, hijos, matriz, cubetas, fuego, ultimacubeta): #11 argumentos
            self.costo = costo
            self.profundidad = profundidad
            self.expandido = False
            self.padre = padre#posicion inicial del punto del arbol 
            self.posicion_y = posicion_y
            self.posicion_x = posicion_x
            self.hijos = hijos # lo que sacan los partes
            self.matriz = matriz
            self.cubetas = cubetas
            self.fuego = fuego

            self.ultimacubeta = ultimacubeta ## prueba

            self.solucion = False
            self.devolver = False

        def expandir(self, arrayExpansion):#array expansion arbol
                self.expandido = True #habilita la expansion

                ##Probabilidad de expansion del arbol
                #MOVIMIENTOS 

                if self.posicion_y > 0:
                    arriba = self.matriz[self.posicion_y-1][self.posicion_x]
                    if arriba != 1:
                        # print(("Se puede mover hacia arriba"))
                        self.crearHijo(self.posicion_y-1,
                                    self.posicion_x, arrayExpansion)

                if self.posicion_y < len(self.matriz) - 1:
                    abajo = self.matriz[self.posicion_y+1][self.posicion_x]
                    if abajo != 1:
                        # print(("Se puede mover hacia abajo"))
                        self.crearHijo(self.posicion_y+1,
                                    self.posicion_x, arrayExpansion)

                if self.posicion_x < len(self.matriz[self.posicion_y]) - 1:
                    derecha = self.matriz[self.posicion_y][self.posicion_x+1]
                    if derecha != 1:
                        # print(("Se puede mover hacia derecha"))
                        self.crearHijo(self.posicion_y,
                                    self.posicion_x+1, arrayExpansion)

                if self.posicion_x > 0:
                    izquierda = self.matriz[self.posicion_y][self.posicion_x-1]
                    if izquierda != 1:
                        # print(("Se puede mover hacia izquierda"))
                        self.crearHijo(self.posicion_y,
                                    self.posicion_x-1, arrayExpansion)
                        
        def crearHijo(self, posicionAMover_y, posicionAMover_x, arrayExpansion):
                matrizNueva = deepcopy(self.matriz)
                costo = 1
                cubetas = 0
                fuego = 0
                ultimacubeta = 0

                matrizNueva[self.posicion_y][self.posicion_x] = 0   #posicion inicial en el nuevo movimiento


                if self.matriz[posicionAMover_y][posicionAMover_x] == 2: #PUNTO DWE FUEGO 
                    #los que nunca cambia quiere decir que en toda la ejecucion llega a 0 
                    if (self.cubetas == 2):
                        costo +=1
                        cubetas = 1 #cambie
                        fuego = fuego + 1  
                        self.devolver = True
                        print('PUNTO DE FUEGOOOOOOOO')
                        print('cantidad de cubetas que existe hasta ahora',cubetas) #esto nunca cambia 
                        print('cantidad de fuegos apagados hasta ahora', fuego) #estoo tampoco nunca cambia
                        print('costo que va hasta ahora', costo) #esto siempre se mantiene en 1 
                        print('ultima cubeta que no se que sea la vdd', ultimacubeta) #esto nunca cambia 
                            #ultimaPelea = 3
                    if(self.cubetas == 3) :
                        costo +=2
                        cubetas = 2 # cambie
                        fuego =fuego + 1
                        self.devolver = True
                        print('PUNTO DE FUEGOOOOOOOO')
                        print('cantidad de cubetas que existe hasta ahora',cubetas) #esto nunca cambia 
                        print('cantidad de fuegos apagados hasta ahora', fuego) #estoo tampoco nunca cambia
                        print('costo que va hasta ahora', costo) #esto siempre se mantiene en 1 
                        print('ultima cubeta que no se que sea la vdd', ultimacubeta) #esto nunca cambia 
                    else:
                        print("NO TIENE CUBETA")
                        print('PUNTO DE FUEGOOOOOOOO')
                        print('cantidad de cubetas que existe hasta ahora',cubetas) #esto nunca cambia 
                        print('cantidad de fuegos apagados hasta ahora', fuego) #estoo tampoco nunca cambia
                        print('costo que va hasta ahora', costo) #esto siempre se mantiene en 1 
                        print('ultima cubeta que no se que sea la vdd', ultimacubeta) #esto nunca cambia 

                elif self.matriz[posicionAMover_y][posicionAMover_x] == 3:
                        
                        print('CUBETA DE UN LITROOOOOOOOOOOOOOOO')
                        print('cantidad de cubetas que existe hasta ahora',cubetas)
                        print('cantidad de fuegos apagados hasta ahora', fuego)
                        print('costo que va hasta ahora', costo)
                        print('ultima cubeta que no se que sea la vdd', ultimacubeta)
                        costo += 1
                        cubetas= 1
                        ultimacubeta = 3
                        self.devolver=True 
                        
                elif self.matriz[posicionAMover_y][posicionAMover_x] == 4: ##Problema 2 coje la cubeta y no suma en cubeta # problema 3 no desaparece la cubeta
                        print('CUBETA DE DOS LITROOOOOOOOOOOOOOOOOOOOOOOOOO')
                        print('cantidad de cubetas que existe hasta ahora',cubetas)
                        print('cantidad de fuegos apagados hasta ahora', fuego)
                        print('costo que va hasta ahora', costo)
                        print('ultima cubeta que no se que sea la vdd', ultimacubeta)
                        costo += 1 #problema 3 que esto llega a ser el final 
                        cubetas= 2
                        ultimacubeta = 4

                elif matrizNueva[posicionAMover_y][posicionAMover_x] == 6:#hidrante ## problema #1 no tiene cubeta y coje awa 
                    if(self.cubetas == 1):
                        costo+= 2
                        cubetas= 2 #cambie
                        print('AWITAAAAAAAAAAAAAAAAAAAAAAAA para 1l')
                        print('cantidad de cubetas que existe hasta ahora',cubetas)
                        print('cantidad de fuegos apagados hasta ahora', fuego)
                        print('costo que va hasta ahora', costo)
                        print('ultima cubeta que no se que sea la vdd', ultimacubeta)
                        self.devolver = True
                    if(self.cubetas == 2):
                        costo+= 3
                        cubetas = 3 #cambie 
                        print('AWITAAAAAAAAAAAAAAAAAAAAAAAA paraa 2l')
                        print('cantidad de cubetas que existe hasta ahora',cubetas)
                        print('cantidad de fuegos apagados hasta ahora', fuego)
                        print('costo que va hasta ahora', costo)
                        print('ultima cubeta que no se que sea la vdd', ultimacubeta)
                        self.devolver = True
                    else:
                        costo+=1
    ###PARA NOSOSTRAS DEVOLVER ES CUANDO RECOJE LA CUBETA LLENA DE AWA

                # if self.ultimacubeta >0:  MODIFICAR PARA QUE EL HIDRANTE QUEDE NICE esto es pa dejar la cosa fija 
                #     matrizNueva[self.posicion_y][self.posicion_x] = 6

                
                #SE SUPONE QUE ESTA ES LA NUEVA MATRIZ CON EL MOVIMIENTO QUE SE REALIZO SE S U P O N E 
                matrizNueva[posicionAMover_y][posicionAMover_x] = 2
                nuevohijo = Nodo(self.costo+costo, self.profundidad+1, self, posicionAMover_y, posicionAMover_x,
                                [], matrizNueva,self.cubetas+cubetas,self.fuego+fuego ,   ultimacubeta)
                
                if self.padre == None:
                    arrayExpansion.append(nuevohijo)
                    self.hijos.append(nuevohijo)
                else:
                    if self.padre.devolver == True:
                        arrayExpansion.append(nuevohijo)
                        self.hijos.append(nuevohijo)
                    elif nuevohijo.seDevuelve(self.padre) == False:
                        arrayExpansion.append(nuevohijo)
                        self.hijos.append(nuevohijo)

        def seDevuelve(hijo, padre):
                if hijo.posicion_x == padre.posicion_x and hijo.posicion_y == padre.posicion_y:
                    return True
                else:
                    return False

        def imprimirMatriz(self):
                for i in range(len(self.matriz)):
                    for j in range(len(self.matriz[i])):
                        print(self.matriz[i][j], end=' ')
                    print()
                print()
        def encontrarAncestros(self):
            ancestros = []
            ancestros.append(self)
            ancestro = self.padre
            while ancestro != None:
                ancestros.append(ancestro)
                ancestro = ancestro.padre
            ancestros.reverse()
            return ancestros

        def generarposicion(self):
            return str(self.posicion_y) + " , " + str(self.posicion_x)

        def nodosExpandidos(self):
            nodos = 0
            if self.expandido == True:
                nodos += 1
                for i in self.hijos:
                    nodos += i.nodosExpandidos()
            return nodos

        def profundidadArbol(self):
            profundidad = self.profundidad
            for i in self.hijos:
                profundidad = max(profundidad, i.profundidadArbol())
            return profundidad

        def generarMatrizString(self):
            matrizString = ""
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz[i])):
                    matrizString += str(self.matriz[i][j])
                matrizString += "\n"
            return matrizString
        
    
    ####IMPORTANTE 
    # nuevohijo = Nodo(self.costo+costo, self.profundidad+1, self, posicionAMover_y, posicionAMover_x,[], matrizNueva,  self.fuego+fuego ,self.cubetas+cubetas, ultimacubeta)
    raiz = Nodo(0, 0, None, positionGoku[0],
                positionGoku[1], [], matriz, 0, 0, 0)

    arrayExpansion.append(raiz)

    nodoMaestro = None

    while len(arrayExpansion) != 0:
        if arrayExpansion[0].fuego == 2:
            nodoMaestro = arrayExpansion[0]
            nodoMaestro.solucion = True
            nodoMaestro.expandido = True
            # nodoMaestro.expandir(arrayExpansion)
            break
        else:
            arrayExpansion[0].expandir(arrayExpansion)
            arrayExpansion.pop(0)

    if not nodoMaestro:
        eg.msgbox(msg="No se encontró una solución con el siguiente input",
                  title="Resultado", image="images/mallaGokuSmart.png")
    else:
        camino = nodoMaestro.encontrarAncestros()
        nodosExpandidos = raiz.nodosExpandidos()
        profundidadArbol = raiz.profundidadArbol()
        costo = nodoMaestro.costo

        timeFinal = time.time()
        timeComputing = timeFinal - timeInitial
        eg.msgbox(msg="Se encontró una solución con los siguientes datos:\n\nNodos expandidos: " + str(nodosExpandidos) + "\nProfundidad del árbol: " +
                  str(profundidadArbol) + "\nTiempo de ejecución: " + str(timeComputing)[:10] + " segundos\n\nAhora se visualizará el camino que tomaría la bombera", title="Resultado")
        


        fig, ax = plt.subplots()
        im = ax.imshow(matriz, cmap=cmap, vmin=0, vmax=6)
        plt.xticks([])
        plt.yticks([])
        fig = plt.gcf()
        fig.canvas.manager.set_window_title(
            "Camino de Goku para encontrar las esferas del dragón usando Amplitud")
        textoSemillas = ax.text(0.2, 1.05, "Semillas actuales: " + str(0),
                                fontsize=12, ha="center", va="center", transform=ax.transAxes)
        textoEsferas = ax.text(0.8, 1.05, "Esferas actuales: " + str(0),
                               fontsize=12, ha="center", va="center", transform=ax.transAxes)

        plt.pause(0.5)
        for i in camino:
            textoSemillas.remove()
            textoEsferas.remove()
            textoSemillas = ax.text(0.2, 1.05, "Semillas actuales: " + str(
                i.ultimacubeta), fontsize=12, ha="center", va="center", transform=ax.transAxes)
            textoEsferas = ax.text(0.8, 1.05, "Esferas actuales: " + str(i.fuego),
                                   fontsize=12, ha="center", va="center", transform=ax.transAxes)
            textoSemillas
            textoEsferas
            matrizTemp = i.matriz
            im.set_data(matrizTemp)
            plt.draw()
            plt.pause(0.3)
            if not plt.get_fignums():
                break
        time.sleep(1)
        plt.close("all")