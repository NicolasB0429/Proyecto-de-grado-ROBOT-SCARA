import time
import matplotlib
matplotlib.use('Qt5Agg')

import math
import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import RevoluteDH, PrismaticDH, SerialLink
import matplotlib.pyplot as plt #Para plotear
from scipy.io import loadmat #Cargar .mat
import cv2 #Para generar contornos imagenes
#Graficar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
#animacion
from PyQt5.QtCore import QTimer

# # #Servos
# from adafruit_servokit import ServoKit
# from time import sleep
# kit=ServoKit(channels=16)
# servo=16 #Se coloca cuantos canales se van a usar
# #Se puede cambiar el rango de actuacion del servo
# kit.servo[0].set_pulse_width_range(600, 2500)
# kit.servo[1].set_pulse_width_range(600, 2500)
# kit.servo[2].set_pulse_width_range(600, 2500)

class CanvasGrafica(FigureCanvas):
    
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(facecolor='black')
        super().__init__(self.fig)
        self.ax.grid(True, which='both', linestyle='--', color='black', linewidth=0.8)
        self.ax.set_xlim(left=-22, right=22)
        self.ax.set_ylim(bottom=-20, top=22)
        self.ax.set_xlabel('Eje X', color='white')
        self.ax.set_ylabel('Eje Y', color='white')
        self.ax.set_aspect('auto')
        self.ax.tick_params(axis='both', which='major', labelsize=10, colors='white')
        self.ax.margins(x=0.1, y=0.1)
        self.trayectoria_puntos = []  # Lista para almacenar los puntos de la trayectoria

    def actualizar_trayectoria(self, x, y):
        """Actualizar la gráfica con la trayectoria del robot."""
        # Asegurarse de que x e y sean arrays o listas
        if isinstance(x, np.float64):
            x = [x]
        if isinstance(y, np.float64):
            y = [y]
        
        # Agregar nueva trayectoria como puntos
        self.ax.plot(x, y, 'bo')  # 'go' para puntos verdes
        self.trayectoria_puntos.extend(zip(x, y))  # Añadir los nuevos puntos a la lista de trayectoria
        self.ax.relim()
        self.ax.autoscale_view()
        self.draw()

    def actualizar_robot(self, p1, p2, p3):
        """Actualizar la gráfica con la posición del robot."""
        self.ax.clear()  # Limpiar la gráfica antes de actualizar
        # Redibujar la trayectoria
        if self.trayectoria_puntos:
            x_trayectoria, y_trayectoria = zip(*self.trayectoria_puntos)
            #self.ax.plot(x_trayectoria, y_trayectoria, 'g-.s')  # 'go' para puntos verdes
            #self.ax.plot(x_trayectoria, y_trayectoria, 'g^--', markersize=10, linewidth=2) 
            self.ax.plot(x_trayectoria, y_trayectoria, 'bo', markeredgewidth=1, markersize=3)

        # Redibujar el robot
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-o', lw=6, label='L1')
        self.ax.plot([p2[0], p3[0]], [p2[1], p3[1]], 'b-o', lw=6, label='L2')
        self.ax.text(p2[0], p2[1], 'L1', fontsize=8, ha='right', color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.1'))
        self.ax.text(p3[0], p3[1], 'L2', fontsize=8, ha='right', color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.1'))
        self.ax.set_title('Robot y Trayectoria', fontsize=12, color='white')
        self.ax.set_xlim(-22, 22)
        self.ax.set_ylim(-20, 22)
        self.ax.set_aspect('equal')
        self.draw()

    def limpiar_trayectoria(self):
            """Limpia la lista de puntos de la trayectoria y la gráfica."""
            self.trayectoria_puntos.clear()  # Borra los puntos almacenados
            self.ax.clear()  # Limpia la gráfica
            self.ax.grid(True, which='both', linestyle='--', color='black', linewidth=0.8)
            self.ax.set_xlim(left=-22, right=22)
            self.ax.set_ylim(bottom=-20, top=22)
            self.ax.set_xlabel('Eje X', color='white')
            self.ax.set_ylabel('Eje Y', color='white')
            self.ax.set_aspect('auto')
            self.ax.tick_params(axis='both', which='major', labelsize=10, colors='white')
            self.ax.margins(x=0.1, y=0.1)
            self.draw()  # Redibuja la gráfica en blanco
        
class Robot:
   
    #Constructor  
    def __init__(self, nombre, l1, l2, pxInicial, pyInicial, pzInicial, canvas_grafica, canvas_robot):

        self.nombre = nombre
        self.l1 = l1
        self.l2 = l2
       
        # Para la Cremallera
        self.arrriba_rad = math.radians(100)
        self.arrriba_cor = 2 #cm
        self.abajo = 0
       
        #Coordenadas iniciales de cada Articulación
        self.pxInicial = pxInicial
        self.pyInicial = pyInicial
        self.pzInicial = pzInicial #Eje Z Cremallera
       
        # Variables para las letras a donde se quiere ir x, y
        self.x_ir = 0;
        self.y_ir = 0;
       
        #ROBOT
        self.Robot_Scara = SerialLink([
            RevoluteDH(d=0, alpha=0, a=self.l1, offset=0),
            RevoluteDH(d=0, alpha=0, a=self.l2, offset=0),
            PrismaticDH(theta=0, a=0, alpha=np.pi, offset=0)
        ], name=self.nombre)
       
        #Variables para las graficas
        self.canvas_grafica = canvas_grafica
        self.canvas_robot = canvas_robot

        # Ajustar límites y características iniciales del gráfico
        self.canvas_robot.ax.set_title('Robot', fontsize=12, color='white')
        self.canvas_grafica.ax.set_title('Trayectoria Robot', fontsize=12, color='white')
       
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_paso)
        self.pasos = []
        self.indice_paso = 0

        # servo1 = kit.servo[0].angle
        # servo2 = kit.servo[1].angle

        # # #crem = round(kit.servo[2].angle)
        # # #print(f"1:{servo1}, 2:{servo2}, 3:{crem}")
        # # #if servo1 !=0 or servo2 !=0 or crem !=0 :
        # if servo1 !=0 or servo2 !=0:
        #     kit.servo[2].angle=math.degrees(self.arrriba_rad) #Servo Cremallera
        #     time.sleep(0.3)  # Pausa por 5 segundo
        #     self.mover_servos(0, 0, self.arrriba_rad, valor = 0)
        #     time.sleep(0.3)  # Pausa por 5 segundo
        #     self.mover_servos(0, 0, self.abajo, valor =  1)
   
    #Funcion para mover los servos
    def mover_servos(self,theta1,theta2,theta_cre,valor):        
       
        # Valor para mover servo1 y servo2 o para mover cremallera
        if valor == 1:
            theta_cre = math.degrees(theta_cre)
            # time.sleep(0.5)
            # kit.servo[2].angle=(theta_cre) #Servo Cremallera
            
        else:
            theta1 = math.degrees(theta1)
            theta2 = math.degrees(theta2)
            # time.sleep(0.5)
            # kit.servo[0].angle=(theta1) #Servo 1
            # kit.servo[1].angle=(theta2) #Servo 2
   
    def coordenadas(self,xu,yu):
        
        self.canvas_grafica.limpiar_trayectoria()
        # Cargar variables desde el archivo .mat
        contorno = loadmat('robot_2R/contorno.mat')
        # Acceder a las variables cargadas
        x1y1 = contorno['x1y1']
        x2y2 = contorno['x2y2']
        x3y3 = contorno['x3y3']
        x4y4 = contorno['x4y4']

        flag1 = 0 #Comparacion seccion derecha
        flag2 = 0 #Comparacion seccion izquierda

        Px1 = self.pxInicial
        Py1 = self.pyInicial
        Pz1 = self.arrriba_cor
        theta1_P1, theta2_P1, theta3_P1 = self.CI(Px1, Py1, Pz1)

        Px2 = xu
        Py2 = yu
        Pz2 = self.arrriba_cor
        theta1_P2, theta2_P2, tetha3_P2= self.CI(Px2, Py2, Pz2)

        #Derecha abajo
        for i in range(len(x1y1)):
            if x1y1[i, 0] >= xu:
                if x1y1[i, 1] <= yu:
                    flag1 += 1
                    break

        #Derecha arriba
        for i in range(len(x2y2)):
            if x2y2[i, 0] <= xu:
                if x2y2[i, 1] >= yu:
                    flag1 += 1
                    break

        #Izquierda arriba
        for i in range(len(x3y3)):
            if x3y3[i, 0] <= xu:
                if x3y3[i, 1] >= yu:
                    flag2 += 1
                    break

        #Izquierda abajo
        for i in range(len(x4y4)):
            if x4y4[i, 0] >= xu:
                if x4y4[i, 1] <= yu:
                    flag2 += 1
                    break
              
        if flag1 == 2 or flag2 == 2: 
            
            pasos = []
                    
            theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, 10)
            theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, 10)
            theta3P1_P2 = theta3_P1
            
            pasos.append((theta1P1_P2[0],theta2P1_P2[0],theta3P1_P2,0,1)) #Para subir cremallera
            
            # Preparar pasos
            for i in range(len(theta1P1_P2)):
                pasos.append((theta1P1_P2[i],theta2P1_P2[i],theta3P1_P2,1,0))
                # Realizar accion para la ultima iteracion
                if i == len(theta1P1_P2) - 1: #Ultima Iteracion
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo,0)
                    # Bajar Cremallera
                    pasos.append((theta1P1_P2[-1],theta2P1_P2[i],self.abajo,0,1))
                    # Guardar Coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]  
                    self.pzInicial = self.abajo
                    
            self.pasos = pasos
            self.indice_paso = 0
            self.timer.start(100)
                    
        else:
            #Aqui va la imagen de error que no esta dentro del espacio de trabajo del Robot
            print("No esta dentro del espacio de trabajo del Robot")

    def esp_trabajo(self):
        
        self.canvas_grafica.limpiar_trayectoria()

        #Cantidad de linspace y de iteraciones en los for
        can_puntos = 5
       
        #Para ir a Posición Inicial
        Px1 = self.pxInicial
        Py1 = self.pyInicial
        Pz1 = self.arrriba_cor
        theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)
        
        # Preparar pasos para la animación
        pasos = []
        
        theta1P1_P2 = np.linspace(theta1_P1,0,can_puntos)
        theta2P1_P2 = np.linspace(theta2_P1,(5/6)*np.pi,can_puntos)

        pasos.append((theta1P1_P2[0],theta2P1_P2[0],theta3_P1,0,1)) #Para subir cremallera
        
        # Ir a Coordenada Inicial
        for i in range(can_puntos):
            MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1,0)
            self.pasos.append((theta1P1_P2[i],theta2P1_P2[i],theta3_P1,0,0)) 
            if i == can_puntos - 1: #Ultima Iteracion
                # Bajar Cremallera
                pasos.append((theta1P1_P2[i],theta2P1_P2[i],self.abajo,0,1)) #Para bajar cremallera
        
        #Comienza entorno de trabajo
        theta1P2_P3 = 0
        theta2P2_P3 = np.linspace((5/6)*np.pi,0,can_puntos)
            
        for i in range(can_puntos):
            MTH = self.CD(theta1P2_P3,theta2P2_P3[i],self.abajo,0)
            pasos.append((theta1P2_P3,theta2P2_P3[i],self.abajo,1,0))
           
        theta1P3_P4 = np.linspace(0,np.pi/2,can_puntos)
        theta2P3_P4 = 0       
        
        for i in range(can_puntos):
            MTH = self.CD(theta1P3_P4[i],theta2P3_P4,self.abajo,0)
            pasos.append((theta1P3_P4[i], theta2P3_P4, self.abajo,1,0))

        theta1P4_P5 = np.linspace(np.pi/2,np.pi,can_puntos)
        theta2P4_P5 = 0
        for i in range(can_puntos):
            MTH = self.CD(theta1P4_P5[i],theta2P4_P5,self.abajo,0)
            pasos.append((theta1P4_P5[i], theta2P4_P5, self.abajo,1,0))

        theta1P5_P6 = np.pi
        theta2P5_P6 = np.linspace(0,(29/36)*np.pi,can_puntos) #145
        for i in range(can_puntos):
            MTH = self.CD(theta1P5_P6,theta2P5_P6[i],self.abajo,0)
            pasos.append((theta1P5_P6, theta2P5_P6[i], self.abajo,1,0))
            # Realizar accion para la ultima iteracion
            if i == can_puntos - 1: #Ultima Iteracion
                self.pxInicial = MTH.t[0]
                self.pyInicial = MTH.t[1]
                self.pzInicial = self.abajo
        
        self.pasos = pasos
        self.indice_paso = 0
        self.timer.start(100)
        
    def imagenes(self,opcion):
        self.canvas_grafica.limpiar_trayectoria()
        
        puntos = 50 #De a cada cuantos puntos se guardan imagenes
        can_puntos = 2 #Numero de puntos for y linspace
        pasos = []
       
        #FIGURA 1 Hyundai
        if opcion == 1:
            #Leer la imagen en formato cv2
            imagen = cv2.imread('robot_2R/imagenes/hyundai.png')
            # Convertir la imagen a escala de grises
            img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            # Aplicar suavizado Gaussiano (filtro) Imagen Filtrada
            img_fil = cv2.GaussianBlur(img_gris, (5,5), 0) #El 0 calcula la Desviacion Estandar automaticamente
            # Encontrar los contornos en la imagen (imagen, metodo, para que se almacenen todos los puntos)
            contornos, _ = cv2.findContours(img_fil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            ofset=820
            contornos_escalados = []
           
            # Acá se hace el escalamiento de coordenadas
            for i in range(len(contornos)):
                # Ajustar espejo, coordenadas y convertirlas en un array numpy
                contorno = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[i]])
                # Seleccionar cada n elemento y agregar el último punto
                contorno = np.vstack([contorno[0::puntos], contorno[-1]])
                # Añadir el contorno procesado a la lista
                contornos_escalados.append(contorno)
           
            for n_contorno in contornos_escalados:
                # Puntos iniciales para Contorno 1 (Cremallera)
                Px1 = self.pxInicial
                Py1 = self.pyInicial
                Pz1 = self.arrriba_cor
                theta1_P1, theta2_P1, theta3_P1 = self.CI(Px1, Py1, Pz1)

                Px2 = n_contorno[0, 0]
                Py2 = n_contorno[0, 1]
                Pz2 = self.arrriba_cor
                theta1_P2, theta2_P2, theta3_P2 = self.CI(Px2, Py2, Pz2)

                theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, can_puntos)
                theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, can_puntos)

                # Subir Cremallera
                pasos.append((theta1P1_P2[0],theta2P1_P2[0],theta3_P1,0,1)) #Para subir cremallera

                # Ir a Coordenada Inicial
                for i in range(can_puntos):
                    pasos.append((theta1P1_P2[i],theta2P1_P2[i],self.abajo,0,0))
                    if i == can_puntos - 1:
                        pasos.append((theta1P1_P2[i],theta2P1_P2[i],theta3_P1,0,1)) #Para bajar cremallera

                for i, punto in enumerate(n_contorno):
                    theta1,theta2,theta3 = self.CI(punto[0],punto[1],self.abajo)
                    pasos.append((theta1,theta2,theta3,1,0))
                    
                    if i == len(n_contorno)-1:  # Última iteración
                        MTH = self.CD(theta1,theta2,theta3,0)
                        # Guardar últimas coordenadas
                        self.pxInicial = MTH.t[0]
                        self.pyInicial = MTH.t[1]
                        self.pzInicial = self.abajo
                    
        #FIGURA 2 Chevrolet
        elif opcion == 2:
            #Leer la imagen en formato cv2
            imagen = cv2.imread('robot_2R/imagenes/chevrolet.png')

            # Convertir la imagen a escala de grises
            img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

            # Aplicar suavizado Gaussiano (filtro) Imagen Filtrada
            img_fil = cv2.GaussianBlur(img_gris, (5,5), 0) #El 0 calcula la Desviacion Estandar automaticamente

            # Encontrar los contornos en la imagen (imagen, metodo, para que se almacenen todos los puntos)
            contornos, _ = cv2.findContours(img_fil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            #print(len(contornos)) #Corroborar numero de contornos

            ofset=500
            contornos_escalados = []
           
            # Acá se hace el escalamiento de coordenadas
            for i in range(len(contornos)):
                # Ajustar espejo, coordenadas y convertirlas en un array numpy
                contorno = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+10.5] for punto in contornos[i]])
                # Seleccionar cada n elemento y agregar el último punto
                contorno = np.vstack([contorno[0::puntos], contorno[-1]])
                # Añadir el contorno procesado a la lista
                contornos_escalados.append(contorno)
           
            for n_contorno in contornos_escalados:
                # Puntos iniciales para Contorno 1 (Cremallera)
                Px1 = self.pxInicial
                Py1 = self.pyInicial
                Pz1 = self.arrriba_cor
                theta1_P1, theta2_P1, theta3_P1 = self.CI(Px1, Py1, Pz1)

                Px2 = n_contorno[0, 0]
                Py2 = n_contorno[0, 1]
                Pz2 = self.arrriba_cor
                theta1_P2, theta2_P2, theta3_P2 = self.CI(Px2, Py2, Pz2)

                theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, can_puntos)
                theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, can_puntos)

                # Subir Cremallera
                pasos.append((theta1P1_P2[0],theta2P1_P2[0],theta3_P1,0,1)) #Para subir cremallera

                # Ir a Coordenada Inicial
                for i in range(can_puntos):
                    pasos.append((theta1P1_P2[i],theta2P1_P2[i],theta3_P1,0,0))
                    if i == can_puntos - 1:
                        pasos.append((theta1P1_P2[i],theta2P1_P2[i],self.abajo,0,1)) #Para bajar cremallera

                for i, punto in enumerate(n_contorno):
                    theta1,theta2,theta3 = self.CI(punto[0],punto[1],self.abajo)
                    pasos.append((theta1,theta2,theta3,1,0))
                    
                    if i == len(n_contorno)-1:  # Última iteración
                        MTH = self.CD(theta1,theta2,theta3,0)
                        # Guardar últimas coordenadas
                        self.pxInicial = MTH.t[0]
                        self.pyInicial = MTH.t[1]
                        self.pzInicial = self.abajo
        
        #FIGURA 3 Tesla
        elif opcion == 3:
            #Leer la imagen en formato cv2
            imagen = cv2.imread('robot_2R/imagenes/tesla.png')

            # Convertir la imagen a escala de grises
            img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

            # Aplicar suavizado Gaussiano (filtro) Imagen Filtrada
            img_fil = cv2.GaussianBlur(img_gris, (5,5), 0) #El 0 calcula la Desviacion Estandar automaticamente

            # Encontrar los contornos en la imagen (imagen, metodo, para que se almacenen todos los puntos)
            contornos, _ = cv2.findContours(img_fil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            print(len(contornos)) #Corroborar numero de contornos

            ofset=1500
            contornos_escalados = []
           
            # Acá se hace el escalamiento de coordenadas
            for i in range(len(contornos)):
                # Ajustar espejo, coordenadas y convertirlas en un array numpy
                contorno = np.array([[(punto[0][0]/100)-15, ((punto[0][1]*-1+ofset)/100)-5] for punto in contornos[i]])
                # Seleccionar cada n elemento y agregar el último punto
                contorno = np.vstack([contorno[0::puntos], contorno[-1]])
                # Añadir el contorno procesado a la lista
                contornos_escalados.append(contorno)

            for n_contorno in contornos_escalados:
                # Puntos iniciales para Contorno 1 (Cremallera)
                Px1 = self.pxInicial
                Py1 = self.pyInicial
                Pz1 = self.arrriba_cor
                theta1_P1, theta2_P1, theta3_P1 = self.CI(Px1, Py1, Pz1)

                Px2 = n_contorno[0, 0]
                Py2 = n_contorno[0, 1]
                Pz2 = self.arrriba_cor
                theta1_P2, theta2_P2, theta3_P2 = self.CI(Px2, Py2, Pz2)

                theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, can_puntos)
                theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, can_puntos)

                # Subir Cremallera
                pasos.append((theta1P1_P2[0],theta2P1_P2[0],theta3_P1,0,1)) #Para subir cremallera

                # Ir a Coordenada Inicial
                for i in range(can_puntos):
                    pasos.append((theta1P1_P2[i],theta2P1_P2[i],self.abajo,0,0))
                    if i == can_puntos - 1:
                        pasos.append((theta1P1_P2[i],theta2P1_P2[i],theta3_P1,0,1)) #Para bajar cremallera

                for i, punto in enumerate(n_contorno):
                    theta1,theta2,theta3 = self.CI(punto[0],punto[1],self.abajo)
                    pasos.append((theta1,theta2,theta3,1,0))
                    
                    if i == len(n_contorno)-1:  # Última iteración
                        MTH = self.CD(theta1,theta2,theta3,0)
                        # Guardar últimas coordenadas
                        self.pxInicial = MTH.t[0]
                        self.pyInicial = MTH.t[1]
                        self.pzInicial = self.abajo
                
        self.pasos = pasos
        self.indice_paso = 0
        self.timer.start(100)
                               
    def palabra(self,palabra):
        
        self.canvas_grafica.limpiar_trayectoria()
        pasos = []

        def abecedario(letra,Pxf,Pyf,i):
            
            self.canvas_grafica.limpiar_trayectoria()
            self.canvas_grafica.ax.autoscale_view()
            #Numero de puntos de todas las letras
            can_puntos = 10
            #IMPORTANTE
            lon = 2 #Esta variable hace lo largo de letra en este caso 2cm
           
            #Generacion de todas las letras
            if letra == 'a' or letra == 'A':
               
                if i == 0:
                    # Bajar Cremallera
                    Pxf,Pyf = arriba_diagonal(0,0,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                 
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(-lon,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -1
               
            elif letra == 'b' or letra == 'B':
               
                if i == 0:
                    # Bajar Cremallera
                    Pxf,Pyf = arriba_diagonal(0,0,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                 
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(lon/2,0,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = 0
               
            elif letra == 'c' or letra == 'C':
               
                if i == 0:  
                    # Ir a punto Inicial
                    Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 2
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0  
             
            elif letra == 'd' or letra == 'D':
               
                if i == 0:
                    # Bajar Cremallera
                    Pxf,Pyf = arriba_diagonal(0,0,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                 
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon/2,Pxf, Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = 0
               
            elif letra == 'e' or letra == 'E':
               
                if i == 0:  
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 2
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(-lon,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon/2,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 2
                self.y_ir = -1    
           
            elif letra == 'f' or letra == 'F':
               
                if i == 0:  
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 2
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(0,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon/2,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 2
                self.y_ir = -1  
           
            elif letra == 'g' or letra == 'G':
               
                if i == 0:    
                    # Ir a punto Inicial
                    Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 2
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon/2,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 2
                self.y_ir = -1  
           
            elif letra == 'h' or letra == 'H':
               
                if i == 0:    
                    # Ir a punto Inicial
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(-lon,lon/2,Pxf,Pyf,can_puntos)                
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -1
           
            elif letra == 'i' or letra == 'I':
               
                if i == 0:    
                    # Ir a punto Inicial
                    Pxf,Pyf = arriba_diagonal(lon/2,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 1
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(-lon/2,lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(-lon,-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)  
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == 'j' or letra == 'J':
               
                if i == 0:  
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(-lon/2,0,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(lon/2,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = -1
           
            elif letra == 'k' or letra == 'K':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon,-lon/2,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == 'l' or letra == 'L':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == 'm' or letra == 'M':
               
                if i == 0:
                    # Bajar Cremallera
                    Pxf,Pyf = arriba_diagonal(0,0,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                 
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)  
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == 'n' or letra == 'N' or letra == 'ñ' or letra == 'Ñ':
               
                if i == 0:
                    # Bajar Cremallera
                    Pxf,Pyf = arriba_diagonal(0,0,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                 
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)  
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -2
           
            elif letra == 'o' or letra == 'O':
               
                if i == 0:  
                    # Ir a punto Inicial    
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = -2
           
            elif letra == 'p' or letra == 'P':
               
                if i == 0:
                    # Bajar Cremallera
                    Pxf,Pyf = arriba_diagonal(0,0,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                 
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)

                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = -1
           
            elif letra == 'q' or letra == 'Q':
               
                if i == 0:
                    # Bajar Cremallera
                    Pxf,Pyf = arriba_diagonal(0,0,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                 
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(lon/2,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)

                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == 'r' or letra == 'r':
               
                if i == 0:
                    # Bajar Cremallera
                    Pxf,Pyf = arriba_diagonal(0,0,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                 
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)

                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == 's' or letra == 's':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 2
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = 0
           
            elif letra == 't' or letra == 'T':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(lon/2,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 1
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(-lon/2,lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)  
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -2
           
            elif letra == 'u' or letra == 'U':
               
                if i == 0:  
                    # Ir a punto Inicial    
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)  
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -2
           
            elif letra == 'v' or letra == 'V':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_diagonal(lon/4,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/4,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/4,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/4,lon/2,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -2
           
            elif letra == 'w' or letra == 'W':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)    
                Pxf,Pyf = linea_diagonal(lon/2,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)    
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -2
           
            elif letra == 'x' or letra == 'X':
               
                if i == 0:  
                    # Ir a punto Inicial    
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = 0
           
            elif letra == 'y' or letra == 'Y':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
                   
                Pxf,Pyf = linea_diagonal(lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(lon/2,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = 0
           
            elif letra == 'z' or letra == 'Z':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)    
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)    
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == '0':
               
                if i == 0:  
                    # Ir a punto Inicial    
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = -2
           
            elif letra == '1':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon/2,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 1
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_diagonal(lon/2,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(-lon/2,0,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)    
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == '2':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)    
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)    
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)    
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == '3':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)    
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(0,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)    
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -1
           
            elif letra == '4':
               
                if i == 0:  
                    # Ir a punto Inicial    
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(0,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == '5':
               
                if i == 0:  
                    # Ir a punto Inicial    
                    Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 2
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)

                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = 0
           
            elif letra == '6':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 2
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)

                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 3
                self.y_ir = -1
           
            elif letra == '7':
               
                if i == 0:  
                    # Ir a punto Inicial    
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_diagonal(-lon/2,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(0,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)

                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -1
           
            elif letra == '8':
               
                if i == 0:    
                    # Ir a punto Inicial  
                    Pxf,Pyf = arriba_diagonal(0,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(0,-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = -1
           
            elif letra == '9':
               
                if i == 0:
                    # Ir a punto Inicial      
                    Pxf,Pyf = arriba_diagonal(lon,lon,Pxf,Pyf,can_puntos)
               
                elif i != 0:
                    self.x_ir = self.x_ir + 2
                    self.y_ir = self.y_ir + 2
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                Pxf,Pyf = linea_horizontal(-lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_horizontal(lon,Pxf,Pyf,can_puntos)
                Pxf,Pyf = arriba_diagonal(0,lon/2,Pxf,Pyf,can_puntos)
                Pxf,Pyf = linea_vertical(-lon,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            elif letra == ' ':
               
                if i == 0:  
                    # Ir a punto Inicial    
                    Pxf,Pyf = arriba_diagonal(lon/2,lon/2,Pxf,Pyf,can_puntos)
               
                if i != 0:
                    self.x_ir = self.x_ir + 1
                    self.y_ir = self.y_ir + 1
                    Pxf,Pyf = arriba_diagonal(self.x_ir,self.y_ir,Pxf,Pyf,can_puntos)
               
                # Lo que falta para llegar a punto de comienzo de otra letra
                self.x_ir = 1
                self.y_ir = 0
           
            return Pxf,Pyf
                   
        #Funcion Interna para lineas verticales
        def linea_vertical(lon, Px1, Py1, can_puntos):
            
            Pxf = Px1
            Pyf = Py1 + lon

            Px7_Pxf = Pxf
            Py7_Pyf = np.linspace(Py1,Pyf,can_puntos)
            
            # Preparar pasos para la animación
        
            for i in range(can_puntos):
                theta1,theta2,tetha3 = self.CI(Px7_Pxf, Py7_Pyf[i],self.abajo)
                # MTH = self.CD(theta1,theta2,tetha3)
                # self.mover_servos(theta1,theta2,tetha3,0)
                pasos.append((theta1,theta2,tetha3,1,0))
                
            #Retorno
            return Pxf, Pyf
       
        #Funcion Interna para lineas horizontales
        def linea_horizontal(lon, Px1, Py1, can_puntos):
            Pxf = Px1 + lon
            Pyf = Py1

            Px7_Pxf = np.linspace(Px1,Pxf,can_puntos)
            Py7_Pyf = Pyf

            for i in range(can_puntos):
                theta1,theta2,theta3 = self.CI(Px7_Pxf[i],Py7_Pyf,self.abajo)
                # MTH = self.CD(theta1,theta2,theta3)
                # self.mover_servos(theta1,theta2,theta3,0)
                pasos.append((theta1,theta2,theta3,1,0))
            #Retorno
            return Pxf, Pyf
       
        #Funcion Interna para lineas horizontales
        def linea_diagonal(lonx, lony, Px1, Py1, can_puntos):
            Pxf = Px1 + lonx
            Pyf = Py1 + lony

            Px7_Pxf = np.linspace(Px1, Pxf, can_puntos)
            Py7_Pyf = np.linspace(Py1, Pyf, can_puntos)

            for i in range(can_puntos):
                theta1,theta2,theta3 = self.CI(Px7_Pxf[i], Py7_Pyf[i],self.abajo)
                # MTH = self.CD(theta1,theta2,theta3)
                # self.mover_servos(theta1,theta2,theta3,0)
                pasos.append((theta1,theta2,theta3,1,0))
            #Retorno
            return Pxf, Pyf
           
        #Funcion Interna para alzar cremallera
        def arriba_diagonal(lonx, lony, Px1, Py1, can_puntos):
            # (x_ir,y_ir,x_esta,y_esta,can_puntos)
            can_puntos = 2 # Para que solo sean 2 posiciones arriba
           
            Pxf = Px1 + lonx
            Pyf = Py1 + lony
           
            # Esto es para solo bajar
            if lonx == 0 and lony == 0:
                theta1,theta2,theta3 = self.CI(Px1,Py1,self.abajo)
                pasos.append((theta1,theta2,theta3,0,1))
           
            else:                
                Px7_Pxf = np.linspace(Px1, Pxf, can_puntos)
                Py7_Pyf = np.linspace(Py1, Pyf, can_puntos)
               
                # Subir Cremallera
                theta1,theta2,theta3 = self.CI(Px1,Py1,self.arrriba_cor)
                pasos.append((theta1,theta2,theta3,0,1))
               
                for i in range(can_puntos):
                    theta1,theta2,theta3 = self.CI(Px7_Pxf[i],Py7_Pyf[i],self.arrriba_cor)
                    pasos.append((theta1,theta2,theta3,0,0))
                    
                    if i == can_puntos - 1:
                        # Bajar Cremallera
                        pasos.append((theta1,theta2,self.abajo,0,1))
           
            #Retorno
            return Pxf, Pyf
        
        #Cantidad de puntos para que llegue a coordenadas iniciales para escribir
        can_puntos = 5
       
        # Puntos Iniciales
        Px1 = self.pxInicial
        Py1 = self.pyInicial
        Pz1 = self.arrriba_cor
        theta1_P1, theta2_P1, theta3_P1 = self.CI(Px1, Py1, Pz1)

        #Coordenadas donde se comienza a escribir
        Px2 = -13
        Py2 = 11
        Pz2 = self.arrriba_cor
        theta1_P2, theta2_P2, tetha3_P2= self.CI(Px2, Py2, Pz2)
       
        theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
        theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)

        # Subir Cremallera
        pasos.append((theta1P1_P2[0],theta2P1_P2[0],theta3_P1,0,1))
       
        for i in range(can_puntos):
            pasos.append((theta1P1_P2[i],theta2P1_P2[i],theta3_P1,0,0))
            # No hace falta bajar cremallera (En las letras lo hace)
               
        #Esto es para que se guarden las ultimas coordenadas en pxInicial y pyInicial
        self.pxInicial = Px2
        self.pyInicial = Py2
        self.pzInicial = self.abajo
       
        if len(palabra)<=9:
            for i in range(len(palabra)):
                Pxf, Pyf = abecedario(palabra[i], self.pxInicial, self.pyInicial,i)
                self.pxInicial = Pxf
                self.pyInicial = Pyf
       
        #Cuando la palabra es muu extensa        
        else:
            print("La palabra o nombre excede los 9 caracteres")
            
        # Preparar los pasos para la animación final
        self.pasos = pasos
        self.indice_paso = 0
        self.timer.start(1)
  
    #Cinematica Inversa (Coordenadas a Angulos)
    def CI(self,px,py,pz):
        h1 = 5
        l3 = 5
       
        # Theta2
        b = np.sqrt(px**2 + py**2)
        cos_theta2 = (b**2-self.l2**2-self.l1**2)/(2*self.l2*self.l1)
        sen_theta2 = np.sqrt(1 - cos_theta2**2)
        theta2 = np.arctan2(sen_theta2, cos_theta2)
        #print(f'Theta2 = {np.degrees(theta2):.3f} grados')
       
        # Theta1
        alpha = np.arctan2(py,px)
        phi = np.arctan2(self.l2 * sen_theta2, self.l1 + self.l2 * cos_theta2)
        # Calcular theta1
        theta1 = alpha - phi
        theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1 #Otra forma de hacer el if
        #print(f'Theta1 = {np.degrees(theta1):.3f} grados')
       
        # d3
        d3 = -1 * (h1 - l3 - pz)
        theta_cre = d3 * 50
        #print(f'Theta3 = {theta_cre:.3f} grados')
        theta_cre = math.radians(theta_cre)
       
        #Retorno
        return theta1,theta2,theta_cre

    # Cinematica Directa (Angulos a Coordenadas)
    def CD(self, theta1, theta2, theta_cre, graficar):
            theta_cre = math.degrees(theta_cre)
            d3 = theta_cre / 50  # Convertir theta_cre en un movimiento lineal
            q = np.array([theta1, theta2, d3])
            MTH = self.Robot_Scara.fkine(q)
            
            if (graficar == 1):
                links = self.Robot_Scara.links
                p1 = [0, 0]
                p2 = [links[0].a * np.cos(q[0]), links[0].a * np.sin(q[0])]
                p3 = [p2[0] + links[1].a * np.cos(q[0] + q[1]), p2[1] + links[1].a * np.sin(q[0] + q[1])]
                self.canvas_grafica.actualizar_robot(p1, p2, p3)
            
            return MTH

    def actualizar_paso(self):
        self.canvas_grafica.ax.autoscale_view() 
        
        if self.indice_paso < len(self.pasos):
            # (theta1,theta2,cremallera,graficar,mov_cremallera)
            theta1,theta2,theta_cre,graficar,mover = self.pasos[self.indice_paso]
            MTH = self.CD(theta1,theta2,theta_cre,1)
            #Cuando se requiera graficar
            if graficar == 1:    
                self.canvas_grafica.actualizar_trayectoria(MTH.t[0], MTH.t[1])
                
            if (mover==0):
                self.mover_servos(theta1,theta2,theta_cre,0)
            else:     
                self.mover_servos(theta1,theta2,theta_cre,1)
            
            self.indice_paso += 1
            
        else:
            self.timer.stop()