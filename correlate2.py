import numpy as np
import sounddevice as sd
import scipy.signal as signal
import librosa
import matplotlib.pyplot as plt

def record_audio(duration, fs):
    """
    Record audio using sounddevice.
    """
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.float32)
    sd.wait()
    return recording.flatten()

def correlate_audio(recording, wav_data):
    """
    Correlate recording with WAV data.
    """
    correlation = signal.correlate(recording, wav_data, mode='full')
    return correlation

# Parámetros de la grabación
duration = 5  # Duración de la grabación en segundos
fs = 44100  # Frecuencia de muestreo en Hz

# Leer archivo WAV
wav_filename1 = 'chirp.wav'
wav_data1, wav_fs = librosa.load(wav_filename1, sr=None)

# Leer archivo WAV
wav_filename2 = 'g__3.wav'
wav_data2, wav_fs2 = librosa.load(wav_filename2, sr=None)

# Grabar audio
#recording = record_audio(duration, fs)

# Correlacionar grabación con datos WAV
#correlation = correlate_audio(recording, wav_data)
correlation = correlate_audio(wav_data1, wav_data2)

# Invertir el array de correlación
correlacion = np.flip(correlation)

# Calcular los retrasos temporales
retrasos = np.arange(-len(wav_data1) + 1, len(wav_data2))

# Calcular el tiempo correspondiente a cada punto en el eje x
tiempo = retrasos / fs

# Visualizar la correlación
plt.plot(tiempo, correlacion)
plt.xlabel('Tiempo (s)')
plt.ylabel('Correlación')
plt.title('Correlación entre la señal original y la señal con eco')
plt.grid(True)
plt.show()