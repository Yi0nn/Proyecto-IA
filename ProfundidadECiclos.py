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


def ProfundidadECiclos(matriz):

    colores = ['#FFF6FF', '#5C0057', '#FF00B5', '#B07DFF', '#B07DFF', '#FFAAD6', '#00D1FF']
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
        def __init__(self, costo, profundidad, padre, posicion_y, posicion_x, hijos, matriz, cubetas, fuego, llenadoagua, hidrante):
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
            self.permitirCiclo = False

        def expandir(self, arrayExpansion):
            self.expandido = True

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
                llenadoagua = 0
                hidrante = 0

                matrizNueva[self.posicion_y][self.posicion_x] = 0   #posicion inicial en el nuevo movimiento

                if self.matriz[posicionAMover_y][posicionAMover_x] == 3:
                        cubetas= 1
                        llenadoagua=0

                elif self.matriz[posicionAMover_y][posicionAMover_x] == 4: ##Problema 2 coje la cubeta y no suma en cubeta # problema 3 no desaparece la cubeta
                        cubetas= 2
                        llenadoagua=0

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

                      elif(self.cubetas == 2 and self.llenadoagua > 0):
                                if self.llenadoagua == 2:
                                    fuego =fuego + 1
                                    llenadoagua -=1

                                elif self.llenadoagua == 1:
                                    fuego =fuego + 1
                                    llenadoagua -=1

                if self.hidrante ==1:
                     matrizNueva[self.posicion_y][self.posicion_x] = 6

                if(self.llenadoagua == 1):
                     costo +=1
                elif(self.llenadoagua == 2):
                     costo +=2


                matrizNueva[posicionAMover_y][posicionAMover_x] = 5
                nuevohijo = Nodo(self.costo+costo, self.profundidad+1, self, posicionAMover_y, posicionAMover_x,
                                [], matrizNueva,self.cubetas+cubetas,self.fuego+fuego , self.llenadoagua + llenadoagua, hidrante)

                if nuevohijo.mallaIgualAntecesor(self) == False:
                    nuevohijo.permitirCiclo = True

                if self.padre == None:
                    arrayExpansion.append(nuevohijo)
                    self.hijos.append(nuevohijo)
                else:
                    if self.permitirCiclo == True:
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

    raiz = Nodo(0, 0, None, positionBombera[0],
                positionBombera[1], [], matriz, 0, 0, 0, 0)

    arrayExpansion.append(raiz)

    nodoMaestro = None

    while len(arrayExpansion) != 0:
        arrayExpansion.sort(key=lambda x: x.profundidad, reverse=True)
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
        eg.msgbox(msg="\n\n          LA BOMBERITA NO ENCONTRO LA SOLUCION PARA EL LABERINTO",
                  title="RESULTADO", image="images/mallabomberitas.png")
    else:
        camino = nodoMaestro.encontrarAncestros()
        nodosExpandidos = raiz.nodosExpandidos()
        profundidadArbol = raiz.profundidadArbol()

        timeFinal = time.time()
        timeComputing = timeFinal - timeInitial
        eg.msgbox(msg="\n             LA BOMBERITA ENCONTRO UNA SOLUCION CON ESTOS DATOS\n\n  NODOS:   " + str(nodosExpandidos) + "\n  PROFUNDIDAD DEL ARBOL:  " +
                  str(profundidadArbol) + "\n  TIEMPO: " + str(timeComputing)[:10] + " SEG \n\n                 ESTE FUE EL CAMINO QUE TOMO LA BOMBERITA", title="RESULTADO")

        # Visualización de camino
        fig, ax = plt.subplots()
        im = ax.imshow(matriz, cmap=cmap, vmin=0, vmax=6)
        plt.xticks([])
        plt.yticks([])
        fig = plt.gcf()
        fig.canvas.manager.set_window_title(
            "BUSQUEDA PROFUNDIDAD EVITANDO CICLOS")
        textoCubeta = ax.text(0.2, 1.05, "NO. CUBETAS: " + str(0)+"\n ",
                                fontsize=12, ha="center", va="center", transform=ax.transAxes)
        textoFuego = ax.text(0.8, 1.05, "FUEGOS APAGADOS: " + str(0)+"\n ",
                               fontsize=12, ha="center", va="center", transform=ax.transAxes)

        plt.pause(0.5)
        for i in camino:
            textoCubeta.remove()
            textoFuego.remove()
            textoCubeta = ax.text(0.2, 1.05, "NO. CUBETAS: " + str(
                i.cubetas)+"\n ", fontsize=12, ha="center", va="center", transform=ax.transAxes)
            textoFuego = ax.text(0.8, 1.05, "FUEGOS APAGADOS: " + str(i.fuego)+"\n ",
                                   fontsize=12, ha="center", va="center", transform=ax.transAxes)
            textoCubeta
            textoFuego
            matrizTemp = i.matriz
            im.set_data(matrizTemp)
            plt.draw()
            plt.pause(0.5)
            if not plt.get_fignums():
                break
        time.sleep(1)
        plt.close("all")
