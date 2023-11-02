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

    colores = ['white', 'gray', 'orange', 'red', 'green', 'blue', 'yellow', 'pink']
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
        def __init__(self, costo, profundidad, padre, posicion_y, posicion_x, hijos, matriz, cubetas, fuego, hidrante, cubellena1l, cubellena2l):
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
            self.hidrante = hidrante
            self.cubellena1l = cubellena1l
            self.cubellena2l = cubellena2l
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
                hidrante = 0
                cubellena1l= 1
                cubellena2l= 2

                matrizNueva[self.posicion_y][self.posicion_x] = 0   #posicion inicial en el nuevo movimiento


                if self.matriz[posicionAMover_y][posicionAMover_x] == 2: #PUNTO DWE FUEGO 
                    if (self.cubellena1l == 1):
                        costo = 1
                        cubellena1l = 0
                        self.devolver = True
                        #ultimaPelea = 3
                    elif(self.cubellena2l == 2):
                        costo = 2
                        cubellena2l = 1
                        self.devolver = True
                    
                    elif(self.cubellena2l == 1):
                        costo = 1
                        cubellena2l = 1
                        self.devolver = True
                    else:
                        print("sino")
                        self.devolver = True
                        #semillas -= 1  // poner el que se quede en la posicion anterior o que la posicion siguiente sea un bloqueo

                elif self.matriz[posicionAMover_y][posicionAMover_x] == 3:
                        costo = 1
                        cubetas= 1
                        
                elif self.matriz[posicionAMover_y][posicionAMover_x] == 4:
                        costo = 1
                        cubetas= 2


                elif matrizNueva[posicionAMover_y][posicionAMover_x] == 6:#hidrante
                    if(self.cubetas == 1):
                        costo= 2
                        cubellena1l= 1
                        self.devolver = True
                    elif(self.cubetas == 2):
                        costo= 3
                        cubellena2l =2
                        self.devolver = True
                    else:
                        costo=1
    ###PARA NOSOSTRAS DEVOLVER ES CUANDO RECOJE LA CUBETA LLENA DE AWA
                
                if self.cubetas == 1:
                    matrizNueva[self.posicion_y][self.posicion_x] = 3
                elif self.cubetas == 2:
                    matrizNueva[self.posicion_y][self.posicion_x] = 4
                
                #SE SUPONE QUE ESTA ES LA NUEVA MATRIZ CON EL MOVIMIENTO QUE SE REALIZO SE S U P O N E 
                matrizNueva[posicionAMover_y][posicionAMover_x] = 2
                nuevohijo = Nodo(self.costo+costo, self.profundidad+1, self, posicionAMover_y, posicionAMover_x,
                                [], matrizNueva, self.cubellena1l+cubellena1l,self.cubellena2l+cubellena2l, self.fuego+fuego, cubetas)
                
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

