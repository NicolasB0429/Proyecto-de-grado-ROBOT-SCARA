#muestra los contornos dando enter
import cv2
import numpy as np
import matplotlib.pyplot as plt
#Leer la imagen en formato cv2
imagen = cv2.imread('pruebas/Camara/img/captura.jpg')

# Definir el nuevo ancho deseado
nuevo_ancho = 1200  # El ancho que quieras ajustar
# Calcular la altura proporcional manteniendo la relación de aspecto
relacion_aspecto = imagen.shape[1] / imagen.shape[0]
nuevo_alto = int(nuevo_ancho / relacion_aspecto)
# Redimensionar la imagen manteniendo la proporción
resized_img = cv2.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)

# Convertir la imagen a escala de grises
img_gris = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

# Invertir la imagen binaria (Para que no exista primer contorno)
imagen_invertida = cv2.bitwise_not(img_gris)

#Ajuste colores (umbral >=)
_, imagen_bn = cv2.threshold(imagen_invertida, 100, 255, cv2.THRESH_BINARY)

# Aplicar suavizado Gaussiano
imagen_suavizada = cv2.GaussianBlur(imagen_bn, (5,5), 0) #Si influye un poco

# Encontrar los contornos en la imagen (imagen, metodo, para que se almacenen todos los puntos)
contornos, _ = cv2.findContours(imagen_suavizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(len(contornos)) #Corroborar numero de contornos

# Crear figura y activar modo interactivo
fig, ax = plt.subplots()
plt.ion()  # Modo interactivo activado
contorno_index = 0  # �ndice del contorno actual

# Mostrar la imagen redimensionada
ax.imshow(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))

# Funci�n para graficar un contorno
def graficar_contorno(contorno):
    contorno = np.squeeze(contorno)  # Quitar dimensiones extra si es necesario
    ax.plot(contorno[:, 0], contorno[:, 1], '*b', markersize=1)  # Graficar puntos x e y de cada contorno
    ax.grid(True)
    plt.draw()  # Actualizar la figura

# Funci�n que maneja el evento de tecla presionada
def on_key_press(event):
    global contorno_index
    if event.key == 'enter' or event.key == 'm':  # Tecla Enter o "m"
        if contorno_index < len(contornos):
            graficar_contorno(contornos[contorno_index])
            contorno_index += 1
        else:
            print("No hay mas contornos para graficar")

# Conectar el evento de teclado
fig.canvas.mpl_connect('key_press_event', on_key_press)

# Mostrar la figura con la imagen y esperar los eventos del teclado
plt.show(block=True)

# # Graficar los contornos utilizando matplotlib
# plt.imshow(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))  # Mostrar la imagen redimensionada

# # Graficar los contornos sobre la imagen
# for contorno in contornos:
#     contorno = np.squeeze(contorno)  # Quitar dimensiones extra si es necesario
#     plt.plot(contorno[:, 0], contorno[:, 1], '*b', markersize=1)  # Graficar puntos x e y de cada contorno

# plt.grid(True)
# plt.show()



