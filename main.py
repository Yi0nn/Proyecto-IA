import os
import sys
import easygui as eg
from PIL import Image
import Avara as avara
import A as a
import matplotlib.pyplot as plt
import Amplitud as amplitud
from matplotlib.colors import ListedColormap
import CostoU as costoU
import ProfundidadECiclos as profundidad
import tkinter as tk
import tkinter.ttk as ttk

def main():
    def limpiar_consola():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    colores = ['#FFF6FF', '#5C0057', '#FF00B5', '#B07DFF', '#B07DFF', '#FFAAD6', '#00D1FF'] #quitar pink

    cmap = ListedColormap(colores)

    tipoBusqueda = 0
    
    def cargarArchivo():
        archivo = eg.fileopenbox(msg='Seleccione el archivo de entrada',
                                 title='BOMBERAS Y FUEGOS',
                                 default="Test/*.txt",
                                 filetypes=["*.txt"],
                                 multiple=False,
                                 )
        
        if archivo is None:
            sys.exit(0)
        archivoInput = open(archivo, 'r')
        matriz = list()

        for i in range(10):
            listaT = []
            for j in range(10):
                listaT.append(int(archivoInput.readline(1)))
                archivoInput.readline(1)
            matriz.append(listaT)
        archivoInput.close()
        plt.imshow(matriz, cmap=cmap)
        plt.xticks([])
        plt.yticks([])
        plt.savefig('Images/mallabomberita.png',
                    bbox_inches='tight', pad_inches=0.05)
        plt.close()
        return matriz

    def preguntarTipoBusqueda():
        tipoBusqueda = eg.indexbox(
                                    msg='                                BOMBERAS Y FUEGOS\n\n                     SELECCIONE EL TIPO DE BUSQUEDA QUE DESEA',
                                   title='PROYECTO #1 IA',
                                   choices=['\nBUSQUEDA \n NO INFORMADA\n', '\nBUSQUEDA\n  INFORMADA\n'],
                                   image='Images/mallabomberita.png'
                                   )

        if tipoBusqueda == None:
            sys.exit(0)
        return tipoBusqueda
    
    def preguntarBusquedaNoInformada(matriz):
        noinformada = eg.indexbox(msg='                                BOMBERAS Y FUEGOS\n\n                        QUE METODO DESEA PARA LA BUSQUEDA',
                                  title='PROYECTO #1 IA',
                                  choices=['\nAMPLITUD\n', '\nCOSTO UNIFORME\n',
                                           '\nPROFUNDIDAD EVITANDO CICLOS\n'],
                                  image='Images/mallabomberita.png',
                                  )
        if (noinformada == 0):
            amplitud.amplitud(matriz)
        elif (noinformada == 1):
            costoU.costoU(matriz)
        elif (noinformada == 2):
            profundidad.ProfundidadECiclos(matriz)
        else:
            sys.exit(0)

    def preguntarBusquedaInformada(matriz):
        informada = eg.indexbox(msg='                                BOMBERAS Y FUEGOS\n\n                        QUE METODO DESEA PARA LA BUSQUEDA',
                                title='PROYECTO #1 IA',
                                choices=['\n   Avara    \n', '\n    A*    \n'],
                                    image='images/mallabomberita.png',
                                )
        if informada == 0:
            avara.avara(matriz)
        elif informada == 1:
            a.a(matriz)
        else:
            sys.exit(0)
    
        limpiar_consola()
    matriz = cargarArchivo()
    tipoBusqueda = preguntarTipoBusqueda()
    if (tipoBusqueda == 0):
        preguntarBusquedaNoInformada(matriz)
    elif (tipoBusqueda == 1):
        preguntarBusquedaInformada(matriz)

    repetir = eg.indexbox(
        msg='\n\n             ¿QUIERES VOLVER A PONER A LA BOMBERITA EN UNA AVENTURA?', title='PROYECTO #1 IA', choices=['SI\n CON EL MISMO LABERITO', 'SI\n CON OTRO LABERITO', 'NO\n QUIERO'])
    print(repetir)
    while repetir >= 0 and repetir <= 2:
        limpiar_consola()
        if (repetir == 0):
            tipoBusqueda = preguntarTipoBusqueda()
            if (tipoBusqueda == 0):
                preguntarBusquedaNoInformada(matriz)
            elif (tipoBusqueda == 1):
                preguntarBusquedaInformada(matriz)
        elif (repetir == 1):
            matriz = cargarArchivo()
            tipoBusqueda = preguntarTipoBusqueda()
            if (tipoBusqueda == 0):
                preguntarBusquedaNoInformada(matriz)
            elif (tipoBusqueda == 1):
                preguntarBusquedaInformada(matriz)
        elif (repetir == 2):
            sys.exit(0)
        repetir = eg.indexbox(
            msg='¿Desea realizar otra búsqueda?', title='BOMBERAS Y FUEGOS', choices=['Sí, con el mismo archivo', 'Sí, con otro archivo', 'No'])


if __name__ == '__main__':
    main()
