import os
import sys
import time
from main import *
import easygui as eg
from copy import deepcopy
from graphviz import Digraph
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


if __name__ == '__main__':
    main()

def avara(matriz):
    colores = ['white', 'gray', 'orange', 'red', 'pink', 'green', 'blue']
    cmap = ListedColormap(colores)

    nodosExpandidos = 0
    profundidadArbol = 0
    costo = 0
    arrayExpansion = []
    timeInitial = time.time()

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 5:
                positionBombera = [i, j]

    class Nodo:
        def __init__(self, valor_heuristico, profundidad, padre, posicion_y, posicion_x, hijos, matriz, cubetas, fuego, llenadoagua, hidrante):
            self.valor_heuristico = valor_heuristico
            self.profundidad = profundidad
            self.expandido = False
            self.padre = padre
            self.posicion_y = posicion_y
            self.posicion_x = posicion_x
            self.hijos = hijos
            self.matriz = matriz
            self.cubetas = cubetas
            self.fuego = fuego
            self.hidrante = hidrante
            self.llenadoagua = llenadoagua 
            self.solucion = False
            self.permitirCiclo = False

        def expandir(self, arrayExpansion):
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

            matrizNueva[self.posicion_y][self.posicion_x] = 0

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
                        llenadoagua = 1

                    elif(self.cubetas == 2 and self.llenadoagua == 0):
                        llenadoagua = 2

            elif matrizNueva[posicionAMover_y][posicionAMover_x] == 2: #PUNTO DE FUEGO 
                #los que nunca cambia quiere decir que en toda la ejecucion llega a 0 
                      if (self.cubetas == 1 and self.llenadoagua > 0):
                                  fuego = fuego + 1  
                                  llenadoagua -=1
                                  self.devolver = True

                      elif(self.cubetas == 2 and self.llenadoagua > 0):
                                if self.llenadoagua == 2:
                                    fuego =fuego + 1
                                    llenadoagua -=1
                                    self.devolver = True

                                elif self.llenadoagua == 1:
                                    fuego =fuego + 1
                                    llenadoagua -=1
                                    self.devolver = True

            if self.hidrante ==1:
                  matrizNueva[self.posicion_y][self.posicion_x] = 6
            if(self.llenadoagua == 1):
                  costo += 1
            elif(self.llenadoagua == 2):
                  costo += 2

            valor_heuristico = heuristica(
                matrizNueva, posicionAMover_y, posicionAMover_x)

            matrizNueva[posicionAMover_y][posicionAMover_x] = 5

            nuevohijo = Nodo(valor_heuristico, self.profundidad+1, self, posicionAMover_y, posicionAMover_x,
                             [], matrizNueva, self.cubetas+cubetas,self.fuego+fuego , self.llenadoagua + llenadoagua, hidrante)

            if nuevohijo.mallaIgualAntecesor(self) == False:
                nuevohijo.permitirCiclo = True
            else:
                nuevohijo.permitirCiclo = False

            if self.padre == None:
                arrayExpansion.append(nuevohijo)
                self.hijos.append(nuevohijo)
            else:
                if nuevohijo.permitirCiclo == True:
                    arrayExpansion.append(nuevohijo)
                    self.hijos.append(nuevohijo)
                elif nuevohijo.entraCiclo(self.padre) == False:
                    arrayExpansion.append(nuevohijo)
                    self.hijos.append(nuevohijo)

        def mallaIgualAntecesor(hijo, padre):
            ancestros = padre.encontrarAncestros()
            if hijo.matriz == padre.matriz:
                return True
            for ancestro in ancestros:
                if hijo.matriz == ancestro.matriz:
                    return True
            return False

        def entraCiclo(hijo, padre):
            ancestros = padre.encontrarAncestros()
            if hijo.posicion_x == padre.posicion_x and hijo.posicion_y == padre.posicion_y:
                return True
            for ancestro in ancestros:
                if hijo.posicion_x == ancestro.posicion_x and hijo.posicion_y == ancestro.posicion_y:
                    return True
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
        fuego = posicionfuego(matrizNueva)
        for i in range(len(fuego)):
            temporal = abs(
                posicion_y - fuego[i][0]) + abs(posicion_x - fuego[i][1])
            if temporal < minimo:
                minimo = temporal
        return minimo

    def posicionfuego(matriz):
        posicionfuego = []
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if matriz[i][j] == 6:
                    posicionfuego.append([i, j])
        return posicionfuego

    raiz = Nodo(0, 0, None, positionBombera[0],
                positionBombera[1], [], matriz, 0, 0, 0, 0)

    raiz.valor_heuristico = heuristica(
        raiz.matriz, raiz.posicion_y, raiz.posicion_x)

    arrayExpansion.append(raiz)

    nodoMaestro = None

    while len(arrayExpansion) != 0:
        arrayExpansion.sort(key=lambda x: x.valor_heuristico)
        ##print(len(arrayExpansion))
        if arrayExpansion[0].fuego == 2:
            nodoMaestro = arrayExpansion[0]
            nodoMaestro.solucion = True
            nodoMaestro.expandido = True
            break
        else:
            arrayExpansion[0].expandir(arrayExpansion)
            arrayExpansion.pop(0)

    if not nodoMaestro:
        eg.msgbox(msg="No se encontró una solución con el siguiente input",
                  title="Resultado", image="images/mallabomberita.png")
    else:
        camino = nodoMaestro.encontrarAncestros()
        nodosExpandidos = raiz.nodosExpandidos()
        profundidadArbol = raiz.profundidadArbol()

        # Impresión de resultados
        timeFinal = time.time()
        timeComputing = timeFinal - timeInitial
        eg.msgbox(msg="Se encontró una solución con los siguientes datos:\n\nNodos expandidos: " + str(nodosExpandidos) + "\nProfundidad del árbol: " +
                  str(profundidadArbol) + "\nTiempo de ejecución: " + str(timeComputing)[:10] + " segundos\n\nAhora se visualizará el camino que tomaría la Bombera", title="Resultado")

        # Visualización de camino
        fig, ax = plt.subplots()
        im = ax.imshow(matriz, cmap=cmap, vmin=0, vmax=6)
        plt.xticks([])
        plt.yticks([])
        fig = plt.gcf()
        fig.canvas.manager.set_window_title(
            "Camino de la Bombera para apagar el fuego usando Avara")
        textoCubeta = ax.text(0.2, 1.05, "Cubeta: " + str(0),
                                fontsize=12, ha="center", va="center", transform=ax.transAxes)
        textoFuego = ax.text(0.8, 1.05, "Fuego: " + str(0),
                               fontsize=12, ha="center", va="center", transform=ax.transAxes)

        plt.pause(0.5)
        for i in camino:
            textoSemillas.remove()
            textoFuego.remove()
            textoSemillas = ax.text(0.2, 1.05, "Cubeta: " + str(
                i.cubetas), fontsize=12, ha="center", va="center", transform=ax.transAxes)
            textoFuego = ax.text(0.8, 1.05, "Fuego: " + str(i.fuego),
                                   fontsize=12, ha="center", va="center", transform=ax.transAxes)
            textoSemillas
            textoFuego
            matrizTemp = i.matriz
            im.set_data(matrizTemp)
            plt.draw()
            plt.pause(0.3)
            if not plt.get_fignums():
                break
        time.sleep(1)
        plt.close("all")
