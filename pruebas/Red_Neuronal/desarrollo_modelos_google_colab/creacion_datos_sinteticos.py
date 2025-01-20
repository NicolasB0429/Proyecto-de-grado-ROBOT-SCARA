#Puntos_Scara_1 ----> Se sacan tethas por medio de los for, y esos se ingresan a la MTH para sacar las coordenadas

import numpy as np
from scipy.io import savemat  # Guardar archivo .mat
import math
import matplotlib.pyplot as plt

# Parámetros
l1 = 10
l2 = 10
h = 0  

# Almacenar variables (Vectores)
xy = []
thetas_i = []
cont = 0

print("Comenzando el conteo de iteraciones...")

# Barrido de ángulos
for theta1 in np.arange(0, np.pi, 0.001):  # Paso de 0.001 para obtener 10 millones de combinaciones
    for theta2 in np.arange(0, np.pi, 0.001):
        # Matriz de transformación homogénea
        MTH = np.array([
            [np.cos(theta1 + theta2), -np.sin(theta1 + theta2), 0, l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)],
            [np.sin(theta1 + theta2),  np.cos(theta1 + theta2), 0, l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)],
            [0, 0, 1, h],
            [0, 0, 0, 1]
        ])

        # Obtener coordenadas
        x = MTH[0, 3]
        y = MTH[1, 3]

        # Almacenar las coordenadas en la lista xy
        xy.append([x, y])

        # Almacenar los ángulos en grados
        theta1_g = math.degrees(theta1)
        theta2_g = math.degrees(theta2)
        thetas_i.append([theta1_g, theta2_g])

        # Para saber en que cantidad de datos va el proceso
        cont += 1
        if cont % 1_000_000 == 0:  # Notificar en cada millón de iteraciones
            print(f"Iteración: {cont / 1_000_000} millones")

print("Conteo de iteraciones completado.")

# Convertir las listas a arrays de numpy para facilitar su uso posterior
xy = np.array(xy)
thetas_i = np.array(thetas_i)

# Graficar las coordenadas
fig = plt.figure()  # Crear Figura
ax = fig.add_subplot(111)  # Configuración de un Subgrafico para 2D, 111, Significa 1 fila, 1 columna

# Separar las coordenadas x y y para graficar
x = xy[:, 0]
y = xy[:, 1]

ax.scatter(x, y, c='b', marker='*')  # Configuración de la gráfica

# Etiquetas del gráfico
ax.set_xlabel('X (cm)')
ax.set_ylabel('Y (cm)')
ax.set_title('Puntos del area de trabajo del Robot')

plt.show()  # Mostrar gráfico

# Guardar en archivos .mat separados
savemat('xy.mat', {'xy': xy})
thetas_i_t = thetas_i.T
savemat('thetas_i_t.mat', {'thetas_i_t': thetas_i_t})

print("Datos guardados en 'xy.mat' y 'thetas_i_t.mat'")
