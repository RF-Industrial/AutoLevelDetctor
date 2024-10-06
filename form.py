import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from libs import makeTone as mt
from libs import capture as cptr
from libs import graphic as grap
import os

sampling_rate = 44100  # Tasa de muestreo en Hz (número de muestras por segundo)
amplitude = 32767  # Amplitud máxima

# Crear la ventana principal
root = tk.Tk()
root.title("Programa de Escritorio en Python")

# Configurar el layout principal
root.geometry("800x600")

# Crear un frame para la barra de botones
frame_buttons = tk.Frame(root)
frame_buttons.pack(side=tk.TOP, fill=tk.X)

# Función para mostrar un mensaje cuando se presiona un botón
def on_button_click(button_number):
    #messagebox.showinfo("Información", f"Has presionado el Botón {button_number}")
    dir = f'{text_box_pozo.get("1.0", tk.END).strip()}/{text_box_nombre.get("1.0", tk.END).strip()}'

    time = text_box_time.get("1.0", tk.END).strip()
    f_time = float(time)

    print(radio_var.get())

    if (radio_var.get() == "Chirp"):
        start_freq = combo_box.get()
        end_freq = combo_box_fEnd.get()
        n = combo_box_N.get()

        file = f'{dir}/pulse_{start_freq}_{end_freq}_{n}'
        
        f_start_freq = float(start_freq)
        f_end_freq = float(end_freq)
        f_n = float(n)


        print(f"frecInit:{start_freq}, frecEnd:{end_freq}, n:{n}")
        chirp = mt.generate_cycles(f_n, f_start_freq, f_end_freq, sampling_rate, amplitude)
        mt.save_wav(f'{dir}/pulse_{start_freq}_{end_freq}_{n}','chirp.wav', chirp, sampling_rate)
        #messagebox.showinfo("Información",f'pulse_{start_freq}_{end_freq}_{n}')
    
    else:
        start_freq = combo_box.get()
        end_freq = combo_box.get()
        f_duration = 1 / float(start_freq)

        duration = "{:.3f}".format(f_duration * 1000)

        file = f'{dir}/pulse_{duration}'

        chirp = mt.generate_exp(f_duration, sampling_rate, amplitude)

        mt.save_wav(file,'chirp.wav', chirp, sampling_rate)


    for k in range(int(button_number)):
        nombre_archivo = cptr.capture(file, 1, f_time)
        tiempo, audio_data = grap.plot(nombre_archivo)
        tiempo_suma, audio_suma = grap.plot(f'{file}/suma.wav')


        ax.clear()
        ax.plot(tiempo, audio_data)
        ax.set_title("Gráfico de ejemplo")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")

        ax2.clear()
        ax2.plot(tiempo_suma, audio_suma, color='red')
        ax2.set_title("suma")
        ax2.set_xlabel("")
        ax2.set_ylabel("Suma")

        canvas.draw()
        root.update_idletasks()

# Crear 5 botones en la barra de botones, cada uno ejecutando la función on_button_click con un argumento diferente
for i in [1,5,10,25,50]:
    btn = tk.Button(frame_buttons, text=f"{i} tiros", command=lambda i=i: on_button_click(i))
    btn.pack(side=tk.LEFT, padx=5, pady=5)

# Crear un frame para los selectores de radio buttons
frame_radio = tk.Frame(root)
frame_radio.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Variable para los radio buttons
radio_var = tk.StringVar()

# Crear 3 radio buttons
for i in ["Dirac","Chirp"]:
    radio_btn = tk.Radiobutton(frame_radio, text=f"{i}", variable=radio_var, value=i)
    radio_btn.pack(anchor=tk.W)

# Crear un combo box
combo_label = tk.Label(frame_radio, text="Frecuencia inicial:")
combo_label.pack(anchor=tk.W, pady=(10, 0))

combo_box = ttk.Combobox(frame_radio, values=["1","2","3","5","7","10","15","20","40","30","50", "60", "70", "80", "90", "100", "110", "120", "130", "140", "150"])
combo_box.pack(anchor=tk.W, pady=5)
combo_box.current(16)

# Crear un combo box
combo_label_fE = tk.Label(frame_radio, text="Frecuencia final:")
combo_label_fE.pack(anchor=tk.W, pady=(10, 0))

combo_box_fEnd = ttk.Combobox(frame_radio, values=["1","2","3","5","7","10","15","20","40","30","50", "60", "70", "80", "90", "100", "110", "120", "130", "140", "150"])
combo_box_fEnd.pack(anchor=tk.W, pady=5)
combo_box_fEnd.current(16)

# Crear un combo box
combo_label_N = tk.Label(frame_radio, text="Cantidad de Ciclos:")
combo_label_N.pack(anchor=tk.W, pady=(10, 0))

combo_box_N = ttk.Combobox(frame_radio, values=["1", "2", "3", "4", "5", "6", "7", "8", "8", "10", "15","20","50","100","1000"])
combo_box_N.pack(anchor=tk.W, pady=5)
combo_box_N.current(0)

# Crear un cuadro de texto
text_label = tk.Label(frame_radio, text="Pozo:")
text_label.pack(anchor=tk.W, pady=(10, 0))

text_box_pozo = tk.Text(frame_radio, height=1, width=30)
text_box_pozo.pack(anchor=tk.W, pady=5)
text_box_pozo.insert("1.0", "Pozo") 

# Crear un cuadro de texto
text_label_nombre = tk.Label(frame_radio, text="Sufijo:")
text_label_nombre.pack(anchor=tk.W, pady=(10, 0))

text_box_nombre = tk.Text(frame_radio, height=1, width=30)
text_box_nombre.pack(anchor=tk.W, pady=5)
text_box_nombre.insert("1.0", "_") 

# Crear un cuadro de texto
text_label_time = tk.Label(frame_radio, text="Tiempo:")
text_label_time.pack(anchor=tk.W, pady=(10, 0))

text_box_time = tk.Text(frame_radio, height=1, width=30)
text_box_time.pack(anchor=tk.W, pady=5)
text_box_time.insert("1.0", "4") 

# Crear un frame para el gráfico
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

# Crear un gráfico usando Matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_plot)

# Crear un gráfico usando Matplotlib
#fig2 = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# Generar datos de ejemplo para el gráfico
x = np.linspace(0, 10*np.pi, 100)
y = np.sin(x)
y2 = np.sin(x)

ax.plot(x, y)
ax.set_title("Gráfico de ejemplo")
ax.set_xlabel("Eje X")
ax.set_ylabel("Eje Y")

ax2.plot(x, y2, color='red')
ax2.set_title("Gráfico de ejemplo2")
ax2.set_xlabel("Eje X")
ax2.set_ylabel("Eje Y")

# Añadir el gráfico a la interfaz Tkinter

canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Crear una barra de herramientas de navegación y añadirla al marco
toolbar = NavigationToolbar2Tk(canvas, frame_plot)
toolbar.update()
toolbar.pack(side=tk.TOP, fill=tk.X)
# Iniciar el bucle principal de la interfaz
root.mainloop()
