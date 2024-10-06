import os
from pathlib import Path
import subprocess
import time
#from libs import capture as cptr
import os
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
import json

from generar_senial import generar_senal_senoidal

def buscar_y_abrir_archivos(fInit,fStep,n,fSample,nSamples,vSound):
    # Directorio raíz desde donde comenzar la búsqueda
    fs = 959000 / (2**(fSample + 1))

    #directorio_raiz = f"./ECO-GPRS/Compu/3/{fInit}_{fStep}_{n}_{fSample}_{nSamples}"
    directorio_raiz = f"./ECO-GPRS/FONDO/{fInit}_{fStep}_{n}_{fSample}_{nSamples}"
    #ECO-GPRS\FONDO
    archivos = os.listdir(directorio_raiz)
    archivos_g = [d for d in archivos if d.startswith('X')]
  

    chirp_data =  generar_senal_senoidal(fInit,fStep,n,2**(fSample - 6))
    long_Onda =   vSound / 2 / fs * len(chirp_data)
    long_Onda_n =   vSound / 2 / fs * np.arange(len(chirp_data))
    tiempo =  (vSound / 2 / fs * np.arange(nSamples + 1)) - long_Onda/2

    suma = np.zeros(nSamples + 1)
    for archivo in archivos_g:
        ruta_archivo = os.path.join(directorio_raiz, archivo)
        print(archivo)

        with open(ruta_archivo, 'r') as file:
            data = json.load(file)

        audio_data = data['Data']
        audio_data2 = audio_data / np.max(audio_data)
        if  (len(audio_data2) == nSamples + 1):
            suma = suma + audio_data2

        duracion = len(audio_data2) / fs
        #tiempo =  360 / 2 / fs * np.arange(len(audio_data2)) 
        plt.plot( tiempo ,audio_data2)


    indice_inicio = 2000
    correlate =   ( np.correlate(suma,chirp_data,mode="same") ) / 100
    indice_max = indice_inicio + np.argmax(correlate[indice_inicio:])
    fondo = indice_max * vSound / 2 / fs - long_Onda/2

    print (indice_max,correlate[indice_max])
    plt.axvline(x=fondo, color='r', linestyle='--', label=f'Nivel = {round(fondo, 2)} m')
    plt.legend()
    #plt.plot(  tiempo, suma)
    #plt.plot(  long_Onda_n + fondo - long_Onda/2 , chirp_data )
    #plt.plot(  tiempo, correlate)
    plt.xlabel('Distancia (m)')
    plt.ylabel('Amplitud')
    
    plt.title(dir)
    plt.grid(True)
    plt.title("ECOMETRIA POZO D-205 (04/10/2024)")

    plt.show()


   

buscar_y_abrir_archivos(2,2,3,9,6000,352.63)  #2_2_3_9_6000
