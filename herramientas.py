import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

# Crear la ventana principal
root = tk.Tk()
root.title("Gráfico con barra de herramientas en Tkinter")
root.geometry("600x400")

# Crear un marco para contener el gráfico y la barra de herramientas
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Crear la figura de matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# Crear algunos datos de ejemplo
t = np.arange(0, 3, 0.01)
s = np.sin(2 * np.pi * t)
ax.plot(t, s)

# Crear un widget FigureCanvasTkAgg y añadirlo al marco
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Crear una barra de herramientas de navegación y añadirla al marco
toolbar = NavigationToolbar2Tk(canvas, frame)
toolbar.update()
toolbar.pack(side=tk.TOP, fill=tk.X)

# Ejemplo de función para actualizar el gráfico
def update_plot():
    ax.clear()
    new_t = np.arange(0, 3, 0.01)
    new_s = np.cos(2 * np.pi * new_t)
    ax.plot(new_t, new_s)
    canvas.draw()

# Botón para actualizar el gráfico
update_button = ttk.Button(root, text="Actualizar gráfico", command=update_plot)
update_button.pack(side=tk.BOTTOM, pady=10)

# Inicializar la ventana principal
root.mainloop()
