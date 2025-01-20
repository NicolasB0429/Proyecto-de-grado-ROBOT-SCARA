#Importar librerias
import tensorflow as tf
import numpy as np
import pandas as pd
from scipy.io import loadmat
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import math
import os
import pickle
import json
import random
import sklearn

#Variables Angulos (Tethas)
# Cargar el archivo .mat de los angulos (thetas_i_t.mat)
thetas_i_t = loadmat('thetas_i_t.mat')
#Re asignar la variable
datos = thetas_i_t['thetas_i_t']
# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(datos)
# Transponer el DataFrame para intercambiar filas y columnas
df_tethas = df.transpose()
# Renombrar las columnas
df_tethas.columns = ['theta1', 'theta2']
# Mostrar el DataFrame transpuesto con los nuevos nombres de columnas
print(df_tethas.head())  # head Muestra las primeras filas de la tabla

#Variables Coordenadas (XY)
#Cargar archivos .mat de las coordenadas (xy.mat)
xy = loadmat('xy.mat')
xy = xy['xy']
# Convertir los datos de xy a un DataFrame de pandas para coordenadas
df_xy = pd.DataFrame(xy, columns=['x', 'y'])
print(df_xy.head()) 


# Combinar ambos DataFrames
df_todo = pd.concat([df_tethas, df_xy], axis=1)
print(df_todo.head())

# Normalización de los datos ----------------------------------------
scaler_x = StandardScaler()
scaler_y = StandardScaler()

x = df_todo[['x', 'y']].values
y = df_todo[['theta1', 'theta2']].values

# Normalizar datos de entrada
x_scaled = scaler_x.fit_transform(x) # Normalizar etiquetas
y_scaled = scaler_y.fit_transform(y)

# Dividir los datos en conjuntos de entrenamiento, validación y prueba
#X_train e y_train: Son los conjuntos de entrenamiento.
#X_val e y_val: Son los conjuntos de validación.
#X_test e y_test: Son los conjuntos de prueba.

x_train, x_temp, y_train, y_temp = train_test_split(x_scaled, y_scaled, test_size=0.3, random_state=42)
x_val, x_test, y_val, y_test = train_test_split(x_temp, y_temp, test_size=0.3, random_state=42)

# Imprimir los valores de los conjuntos de entrenamiento, validación y prueba
print("Conjunto de entrenamiento:", x_train.shape, y_train.shape)
print("Conjunto de validación:", x_val.shape, y_val.shape)
print("Conjunto de prueba:", x_test.shape, y_test.shape)


import joblib
# Guardar los scalers para usarlos posteriomente para el desarrollo de la red neuronal
# Esto permite que los scalers puedan ser reutilizados posteriormente sin necesidad de volver a ajustarlos.
joblib.dump(scaler_x, 'scaler_x.pkl')
joblib.dump(scaler_y, 'scaler_y.pkl')

# Definir el modelo ----------------------------

neuronas = 250

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(2,)),  # Input layer con dos entradas: x - y
    tf.keras.layers.Dense(neuronas, activation='sigmoid'),  # Capa oculta con # neuronas y función de activación sigmoide
    tf.keras.layers.Dense(neuronas, activation='sigmoid'),  # Nueva capa oculta adicional (Se puede variar el # de neuronas y funcion de activacion)
    tf.keras.layers.Dense(2)  # 2 neuronas de salida: theta 1 y theta 2
])

# Configura el modelo para entrenamiento: 
# utiliza el optimizador Adam (eficiente y adaptable) 
# optimiza la función de pérdida de error cuadrático medio (MSE) 
# y monitorea el error absoluto medio (MAE) como métrica adicional.
model.compile(optimizer='adam', loss='mse', metrics=['mae']) # Compilar el modelo


# ENTRENAMIENTO DEL MODELO -------------------

# Define las variables antes de usarlas
neuronas = 250  # neuronas
batch_size = 264  # tamaño lote
epochs = 100

# 1. Creacion de carpetas para guardar los archivos
# Crear el directorio de guardado si no existe
save_dir = f'Modelo_{neuronas}n_{batch_size}bz_{epochs}e'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print(f"Directorio {save_dir} creado.")

# 2. Configuración de Frecuencia de Guardado:
# Calcular `save_freq`
num_examples = x_train.shape[0]  # Se obtiene el número total de datos en el de entrenamiento (x_train).
batches_per_epoch = math.ceil(num_examples / batch_size)  # Se calcula el # lotes que se procesarán en cada época.Se utiliza math.ceil para redondear
save_freq = 50 * batches_per_epoch  # Guardar cada cantidad de iteraciones, en este caso cada 50 interaciones guarda el modelo

print(f"Neuronas: {neuronas}")
print(f"Batches por época: {batches_per_epoch}")
print(f"Frecuencia de guardado: {save_freq} batches")

# 3. Definición de Callbacks Personalizados
# Definir un callback personalizado para agregar registros
class CustomModelCheckpoint(tf.keras.callbacks.ModelCheckpoint):  # Clase CustomModelCheckpoint que hereda de tf.keras.callbacks.ModelCheckpoint
    def on_epoch_end(self, epoch, logs=None):
        super().on_epoch_end(epoch, logs)  # método on_epoch_end de la clase base tf.keras.callbacks.ModelCheckpoint, guarda el modelo al final de cada época.
        print(f"Modelo guardado en la época {epoch + 1}")

# 4. Configuración de Callbacks
# Callbacks
callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        filepath=os.path.join(save_dir, f'model_epoch_{{epoch:02d}}_neurons_{neuronas}_batchsize_{batch_size}.keras'), #Nombre con el que se guarda el modelo
        save_freq=save_freq,
        save_weights_only=False, #Indica si se deben guardar solo los pesos del modelo (True) o el modelo completo (False).
        save_best_only=False, #Guarda el modelo solo si hay una mejora en la métrica monitoreada (True), o siempre en cada punto de guardado (False)
        monitor='val_loss'
    ),
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10),#Número de épocas sin mejorar el valor de perdiada tras las cuales se detiene el entrenamiento.
]

# 5.  Inicio y Monitoreo del Entrenamiento:
print("Comenzando el entrenamiento...")
# Entrena el modelo con los datos de entrenamiento (x_train, y_train):
# - epochs: número total de épocas de entrenamiento.
# - initial_epoch: época inicial desde la que se empieza el entrenamiento.
# - validation_data: datos de validación (x_val, y_val) para evaluar el modelo en cada época.
# - batch_size: tamaño del lote para procesar los datos en cada iteración.
# - verbose: nivel de detalle en la salida (1 = barra de progreso detallada).
# - callbacks: funciones adicionales que se ejecutan durante el entrenamiento (como guardado del modelo o ajuste de tasa de aprendizaje).
# El historial del entrenamiento se guarda en la variable 'history'.
history = model.fit(x_train, y_train, epochs=epochs, initial_epoch=0, validation_data=(x_val, y_val), batch_size=batch_size, verbose=1, callbacks=callbacks)
print("¡Modelo entrenado!")

# 6. Guardado del Historial de Entrenamiento
history_filename = f'training_history_neurons_{neuronas}_epochs_{epochs}_batchsize_{batch_size}.json'
with open(history_filename, 'w') as f:  # Crea un archivo json para guardar el historial del entrenamiento
    json.dump(history.history, f)

# 7. Verificación de Resultados
# Verificar archivos guardados
saved_models = os.listdir('.')
print(f"Modelos guardados: {saved_models}")

# Verificar historial guardado
if os.path.exists(history_filename):  # Verifica si el archivo de entrenamiento existe
    print(f"Historial de entrenamiento guardado como {history_filename}.")
else:
    print("No se pudo guardar el historial de entrenamiento.")


# Después del entrenamiento, se guarda el modelo en un archivo con formato .h5, 
# que es más fácil de procesar para la Raspberry Pi y compatible con TensorFlow.
model.save('model_epoch_63_neurons_200_batchsize_264.h5')

#---------------------------------------------------------------
# Evaluación y visualización del desempeño del modelo

# Evaluación del modelo con los datos de prueba
# Se calcula la pérdida (loss) y el error absoluto medio (MAE) usando los datos de prueba (x_test, y_test).
loss, mae = model.evaluate(x_test, y_test)
print(f'MAE: {mae}')  # MAE = Mean Absolute Error, mide el error promedio absoluto entre predicciones y valores reales.

# 2. Obtención de métricas finales del historial
# Extraemos los valores finales de las métricas de pérdida y MAE, tanto para el entrenamiento como para la validación.
final_loss = history.history["loss"][-1]  # Última pérdida de entrenamiento
final_val_loss = history.history["val_loss"][-1]  # Última pérdida de validación
final_mae = history.history["mae"][-1]  # Último MAE de entrenamiento
final_val_mae = history.history["val_mae"][-1]  # Último MAE de validación

# 3. Visualización de las métricas: Pérdida y MAE a lo largo de las épocas
plt.figure(figsize=(14, 5))

# Gráfica de Pérdida:
plt.subplot(1, 2, 1)
plt.xlabel("Época")  # Número de iteraciones completas sobre el conjunto de datos
plt.ylabel("Pérdida (Loss)")  # Muestra la magnitud del error durante el entrenamiento
plt.plot(history.history["loss"], label=f'Pérdida de Entrenamiento (final: {final_loss:.7f})')
plt.plot(history.history["val_loss"], label=f'Pérdida de Validación (final: {final_val_loss:.7f})')
plt.legend()
plt.grid(True)
plt.title('Pérdida sobre Épocas')  # Visualización del progreso de la pérdida

# Gráfica de MAE:
plt.subplot(1, 2, 2)
plt.xlabel("Época")
plt.ylabel("MAE (Error Absoluto Medio)")  # Muestra el error promedio absoluto por época
plt.plot(history.history["mae"], label=f'MAE de Entrenamiento (final: {final_mae:.7f})')
plt.plot(history.history["val_mae"], label=f'MAE de Validación (final: {final_val_mae:.7f})')
plt.legend()
plt.grid(True)
plt.title('MAE sobre Épocas')  # Visualización del progreso del MAE

# Mostrar las gráficas
plt.show()
