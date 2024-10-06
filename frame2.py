import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
    messagebox.showinfo("Información", f"Has presionado el Botón {button_number}")

# Crear 5 botones en la barra de botones, cada uno ejecutando la función on_button_click con un argumento diferente
for i in range(1, 6):
    btn = tk.Button(frame_buttons, text=f"Botón {i}", command=lambda i=i: on_button_click(i))
    btn.pack(side=tk.LEFT, padx=5, pady=5)

# Crear un frame para los selectores de radio buttons
frame_radio = tk.Frame(root)
frame_radio.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Variable para los radio buttons
radio_var = tk.IntVar()

# Crear 3 radio buttons
for i in range(1, 4):
    radio_btn = tk.Radiobutton(frame_radio, text=f"Opción {i}", variable=radio_var, value=i)
    radio_btn.pack(anchor=tk.W)

# Crear un combo box
combo_label = tk.Label(frame_radio, text="Seleccionar opción:")
combo_label.pack(anchor=tk.W, pady=(10, 0))

combo_box = ttk.Combobox(frame_radio, values=["Opción 1", "Opción 2", "Opción 3"])
combo_box.pack(anchor=tk.W, pady=5)

# Crear un cuadro de texto
text_label = tk.Label(frame_radio, text="Cuadro de texto:")
text_label.pack(anchor=tk.W, pady=(10, 0))

text_box = tk.Text(frame_radio, height=10, width=30)
text_box.pack(anchor=tk.W, pady=5)

# Crear un frame para el gráfico con scrollbar
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

# Crear un canvas para el gráfico y el scrollbar
canvas_frame = tk.Frame(frame_plot)
canvas_frame.pack(fill=tk.BOTH, expand=True)

# Crear un scrollbar horizontal
scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Crear un frame para el gráfico
plot_frame = tk.Frame(canvas_frame)
plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear un gráfico usando Matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# Generar datos de ejemplo para el gráfico
x = np.linspace(0, 10*np.pi, 1000)
y = np.sin(x)

# Inicializar el gráfico con una ventana de visualización
window_size = 100
zoom_factor = 1
start, end = 0, window_size

# Función para actualizar los límites del gráfico
def update_plot(start, end):
    ax.clear()
    ax.plot(x, y)
    ax.set_xlim(x[start], x[end])
    ax.set_ylim(-1, 1)
    ax.set_title("Gráfico de ejemplo")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    canvas.draw()
    update_scrollbar(start, end)

# Función para actualizar la posición del scrollbar
def update_scrollbar(start, end):
    total_points = len(x)
    view_fraction = (end - start) / total_points
    start_fraction = start / total_points
    scrollbar.set(start_fraction, start_fraction + view_fraction)

# Añadir el gráfico a la interfaz Tkinter
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Función de scroll
def on_scroll(*args):
    global start, end
    move_to = int(float(args[1]) * (len(x) - window_size // zoom_factor))
    start = move_to
    end = start + window_size // zoom_factor
    update_plot(start, end)

# Configurar el scrollbar
scrollbar.config(command=on_scroll)

# Función de zoom in
def zoom_in():
    global window_size, zoom_factor, start, end
    zoom_factor *= 2
    end = start + window_size // zoom_factor
    if end > len(x):
        end = len(x)
        start = end - window_size // zoom_factor
    update_plot(start, end)

# Función de zoom out
def zoom_out():
    global window_size, zoom_factor, start, end
    zoom_factor = max(1, zoom_factor // 2)
    end = start + window_size // zoom_factor
    if end > len(x):
        end = len(x)
        start = end - window_size // zoom_factor
    if start < 0:
        start = 0
        end = start + window_size // zoom_factor
    update_plot(start, end)

# Función para detectar cambios en el tamaño del scrollbar y ajustar el zoom
def on_scroll_zoom(*args):
    if args[0] == 'moveto':
        # Movimiento del scrollbar
        on_scroll(*args)
    elif args[0] == 'scroll':
        # Zoom del scrollbar
        zoom_level = float(args[1])
        if zoom_level > 0:
            zoom_in()
        else:
            zoom_out()

# Configurar el scrollbar para usar la función de detección de cambios
scrollbar.config(command=on_scroll_zoom)

# Inicializar el gráfico
update_plot(start, end)

# Iniciar el bucle principal de la interfaz
root.mainloop()
