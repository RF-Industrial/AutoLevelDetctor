import numpy as np
import matplotlib.pyplot as plt

# Datos para el primer gráfico
x1 = np.linspace(0, 10, 100)
y1 = np.sin(x1)

# Datos para el segundo gráfico
x2 = np.linspace(0, 10, 100)
y2 = np.cos(x2)

# Crear la figura y los ejes
plt.figure()

# Dibujar el primer gráfico
plt.plot(x1, y1, label='sin(x)', color='blue')

# Dibujar el segundo gráfico en el mismo plot
plt.plot(x2, y2, label='cos(x)', color='red')

# Etiquetas de los ejes y título
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Gráfico de sin(x) y cos(x)')

# Leyenda
plt.legend()

# Mostrar el plot
plt.show()
