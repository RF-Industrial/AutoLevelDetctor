import os
from pathlib import Path
import subprocess
import time
from libs import capture as cptr
import os


def buscar_y_abrir_archivos():
    # Directorio raíz desde donde comenzar la búsqueda
    directorio_raiz = "./K432/_C"

    # Patrón para buscar directorios
    patron_directorio = "pulse_"

    # Nombre del archivo a buscar y abrir en cada directorio
    nombre_archivo = "chirp.wav"

    # Recorrer los directorios y subdirectorios
    for ruta_actual, directorios, archivos in os.walk(directorio_raiz):
        # Verificar si algún directorio coincide con el patrón
        directorios_coincidentes = [d for d in directorios if d.startswith(patron_directorio)]
        
        # Iterar sobre los directorios coincidentes
        for directorio in directorios_coincidentes:

            print(directorio)
            # Ruta completa del directorio
            ruta_directorio = os.path.join(ruta_actual, directorio)
            
            # Ruta completa del archivo a abrir
            ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
            time.sleep(1)
            # Verificar si el archivo existe en el directorio
            if os.path.exists(ruta_archivo):

                cptr.capture(directorio, 20 , 4)
                #subprocess.Popen(["start", ruta_archivo], shell=True)

                print(f"Archivo '{nombre_archivo}' encontrado en '{ruta_directorio}'")

#buscar_y_abrir_archivos()