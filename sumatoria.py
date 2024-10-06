import os
from pathlib import Path
import subprocess
import time
from libs import capture as cptr
import os
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np


def buscar_y_abrir_archivos():
    # Directorio raíz desde donde comenzar la búsqueda
    directorio_raiz = "./D205AAA/Miercoles"

    # Patrón para buscar directorios
    patron_directorio = "pulse_"    
    patron_archivos = "g__"

    # Recorrer los directorios y subdirectorios
    elementos = os.listdir(directorio_raiz)
    # Verificar si algún directorio coincide con el patrón
    directorios_pulse = [d for d in elementos if d.startswith(patron_directorio)]
    
    for dir in directorios_pulse:
        print(dir)
        ruta_directorio = os.path.join(directorio_raiz, dir)

        archivos = os.listdir(ruta_directorio)
        archivos_g = [d for d in archivos if d.startswith(patron_archivos)]
        
        suma = np.zeros(100000)
        for archivo in archivos_g:
            ruta_archivo = os.path.join(ruta_directorio, archivo)
            print(archivo)
            fs, audio_data = wav.read(ruta_archivo)

            indice = np.argmax(audio_data < -0.1)

            audio_data2 = audio_data[indice:indice+100000]

            if  (len(audio_data2) >= 100000):

                suma = suma + audio_data2

            print(indice)

            duracion = len(audio_data2) / fs
            tiempo =  380 / 2 * duracion * (1.0 / len(audio_data2)) * np.arange(len(audio_data2))

            plt.plot( tiempo,audio_data2)

        plt.plot(tiempo, suma)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.title(dir)
        plt.grid(True)
        plt.show()

buscar_y_abrir_archivos()