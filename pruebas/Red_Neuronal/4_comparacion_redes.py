import cv2
import numpy as np
import math
import joblib
import tensorflow as tf
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import io
import sys
sys.stdout.reconfigure(encoding='utf-8')
import roboticstoolbox as rtb
from roboticstoolbox import RevoluteDH, PrismaticDH, SerialLink
import matplotlib.colors as mcolors


class RobotSimulation:
    def __init__(self):
        self.pxInicial = 20
        self.pyInicial = 0
        self.pzInicial = 0
        self.arriba_cor = 10
        self.abajo = 0
        self.Robot_Scara = self.initialize_robot_model()

    def initialize_robot_model(self):
        Robot_Scara = SerialLink([
            RevoluteDH(d=0, alpha=0, a=10, offset=0),
            RevoluteDH(d=0, alpha=0, a=10, offset=0),
            PrismaticDH(theta=0, a=0, alpha=np.pi, offset=0)
        ])
        return Robot_Scara

    def esp_trabajo(self):
        # Cantidad de linspace y de iteraciones en los for
        can_puntos = 20
        theta_cre = 0

        theta1P1_P2 = 0
        theta2P1_P2 = np.linspace((5/6)*np.pi, 0, can_puntos)
        pasos = []
        
        # Para graficar el espacio de trabajo
        x_vals, y_vals = [], []  # Para almacenar las coordenadas del área de trabajo

        for i in range(can_puntos):
            MTH = self.CD(theta1P1_P2, theta2P1_P2[i], theta_cre, graficar=1)
            x_vals.append(MTH.t[0])
            y_vals.append(MTH.t[1])

        theta1P2_P3 = np.linspace(0, np.pi/2, can_puntos)
        theta2P2_P3 = 0
        for i in range(can_puntos):
            MTH = self.CD(theta1P2_P3[i], theta2P2_P3, theta_cre, graficar=1)
            x_vals.append(MTH.t[0])
            y_vals.append(MTH.t[1])

        theta1P3_P4 = np.linspace(np.pi/2, np.pi, can_puntos)
        theta2P3_P4 = 0
        for i in range(can_puntos):
            MTH = self.CD(theta1P3_P4[i], theta2P3_P4, theta_cre, graficar=1)
            x_vals.append(MTH.t[0])
            y_vals.append(MTH.t[1])

        theta1P4_P5 = np.pi
        theta2P4_P5 = np.linspace(0, (5/6)*np.pi, can_puntos)
        for i in range(can_puntos):
            MTH = self.CD(theta1P4_P5, theta2P4_P5[i], theta_cre, graficar=1)
            x_vals.append(MTH.t[0])
            y_vals.append(MTH.t[1])
        
        return x_vals, y_vals

    # Agregar el gráfico con las coordenadas (x, y) de la imagen
    def imagen_camara2(self):
        
        imagen = cv2.imread('pruebas\Red_Neuronal\modelos\img\imagen.jpg')
        nuevo_ancho = 1000
        relacion_aspecto = imagen.shape[1] / imagen.shape[0]
        nuevo_alto = int(nuevo_ancho / relacion_aspecto)
        resized_img = cv2.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)
        img_gris = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        imagen_invertida = cv2.bitwise_not(img_gris)
        _, imagen_bn = cv2.threshold(imagen_invertida, 140, 255, cv2.THRESH_BINARY)
        imagen_suavizada = cv2.GaussianBlur(imagen_bn, (5, 5), 0)
        contornos, _ = cv2.findContours(imagen_suavizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        contornos_escalados = []
        for contorno in contornos:
            contorno_escalado = np.array([[(punto[0][0] / 100) - 17, ((punto[0][1] * -1 + 950) / 100) - 3] for punto in contorno])
            contorno_escalado = np.vstack([contorno_escalado[0::5], contorno_escalado[-1]])
            contornos_escalados.append(contorno_escalado)
            

        # Lista para almacenar los valores de los ángulos
        puntos = []  # Almacenar coordenadas (x, y)
        theta1_CI, theta2_CI = [], []
        theta1_M1, theta2_M1 = [], []
        theta1_M2, theta2_M2 = [], []
        theta1_M3, theta2_M3 = [], []

        # Procesar cada contorno
        if contornos_escalados:
            for contorno in contornos_escalados:
                for punto in contorno:
                    Px, Py = punto[0], punto[1]
                    puntos.append((Px, Py))  # Almacenar el punto

                    # CI Tradicional
                    theta1_ci, theta2_ci, _ = self.CI(Px, Py, self.abajo)
                    theta1_CI.append(np.degrees(theta1_ci))  # Convertir a grados
                    theta2_CI.append(np.degrees(theta2_ci))  # Convertir a grados

                    # CI Red Neuronal - Modelo 1
                    t1_m1, t2_m1, _ = self.CI_Modelo_1(Px, Py, self.abajo)
                    theta1_M1.append(np.degrees(t1_m1))  # Convertir a grados y añadir a la lista
                    theta2_M1.append(np.degrees(t2_m1))  # Convertir a grados y añadir a la lista
                    
                    # CI Red Neuronal - Modelo 2
                    t1_m2, t2_m2, _ = self.CI_Modelo_2(Px, Py, self.abajo)
                    theta1_M2.append(np.degrees(t1_m2))  # Convertir a grados y añadir a la lista
                    theta2_M2.append(np.degrees(t2_m2))  # Convertir a grados y añadir a la lista
                    
                    # CI Red Neuronal - Modelo 3
                    t1_m3, t2_m3, _ = self.CI_Modelo_3(Px, Py, self.abajo)
                    theta1_M3.append(np.degrees(t1_m3))  # Convertir a grados y añadir a la lista
                    theta2_M3.append(np.degrees(t2_m3))  # Convertir a grados y añadir a la lista

                    # Graficar las trayectorias (si es necesario)
                    MTH = self.CD(theta1_ci, theta2_ci, self.abajo, graficar=1)
                    MTH_M1 = self.CD(t1_m1, t2_m1, self.abajo, graficar=1)
                    MTH_M2 = self.CD(t1_m2, t2_m2, self.abajo, graficar=1)
                    MTH_M3 = self.CD(t1_m3, t2_m3, self.abajo, graficar=1)

                    # # Imprimir cada ángulo       
                    # print(f"Coordenadas (Px, Py): ({Px:.2f}, {Py:.2f})")
                    # print(f" - CI Tradicional: Theta1 = {theta1_ci_vals[-1]:.4f} °, Theta2 = {theta2_ci_vals[-1]:.4f} °")
                    # print(f" - CI Red Neuronal: Theta1 = {theta1_red_vals[-1]:.4f} °, Theta2 = {theta2_red_vals[-1]:.4f} °\n")

    
      
        intervalo_marcador = 10  # For example, plot a marker every 10 data points

        fig1, ax1 = plt.subplots(figsize=(12, 6))

        # Graficar los ángulos para CI tradicional y Red Neuronal
        
        #Aumentando el tamaño de los símbolos y espaciando los puntos
        ax1.plot(theta1_CI, label="Theta1 CI", marker='o', color='blue', markersize=6, markevery=30)
        ax1.plot(theta2_CI, label="Theta2 CI", marker='o', color='blue', markersize=6, markevery=30)
        ax1.plot(theta1_M1, label="Theta1 Modelo 1", marker='d', color='orange', markersize=6, markevery=30)
        ax1.plot(theta2_M1, label="Theta2 Modelo 1", marker='d', color='orange', markersize=6, markevery=30)
        ax1.plot(theta1_M3, label="Theta1 Modelo 2", marker='s', color='red', markersize=6, markevery=30)
        ax1.plot(theta2_M3, label="Theta2 Modelo 2", marker='s', color='red', markersize=6, markevery=30)
        ax1.plot(theta1_M2, label="Theta1 Modelo 3", marker='v', color='green', markersize=6, markevery=30)
        ax1.plot(theta2_M2, label="Theta2 Modelo 3", marker='v', color='green', markersize=6, markevery=30)


        # # ax1.plot(etiquetas_puntos, theta2_M3, label="Theta2 Modelo 3", marker='<', markersize=1, linestyle='--', color='orange')
        
        plt.rc('legend', fontsize=30)
        ax1.set_xlabel("Puntos de referencia", fontsize=16)  # Etiqueta del eje X
        ax1.set_ylabel("Ángulo (°)", fontsize=16)  # Etiqueta del eje Y
        #.set_title("Comparación de Ángulos entre Cinemática Inversa y Modelos de Red Neuronal", fontsize=16)  # Título
        ax1.legend(fontsize=16)  # 

        # # Rotar las etiquetas del eje X para mejor visualización
        # ax1.set_xticks([i for i in range(0, len(etiquetas_puntos), max(1, len(etiquetas_puntos)//10))])  # Mostrar cada 10 puntos
        # ax1.set_xticklabels(etiquetas_puntos[::max(1, len(etiquetas_puntos)//10)], rotation=45, ha="right")
        
        # Cambiar el fondo del gráfico a blanco
        fig1.patch.set_facecolor('white')
        ax1.set_facecolor('white')

        plt.tight_layout()
        plt.show()

        print(f"Error absoluto medio M1")
        self.calcular_error(theta1_CI, theta2_CI, theta1_M1, theta2_M1)
        print(f"Error absoluto medio M2")
        self.calcular_error(theta1_CI, theta2_CI, theta1_M2, theta2_M2)
        print(f"Error absoluto medio M3")
        self.calcular_error(theta1_CI, theta2_CI, theta1_M3, theta2_M3)
        print(f"RMSE M1")
        self.calcular_rmse(theta1_CI, theta2_CI, theta1_M1, theta2_M1)
        print(f"RMSE M2")
        self.calcular_rmse(theta1_CI, theta2_CI, theta1_M2, theta2_M2)
        print(f"RMSE M3")
        self.calcular_rmse(theta1_CI, theta2_CI, theta1_M3, theta2_M3)
       
    def imagen_camara1(self):
        imagen = cv2.imread('pruebas\Red_Neuronal\modelos\img\imagen.jpg')
        nuevo_ancho = 1200
        relacion_aspecto = imagen.shape[1] / imagen.shape[0]
        nuevo_alto = int(nuevo_ancho / relacion_aspecto)
        resized_img = cv2.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)
        img_gris = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        imagen_invertida = cv2.bitwise_not(img_gris)
        _, imagen_bn = cv2.threshold(imagen_invertida, 140, 255, cv2.THRESH_BINARY)
        imagen_suavizada = cv2.GaussianBlur(imagen_bn, (5, 5), 0)
        contornos, _ = cv2.findContours(imagen_suavizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        contornos_escalados = []
        modelos = [self.CI, self.CI_Modelo_1, self.CI_Modelo_3, self.CI_Modelo_2]
        colores = ['b', 'orange', 'r', 'g']
        etiquetas = ["Cinematica Inversa Geometrica", "Modelo 1", "Modelo 2", "Modelo 3"]

        total_puntos = 0  # Contador de puntos

        for contorno in contornos:
            contorno_escalado = np.array([[(punto[0][0] / 100) - 17, ((punto[0][1] * -1 + 950) / 100) - 3] for punto in contorno])
            contorno_escalado = np.vstack([contorno_escalado[0::5], contorno_escalado[-1]])
            contornos_escalados.append(contorno_escalado)
            total_puntos += len(contorno_escalado)  # Sumar los puntos procesados

        if contornos_escalados:
            for n_contorno in contornos_escalados:
                for punto in n_contorno:
                    Px, Py = punto[0], punto[1]

                    for modelo, color, etiqueta in zip(modelos, colores, etiquetas):
                        theta1_red, theta2_red, _ = modelo(Px, Py, self.abajo)
                        MTH_red = self.CD(theta1_red, theta2_red, self.pzInicial, graficar=1)
                        # plt.plot(MTH_red.t[0], MTH_red.t[1], f'{color}o', markersize=2)
                        plt.plot(MTH_red.t[0], MTH_red.t[1], 'o', color=color, markersize=2)

                    theta1, theta2, theta3 = self.CI(Px, Py, self.abajo)
                    MTH = self.CD(theta1, theta2, theta3, graficar=1)
                    plt.plot(MTH.t[0], MTH.t[1], 'b', markersize=1)

        # Mostrar el total de puntos procesados
        print(f"Cantidad total de puntos procesados: {total_puntos}")

         # Agregar etiquetas y mostrar la gráfica
        plt.xlim(-17, -5)  # Establece el rango del eje x de -20 a 20
        plt.ylim(-3, 7)
        plt.rc('legend', fontsize=15)
        plt.xlabel("X (cm)", fontsize=14)
        plt.ylabel("Y (cm)", fontsize=14)
        plt.tick_params(axis='both', which='major', labelsize=12) 
        plt.legend(labels=etiquetas)

        # Corrected line for background color
        # plt.gcf().set_facecolor('white')  # Set the background color of the figure
        # Set the background color of the figure and axes to white
        plt.gcf().set_facecolor('white')  # Set the background color of the figure
        plt.gca().set_facecolor('white')  # Set the background color of the axes
        plt.tight_layout()
        plt.show()
  
    def calcular_error(self, theta1_traj, theta2_traj, theta1_traj_red, theta2_traj_red):
        error_theta1 = np.abs(np.array(theta1_traj) - np.array(theta1_traj_red))
        error_theta2 = np.abs(np.array(theta2_traj) - np.array(theta2_traj_red))

        error_theta1_medio = np.mean(error_theta1)
        error_theta2_medio = np.mean(error_theta2)

        print(f"Error absoluto medio para θ1: {error_theta1_medio:.4f} °")
        print(f"Error absoluto medio para θ2: {error_theta2_medio:.4f} °")
        
    def calcular_rmse(self, theta1_traj, theta2_traj, theta1_traj_red, theta2_traj_red):
        # Calcula el error cuadrático para cada ángulo
        error_theta1 = np.square(np.array(theta1_traj) - np.array(theta1_traj_red))
        error_theta2 = np.square(np.array(theta2_traj) - np.array(theta2_traj_red))
        
        # Calcula el RMSE tomando la raíz cuadrada del promedio del error cuadrático
        rmse_theta1 = np.sqrt(np.mean(error_theta1))
        rmse_theta2 = np.sqrt(np.mean(error_theta2))
        
        print(f"RMSE para θ1: {rmse_theta1:.4f} °")
        print(f"RMSE para θ2: {rmse_theta2:.4f} °")

    def CD(self, theta1, theta2, theta_cre, graficar):
        
        theta_cre = math.degrees(theta_cre)
        d3 = theta_cre / 50
        q = np.array([theta1, theta2, d3])
        MTH = self.Robot_Scara.fkine(q)
        
        if graficar == 1:
            links = self.Robot_Scara.links
            p1 = [0, 0]
            p2 = [links[0].a * np.cos(q[0]), links[0].a * np.sin(q[0])]
            p3 = [p2[0] + links[1].a * np.cos(q[0] + q[1]), p2[1] + links[1].a * np.sin(q[0] + q[1])]
            #plt.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='blue', marker='o')

        return MTH
    
    def CI(self,px,py,pz):
        h1 = 5
        l3 = 5
        l1 = 10
        l2 = 10
        # Theta2
        b = np.sqrt(px**2 + py**2)
        cos_theta2 = (b**2-l2**2-l1**2)/(2*l2*l1)
        sen_theta2 = np.sqrt(1 - cos_theta2**2)
        theta2 = np.arctan2(sen_theta2, cos_theta2)
        #print(f'Theta2 = {np.degrees(theta2):.3f} grados')
       
        # Theta1
        alpha = np.arctan2(py,px)
        phi = np.arctan2(l2 * sen_theta2, l1 + l2 * cos_theta2)
        # Calcular theta1
        theta1 = alpha - phi
        theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1 #Otra forma de hacer el if
        #print(f'Theta1 = {np.degrees(theta1):.3f} grados')
       
        # d3
        d3 = -1 * (h1 - l3 - pz)
        theta_cre = d3 * 50
        #print(f'Theta3 = {theta_cre:.3f} grados')
        theta_cre = math.radians(theta_cre)
        
        print(f'Theta1 = {theta1:.3f} grados')
        print(f'Theta2 = {theta2:.3f} grados')
       
        #Retorno
        return theta1,theta2,theta_cre
        
    def CI_Modelo_1(self, px, py, pz):
        h1 = 5
        l3 = 5
        d3 = -1 * (h1 - l3 - pz)
        theta_cre = d3 * 50
        theta_cre = math.radians(theta_cre)
        
        # model = tf.keras.models.load_model('Datos_Red\modelos\model_epoch_150_neurons_90_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
        model = tf.keras.models.load_model('pruebas\Red_Neuronal\modelos\model_epoch_150_neurons_90_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})

        scaler_x = joblib.load('pruebas\Red_Neuronal\modelos\scaler_x.pkl')
        scaler_y = joblib.load('pruebas\Red_Neuronal\modelos\scaler_y.pkl')
        
        data = np.array([[px, py]])
        data_normalized = scaler_x.transform(data)
        prediction = model.predict(data_normalized)
        prediction_denormalized = scaler_y.inverse_transform(prediction)
        
        theta1_pred, theta2_pred = prediction_denormalized[0][0], prediction_denormalized[0][1]
        theta1 = math.radians(theta1_pred)
        theta2 = math.radians(theta2_pred)
        theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1
        # print(f'Theta1_red = {theta1:.3f} grados')
        # print(f'Theta2_red = {theta2:.3f} grados')
        
        # Aplicar umbral absoluto para valores pequeños cercanos a cero
        if abs(theta1) < 0.01 and abs(theta2) < 0.03:
            theta1 = 0
            theta2 = 0
            
        return theta1, theta2, theta_cre
    
    def CI_Modelo_2(self, px, py, pz):
        h1 = 5
        l3 = 5
        d3 = -1 * (h1 - l3 - pz)
        theta_cre = d3 * 50
        theta_cre = math.radians(theta_cre)
        
        model = tf.keras.models.load_model('pruebas\Red_Neuronal\modelos\model_epoch_63_neurons_200_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
        scaler_x = joblib.load('pruebas\Red_Neuronal\modelos\scaler_x.pkl')
        scaler_y = joblib.load('pruebas\Red_Neuronal\modelos\scaler_y.pkl')
        
        data = np.array([[px, py]])
        data_normalized = scaler_x.transform(data)
        prediction = model.predict(data_normalized)
        prediction_denormalized = scaler_y.inverse_transform(prediction)
        
        theta1_pred, theta2_pred = prediction_denormalized[0][0], prediction_denormalized[0][1]
        theta1 = math.radians(theta1_pred)
        theta2 = math.radians(theta2_pred)
        theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1
        # print(f'Theta1_red = {theta1:.3f} grados')
        # print(f'Theta2_red = {theta2:.3f} grados')
        
        # Aplicar umbral absoluto para valores pequeños cercanos a cero
        if abs(theta1) < 0.01 and abs(theta2) < 0.03:
            theta1 = 0
            theta2 = 0
            
        return theta1, theta2, theta_cre
    
    def CI_Modelo_3(self, px, py, pz):
        h1 = 5
        l3 = 5
        d3 = -1 * (h1 - l3 - pz)
        theta_cre = d3 * 50
        theta_cre = math.radians(theta_cre)

        # Carga los modelos
        model1 = tf.keras.models.load_model('pruebas\Red_Neuronal\modelos\model_epoch_33_neurons_210_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
        # model1 = tf.keras.models.load_model('Datos_Red\Modelo_red\Modelo_250n_264bz_80e\model_epoch_50_neurons_250_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
        # model1 = tf.keras.models.load_model('Datos_Red\Modelo_red\Modelo_250n_264bz_100e2\model_epoch_57_neurons_250_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
        model2 = tf.keras.models.load_model('pruebas\Red_Neuronal\modelos\model_epoch_80_neurons_250_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
        model3 = tf.keras.models.load_model('pruebas\Red_Neuronal\modelos\model_epoch_77_neurons_200_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
        
        # Carga los escaladores
        scaler_x = joblib.load('pruebas\Red_Neuronal\modelos\scaler_x.pkl')
        scaler_y = joblib.load('pruebas\Red_Neuronal\modelos\scaler_y.pkl')
        
        # Normaliza los datos de entrada
        data = np.array([[px, py]])
        data_normalized = scaler_x.transform(data)
        
        # Predicciones de cada modelo
        prediction1 = model1.predict(data_normalized)
        prediction2 = model2.predict(data_normalized)
        prediction3 = model3.predict(data_normalized)
        
        # Desnormaliza las predicciones
        prediction1_denormalized = scaler_y.inverse_transform(prediction1)
        prediction2_denormalized = scaler_y.inverse_transform(prediction2)
        prediction3_denormalized = scaler_y.inverse_transform(prediction3)
        
        # Calcula el promedio de los ángulos
        theta1_avg = np.mean([prediction1_denormalized[0][0], prediction2_denormalized[0][0], prediction3_denormalized[0][0]])
        theta2_avg = np.mean([prediction1_denormalized[0][1], prediction2_denormalized[0][1], prediction3_denormalized[0][1]])
        
        # Convierte los ángulos a radianes
        theta1 = math.radians(theta1_avg)
        theta2 = math.radians(theta2_avg)
        theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1

        # print(f'Theta1_red = {theta1:.3f} grados')
        # print(f'Theta2_red = {theta2:.3f} grados')
        
        # Aplicar umbral absoluto para valores pequeños cercanos a cero
        if abs(theta1) < 0.03 and abs(theta2) < 0.04:
            theta1 = 0
            theta2 = 0
            
        # print(f'Theta1_red = {theta1:.3f} grados')
        # print(f'Theta2_red = {theta2:.3f} grados')
        
        return theta1, theta2, theta_cre

    
robot_simulation = RobotSimulation()
robot_simulation.imagen_camara1() # Comparacion modelos, solo imagen apple grande
robot_simulation.imagen_camara2() # Comparacion de las coordenads vs angulos

# robot_simulation.CI(20,0,0) 
# robot_simulation.CI_Modelo_3(20,0,0)

