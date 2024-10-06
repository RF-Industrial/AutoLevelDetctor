from tablas import tabla_seno

def generar_senal_senoidal(frecuencia_inicial, incremento_frecuencia, numero_ciclos, sub = 1):
    """
    Genera una señal senoidal muestreada a partir de una tabla de valores precalculados del seno.

    :param frecuencia_inicial: Frecuencia inicial de la señal senoidal
    :param numero_ciclos: Número de ciclos de la señal a generar
    :param tabla_seno: Lista de valores precalculados de la función seno
    :param incremento_frecuencia: Incremento de la frecuencia después de cada ciclo
    :param divisor_pasos: Divisor utilizado para calcular la cantidad de pasos entre muestras
    :return: Lista con los valores muestreados de la señal
    """
    frecuencia_actual = frecuencia_inicial
    muestras_senial = []
    
    indice_seno = 0 

    for ciclo in range(numero_ciclos):
        # Recorrer la tabla de valores de seno hacia adelante
        while indice_seno  < len(tabla_seno):
            
            valor_seno = tabla_seno[indice_seno] / 4096
            muestras_senial.append(valor_seno)
            indice_seno += frecuencia_actual * sub
            
        frecuencia_actual += incremento_frecuencia 
        indice_seno -= len(tabla_seno)



    return muestras_senial

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    # Parámetros de la señal
    frecuencia_inicial = 110
    numero_ciclos = 2
    incremento_frecuencia = 10



    # Generar la señal senoidal
    senal = generar_senal_senoidal(frecuencia_inicial, numero_ciclos,incremento_frecuencia) 

    # Graficar la señal generada
    plt.plot(senal)
    plt.title('Señal Senoidal Generada')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()