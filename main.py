import os
import sys
import easygui as eg
from PIL import Image
#import avara as avara
#import a as a
import matplotlib.pyplot as plt
import Amplitud as amplitud
from matplotlib.colors import ListedColormap
import CostoU as costoU
#import profundidadEvitandoCiclos as profundidad

def main():
    def limpiar_consola():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    colores = ['white', 'gray', 'orange', 'red', 'pink', 'green', 'blue'] #quitar pink

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
        tipoBusqueda = eg.indexbox(msg='¿Qué tipo de búsqueda desea realizar?',
                                   title='BOMBERAS Y FUEGOS',
                                   choices=['Busqueda no Informada', 'Busqueda informada'],
                                   image='Images/mallabomberita.png'
                                   )

        if tipoBusqueda == None:
            sys.exit(0)
        return tipoBusqueda
    
    def preguntarBusquedaNoInformada(matriz):
        noinformada = eg.indexbox(msg='¿Qué tipo de búsqueda desea realizar?',
                                  title='BOMBERAS Y FUEGOS',
                                  choices=['Amplitud', 'Costo Uniforme',
                                           'Profundidad Evitando Ciclos'],
                                  image='Images/mallabomberita.png',
                                  )
        if (noinformada == 0):
            print("Usted seleccionó Amplitud, una ventana aparecerá cuando el algoritmo acabe, si el proceso es demorado significa que sigue expandiendo nodos, si considera que es mucho tiempo puede cortar la ejecución.\n")
            amplitud.amplitud(matriz)
        elif (noinformada == 1):
            print("Usted seleccionó Costo Uniforme, una ventana aparecerá cuando el algoritmo acabe, si el proceso es demorado significa que sigue expandiendo nodos, si considera que es mucho tiempo puede cortar la ejecución.\n")
            costoU.costoU(matriz)
        else:
            sys.exit(0)
    
        limpiar_consola()
    matriz = cargarArchivo()
    tipoBusqueda = preguntarTipoBusqueda()
    if (tipoBusqueda == 0):
        preguntarBusquedaNoInformada(matriz)


    repetir = eg.indexbox(
        msg='¿Desea realizar otra búsqueda?', title='Goku Smart', choices=['Sí, con el mismo archivo', 'Sí, con otro archivo', 'No'])
    print(repetir)
    while repetir >= 0 and repetir <= 2:
        limpiar_consola()
        if (repetir == 0):
            tipoBusqueda = preguntarTipoBusqueda()
            if (tipoBusqueda == 0):
                preguntarBusquedaNoInformada(matriz)
        elif (repetir == 1):
            matriz = cargarArchivo()
            tipoBusqueda = preguntarTipoBusqueda()
            if (tipoBusqueda == 0):
                preguntarBusquedaNoInformada(matriz)
        elif (repetir == 2):
            sys.exit(0)
        repetir = eg.indexbox(
            msg='¿Desea realizar otra búsqueda?', title='Goku Smart', choices=['Sí, con el mismo archivo', 'Sí, con otro archivo', 'No'])


if __name__ == '__main__':
    main()