from libs import makeTone as mt
import os

sampling_rate = 44100  # Tasa de muestreo en Hz (número de muestras por segundo)
amplitude = 32767  # Amplitud máxima

# Abrir el archivo exp_neg
#with open("parametros.txt", "r") as archivo:
#with open("chirp_n.txt", "r") as archivo:
with open("exp_neg.txt", "r") as archivo:
    # Leer líneas del archivo
    lineas = archivo.readlines()

# Iterar sobre las líneas
for linea in lineas:
    # Separar los valores de la línea
    start_freq, end_freq, n = linea.strip().split(",")
    f_start_freq = float(start_freq)
    f_end_freq = float(end_freq)
    f_n = float(n)
    print(f"frecInit:{start_freq}, frecEnd:{end_freq}, n:{n} " , end=", ")
    chirp = mt.generate_cycles(f_n, f_start_freq, f_end_freq, sampling_rate, amplitude)
    mt.save_wav(f'pulse_{start_freq}_{end_freq}_{n}','chirp.wav', chirp, sampling_rate)
    
    
    # # Separar los valores de la línea ()
    # start_freq, end_freq, duration = linea.strip().split(",")
    # f_start_freq = float(start_freq)
    # f_end_freq = float(end_freq)
    # f_duration = float(duration)
    # print(f"frecInit:{start_freq}, frecEnd:{end_freq}, tiempo:{duration} " , end=", ")
    # chirp = mt.generate_chirp(f_duration, f_start_freq, f_end_freq, sampling_rate, amplitude)



    duration = linea.strip()
    f_duration = float(duration)
    chirp = mt.generate_exp(f_duration, sampling_rate, amplitude)

    ## Guardar el chirp en un archivo WAV
    mt.save_wav(f'pulse_{duration}','chirp.wav', chirp, sampling_rate)