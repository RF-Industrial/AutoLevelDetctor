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

def buscar_y_abrir_archivos(fInit,fStep,n,fSample,nSamples):
    # Directorio raíz desde donde comenzar la búsqueda
    DivisorFrec = 2**(fSample - 6)

    fs = int ( 959000 / (2**(fSample + 1)))
    

    directorio_raiz = f"./ECO-GPRS/Domingo/{fInit}_{fStep}_{n}_{fSample}_{nSamples}"

    archivos = os.listdir(directorio_raiz)
    archivos_g = [d for d in archivos if d.startswith('cupla')]
  
    suma = np.zeros(nSamples + 1)
    for archivo in archivos_g:
        ruta_archivo = os.path.join(directorio_raiz, archivo)
        print(archivo)


        # Método 1: Leer todo el archivo de una vez
        with open(ruta_archivo, 'r') as file:
            data = json.load(file)


        audio_data = data['Data']

        audio_data2 = audio_data / np.max(audio_data)

        if  (len(audio_data2) == nSamples + 1):

            suma = suma + audio_data2

        

        duracion = len(audio_data2) / fs
        tiempo =  380 / 2 * duracion * (1.0 / len(audio_data2)) * np.arange(len(audio_data2))

        #plt.plot( audio_data2)

    #suma = suma[int(1000/DivisorFrec):int(10000/DivisorFrec)] 
    suma = suma[900//DivisorFrec:] 

    

    chirp_data =  generar_senal_senoidal(fInit,fStep,n,2**(fSample - 6))

    correlate =   ( np.correlate(suma,chirp_data,mode="same") ) / 100 #np.abs

    windows_len = int(80//DivisorFrec)

    envolvente = np.convolve(correlate, np.ones(windows_len + 1), 'valid') / windows_len + 1

    envolvente = np.pad(envolvente, (0, windows_len), mode='constant', constant_values=0)  - 1
    #peine = 0

    def peinificar (start,step,envolvente):
        # Generar el array de índices

        indices_array = np.arange(start, start + step * 20, step)  # Generamos 20 índices

        # Función para obtener índices válidos
        def get_valid_indices(indices, max_index):
            return indices[indices < max_index]

        # Obtener índices válidos
        valid_indices = get_valid_indices(indices_array, len(envolvente))

        # Realizar la suma
        return (np.sum(envolvente[valid_indices]) , valid_indices)

    peine = 0



    for i in range(300//DivisorFrec, 501//DivisorFrec):
        for j in range(300//DivisorFrec,450): 
            peine_ , valid_indices_ = peinificar(i,j,envolvente)

            if (peine_ > peine):
                peine = peine_
                valid_indices = valid_indices_
                init = i
                paso = j


    #paso = 366
    print(f"Velocidad del sonido = {round( 18.8 / (paso / fs),2)}",  paso , init)

    peine , valid_indices = peinificar(init,paso,envolvente)
    #plt.plot(  suma)
    plt.plot(  chirp_data)
    plt.plot(  correlate)
    plt.plot(  envolvente)
    #plt.plot(  conZeroes)
    #plt.plot( valid_indices, envolvente[valid_indices])
    for i in valid_indices:
        plt.axvline(x=i, color='r', linestyle='--', alpha=0.3)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    
    plt.title(dir)
    plt.grid(True)
    plt.show()


    

buscar_y_abrir_archivos(120,10,2,7,6000)