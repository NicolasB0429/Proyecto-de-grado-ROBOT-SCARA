import numpy as np
import tensorflow as tf
import joblib
from roboticstoolbox import RevoluteDH, SerialLink
import matplotlib.pyplot as plt
import math
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#print(sklearn.__version__)


def CI_red(px, py):
    # Cargar el modelo
    #model = tf.keras.models.load_model('model_epoch_200_neurons_90_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
    #model = tf.keras.models.load_model('model_epoch_250_neurons_90_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
    model = tf.keras.models.load_model('pruebas\Red_Neuronal\modelos\model_epoch_100_neurons_100_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
    #model = tf.keras.models.load_model('model_epoch_100_neurons_100_batchsize_264.keras')
   
    # Cargar los scalers guardados
    scaler_x = joblib.load('pruebas\Red_Neuronal\modelos\scaler_x.pkl')
    scaler_y = joblib.load('pruebas\Red_Neuronal\modelos\scaler_y.pkl')

    # Crear un array con los valores px y py que se pasan a la función
    data = np.array([[px, py]])

    # Normalizar los datos de entrada
    data_normalized = scaler_x.transform(data)

    # Realizar la predicción con el modelo
    prediction = model.predict(data_normalized)

    # Desnormalizar la predicción para obtener los ángulos en su escala original
    prediction_denormalized = scaler_y.inverse_transform(prediction)

    # Extraer theta1 y theta2 de la predicción desnormalizada
    theta1_pred, theta2_pred = prediction_denormalized[0][0], prediction_denormalized[0][1]

    # Ajustar theta1 si es necesario
    theta1_pred = theta1_pred + 2 * np.pi if theta1_pred <= -np.pi else theta1_pred

    theta1 = math.radians(theta1_pred)
    theta2 = math.radians(theta2_pred)

    theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1

    return theta1, theta2

def CI(px, py):
    l1 = 10
    l2 = 10
    b = np.sqrt(px**2 + py**2)
    cos_theta2 = (b**2 - l2**2 - l1**2) / (2 * l2 * l1)
    sen_theta2 = np.sqrt(1 - cos_theta2**2)
    theta2 = np.arctan2(sen_theta2, cos_theta2)

    alpha = np.arctan2(py, px)
    phi = np.arctan2(l2 * sen_theta2, l1 + l2 * cos_theta2)

    theta1 = alpha - phi
    theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1

    return theta1, theta2

def CD(theta1, theta2):
    l1 = 10
    l2 = 10 
    q = np.array([theta1, theta2])

    robot = SerialLink([
        RevoluteDH(d=0, alpha=0, a=l1, offset=0),
        RevoluteDH(d=0, alpha=0, a=l2, offset=0)
    ])   
    # Visualizar el robot, con sus limites 
    #robot.plot(q, limits=[-25, 25, -25, 25, 0, 5])
    
    MTH = robot.fkine(q)
    return MTH

# Parámetros Iniciales  
pxi = 20
pyi = 0
# Parámetros Finales 
pxf = -20
pyf = 0

#Cantidad de puntos 
a = 20
# Red Neuronal
theta1_P1_red, theta2_P1_red = CI_red(pxi,pyi)
theta1_P2_red, theta2_P2_red = CI_red(pxf,pyf)
theta1P1_P2_red = np.linspace(theta1_P1_red, theta1_P2_red, a)
theta2P1_P2_red = np.linspace(theta2_P1_red, theta2_P2_red, a)

# Cinematica Inversa
theta1_P1_ci, theta2_P1_ci = CI(pxi,pyi)
theta1_P2_ci, theta2_P2_ci = CI(pxf,pyf)
theta1P1_P2_ci = np.linspace(theta1_P1_ci, theta1_P2_ci, a)
theta2P1_P2_ci = np.linspace(theta2_P1_ci, theta2_P2_ci, a)

# Calcular el error absoluto entre los ángulos
error_theta1 = np.abs(theta1P1_P2_red - theta1P1_P2_ci)
error_theta2 = np.abs(theta2P1_P2_red - theta2P1_P2_ci)

# Datos para la tabla de comparación
data = {
    'Px': np.round(np.linspace(pxi, pxf, a),2),
    'Py': np.round(np.linspace(pyi, pyf, a),2),
    'Theta1_red': np.round(np.degrees(theta1P1_P2_red),2),
    'Theta2_red': np.round(np.degrees(theta2P1_P2_red),2),
    'Theta1_ci': np.round(np.degrees(theta1P1_P2_ci),2),
    'Theta2_ci': np.round(np.degrees(theta2P1_P2_ci),2),
    'Error_Theta1': np.round(np.degrees(error_theta1),2),
    'Error_Theta2': np.round(np.degrees(error_theta2),2)
}

# Crear el DataFrame
df = pd.DataFrame(data)

# Imprimir la tabla de comparación con los errores
print(df)

# Plotear los resultados de la red neuronal y la cinemática inversa
for i in range(len(theta1P1_P2_red)):
    # Resultados de la red neuronal
    MTH_red = CD(theta1P1_P2_red[i], theta2P1_P2_red[i])
    #plt.figure('Trayectoria del Robot Red Neuronal')
    #plt.title('Trayectoria del Robot Red Neuronal')
    plt.figure('Trayectoria del Robot')
    plt.plot(MTH_red.t[0], MTH_red.t[1], 'r*', label='CI_red' if i == 0 else "")

    # Resultados de la cinemática inversa
    MTH_ci = CD(theta1P1_P2_ci[i], theta2P1_P2_ci[i])
    #plt.figure('Trayectoria del Robot Cinematica Inversa')
    #plt.title('Trayectoria del Robot Cinematica Inversa')
    plt.figure('Trayectoria del Robot')
    plt.plot(MTH_ci.t[0], MTH_ci.t[1], 'b*', label='CI' if i == 0 else "")

plt.grid(True)
plt.show(block=True)
