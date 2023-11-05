import sys
import os
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


def a(matriz):
    colores = ['white', 'gray', 'orange', 'red', 'pink', 'green', 'blue']
    cmap = ListedColormap(colores)

    nodosExpandidos = 0
    profundidadArbol = 0
    costo = 0
    arrayExpansion = []
    timeInitial = time.time()

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 2:
                positionGoku = [i, j]

    class Nodo:
        def __init__(self, costo, profundidad, padre, posicion_y, posicion_x, hijos, matriz, cubetas, fuego, llenadoagua, hidrante): #11 argumentos
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
            self.llenadoagua = llenadoagua ## prueba
            self.solucion = False
            self.costo_real = costo_real ##nuevo
            self.costo_suma = costo_real + valor_heuristico ##nuevo
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
                        
                if self.posicion_x > 0:
                    izquierda = self.matriz[self.posicion_y][self.posicion_x-1]
                    if izquierda != 1:
                        # print(("Se puede mover hacia izquierda"))
                        self.crearHijo(self.posicion_y,
                                    self.posicion_x-1, arrayExpansion)

                if self.posicion_x < len(self.matriz[self.posicion_y]) - 1:
                    derecha = self.matriz[self.posicion_y][self.posicion_x+1]
                    if derecha != 1:
                        # print(("Se puede mover hacia derecha"))
                        self.crearHijo(self.posicion_y,
                                    self.posicion_x+1, arrayExpansion)
     
        def crearHijo(self, posicionAMover_y, posicionAMover_x, arrayExpansion):
                matrizNueva = deepcopy(self.matriz)
                costo = 1
                cubetas = 0
                fuego = 0
                llenadoagua = 0
                hidrante = 0

                matrizNueva[self.posicion_y][self.posicion_x] = 0   #posicion inicial en el nuevo movimiento

                if self.matriz[posicionAMover_y][posicionAMover_x] == 3:
                        cubetas= 1
                        llenadoagua=0
                        self.devolver=True 

                elif self.matriz[posicionAMover_y][posicionAMover_x] == 4: ##Problema 2 coje la cubeta y no suma en cubeta # problema 3 no desaparece la cubeta
                        cubetas= 2
                        llenadoagua=0
                        self.devolver =True

                elif self.matriz[posicionAMover_y][posicionAMover_x] == 6 :#hidrante ## problema #1 no tiene cubeta y coje awa 
                    hidrante = 1
                    if(self.cubetas == 1 and self.llenadoagua == 0):
                        costo = 2
                        llenadoagua = 1
                        self.devolver= True

                    elif(self.cubetas == 2 and self.llenadoagua == 0):
                        costo = 3
                        llenadoagua = 2
                        self.devolver= True
                
                elif matrizNueva[posicionAMover_y][posicionAMover_x] == 2: #PUNTO DE FUEGO 
                #los que nunca cambia quiere decir que en toda la ejecucion llega a 0 
                      if (self.cubetas == 1 and self.llenadoagua > 0):
                                  costo = 1
                                  fuego = fuego + 1  
                                  llenadoagua -=1
                                  self.devolver = True

                      elif(self.cubetas == 2 and self.llenadoagua > 0):
                                if self.llenadoagua == 2:
                                    costo = 2
                                    fuego =fuego + 1
                                    llenadoagua -=1
                                    self.devolver = True

                                elif self.llenadoagua == 1:
                                    costo = 1
                                    fuego =fuego + 1
                                    llenadoagua -=1
                                    self.devolver = True

                if self.hidrante ==1:
                     matrizNueva[self.posicion_y][self.posicion_x] = 6

                #self.imprimirMatriz()
                #SE SUPONE QUE ESTA ES LA NUEVA MATRIZ CON EL MOVIMIENTO QUE SE REALIZO SE S U P O N E 
                matrizNueva[posicionAMover_y][posicionAMover_x] = 5

                nuevohijo = Nodo(self.costo_real + costo, valor_heuristico, self.profundidad+1, self, posicionAMover_y, posicionAMover_x,
                                [], matrizNueva, self.cubetas+cubetas,self.fuego+fuego , self.llenadoagua + llenadoagua, hidrante)

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

    def heuristica(matrizNueva, posicion_y, posicion_x):
        minimo = float('inf')
        fuego = posicionFuego(matrizNueva)
        for i in range(len(fuego)):
            # if fuego[i][0] == posicion_y and fuego[i][1] == posicion_x:
            #     return 0
            # else:
            if abs(posicion_y - fuego[i][0]) + abs(posicion_x - fuego[i][1]) < minimo:
                minimo = abs(
                    posicion_y - fuego[i][0]) + abs(posicion_x - fuego[i][1])
                # fuego.pop(i)
        # print("valor heuristico: ", minimo)
        return minimo

    def posicionFuego(matriz):
        posicionFuego = []
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if matriz[i][j] == 6:
                    posicionFuego.append([i, j])
        return posicionFuego

    raiz = Nodo(0, 0, 0, None, positionGoku[0],
                positionGoku[1], [], matriz, 0, 0, 0)

    raiz.valor_heuristico = heuristica(
        raiz.matriz, raiz.posicion_y, raiz.posicion_x)

    arrayExpansion.append(raiz)

    nodoMaestro = None

    while len(arrayExpansion) != 0:
        arrayExpansion.sort(key=lambda x: x.costo_suma)
        # print([Nodo.valor_heuristico for Nodo in arrayExpansion])
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
        costo = nodoMaestro.costo_real

        # Se imprime el camino con valores de profundidad y costo
        # for i in camino:
        #     i.imprimirMatriz()
        #     print("profundidad: ", i.profundidad, "valor heuristico: ", i.valor_heuristico, "costo real: ", i.costo_real, "costo suma: ", i.costo_suma)
        #     print()

        # Generación de grafos
        # def generar_grafo_1(nodo, grafo):
        #     temp = "Matriz:\n"+nodo.generarMatrizString()+"\nCon valor: " + \
        #         str(nodo.costo) + "\nExpandido: "+str(nodo.expandido)
        #     grafo.node(str(id(nodo)), label=temp)
        #     for hijo in nodo.hijos:
        #         grafo.edge(str(id(nodo)), str(id(hijo)))
        #         generar_grafo_1(hijo, grafo)
        # grafo1 = Digraph()
        # generar_grafo_1(raiz, grafo1)
        # grafo1.render('grafo', view=True)

        # Impresión de resultados
        timeFinal = time.time()
        timeComputing = timeFinal - timeInitial
        eg.msgbox(msg="Se encontró una solución con los siguientes datos:\n\nNodos expandidos: " + str(nodosExpandidos) + "\nProfundidad del árbol: " +
                  str(profundidadArbol) + "\nCosto de la solución: " + str(costo) + "\nTiempo de ejecución: " + str(timeComputing)[:10] + " segundos\n\nAhora se visualizará el camino que tomaría Goku", title="Resultado")

        # Visualización de camino
        fig, ax = plt.subplots()
        im = ax.imshow(matriz, cmap=cmap, vmin=0, vmax=6)
        plt.xticks([])
        plt.yticks([])
        fig = plt.gcf()
        fig.canvas.manager.set_window_title(
            "Camino de Goku para encontrar las fuego del dragón usando A*")
        textoSemillas = ax.text(0.2, 1.05, "Semillas actuales: " + str(0),
                                fontsize=12, ha="center", va="center", transform=ax.transAxes)
        textofuego = ax.text(0.8, 1.05, "fuego actuales: " + str(0),
                               fontsize=12, ha="center", va="center", transform=ax.transAxes)

        plt.pause(0.5)
        for i in camino:
            textoSemillas.remove()
            textofuego.remove()
            textoSemillas = ax.text(0.2, 1.05, "Semillas actuales: " + str(
                i.semillas), fontsize=12, ha="center", va="center", transform=ax.transAxes)
            textofuego = ax.text(0.8, 1.05, "fuego actuales: " + str(i.fuego),
                                   fontsize=12, ha="center", va="center", transform=ax.transAxes)
            textoSemillas
            textofuego
            matrizTemp = i.matriz
            im.set_data(matrizTemp)
            plt.draw()
            plt.pause(0.3)
            if not plt.get_fignums():
                break
        time.sleep(1)
        plt.close("all")
