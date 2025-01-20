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

    def imagen_camara(self):
        
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

        plt.figure()
        x_vals, y_vals = self.esp_trabajo()
        plt.plot(x_vals, y_vals, 'g--',  markersize=3, label="Espacio de trabajo del Robot SCARA")

        if contornos_escalados:
            punto_inicial = contornos_escalados[0][0]
            px_inicial, py_inicial = self.pxInicial, self.pyInicial
            pz_inicial = self.pzInicial

            theta1_inicial, theta2_inicial, theta3_inicial = self.CI(px_inicial, py_inicial, pz_inicial)
            theta1_final, theta2_final, _ = self.CI(punto_inicial[0], punto_inicial[1], self.abajo)

            can_puntos = 10
            theta1_traj = np.linspace(theta1_inicial, theta1_final, can_puntos)
            theta2_traj = np.linspace(theta2_inicial, theta2_final, can_puntos)

            for t1, t2 in zip(theta1_traj, theta2_traj):
                MTH = self.CD(t1, t2, theta3_inicial, graficar=1)
                plt.plot(MTH.t[0], MTH.t[1], 'ro', markersize=2, label="Trayectoria CI Geometrica" if t1 == theta1_traj[0] else "")

            theta1_red, theta2_red, _ = self.CI_red(px_inicial, py_inicial, pz_inicial)
            theta1_red_final, theta2_red_final, _ = self.CI_red(punto_inicial[0], punto_inicial[1], self.abajo)

            theta1_traj_red = np.linspace(theta1_red, theta1_red_final, can_puntos)
            theta2_traj_red = np.linspace(theta2_red, theta2_red_final, can_puntos)

            for t1, t2 in zip(theta1_traj_red, theta2_traj_red):
                MTH = self.CD(t1, t2, theta3_inicial, graficar=1)
                plt.plot(MTH.t[0], MTH.t[1], 'bo', markersize=2, label="Trayectoria CI Red Neuronal" if t1 == theta1_traj_red[0] else "")

        for n_contorno in contornos_escalados:
            for punto in n_contorno:
                Px, Py = punto[0], punto[1]
                theta1, theta2, theta3 = self.CI(Px, Py, self.abajo)
                MTH = self.CD(theta1, theta2, theta3, graficar=1)
                plt.plot(MTH.t[0], MTH.t[1], 'ro', markersize=1)  # Trayectoria CI tradicional

                theta1_red, theta2_red, _ = self.CI_red(Px, Py, self.abajo)
                MTH_red = self.CD(theta1_red, theta2_red, theta3, graficar=1)
                plt.plot(MTH_red.t[0], MTH_red.t[1], 'bo', markersize=1)  # Trayectoria CI red neuronal

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Trayectoria Comparativa: CI Geometrica vs. CI Red Neuronal")
        plt.legend()
        plt.show()
           
    # Agregar el gráfico con las coordenadas (x, y) de la imagen
    
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
        
    def CI_red(self, px, py, pz):
        h1 = 5
        l3 = 5
        d3 = -1 * (h1 - l3 - pz)
        theta_cre = d3 * 50
        theta_cre = math.radians(theta_cre)
        
        model = tf.keras.models.load_model('pruebas\Red_Neuronal\modelos\model_epoch_77_neurons_200_batchsize_264.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
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

    
robot_simulation = RobotSimulation()
robot_simulation.imagen_camara() # Comparacion Modelo red vs CI
# robot_simulation.CI(20,0,0)
# robot_simulation.CI_red(20,0,0)

