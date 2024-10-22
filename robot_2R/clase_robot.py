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

# # Servos
# from adafruit_servokit import ServoKit
# from time import sleep
# kit=ServoKit(channels=16)
# servo=16 #Se coloca cuantos canales se van a usar
# #Se puede cambiar el rango de actuacion del servo
# kit.servo[0].set_pulse_width_range(600, 2500)
# kit.servo[1].set_pulse_width_range(600, 2500)
# kit.servo[2].set_pulse_width_range(600, 2500)

class Robot:
    #Atributos
    def __init__(self,nombre,l1,l2,pxInicial,pyInicial,pzInicial):
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

        # servo1 = round(kit.servo[0].angle) 
        # servo2 = round(kit.servo[1].angle)
        # crem = round(kit.servo[2].angle)
        # print(f"1:{servo1}, 2:{servo2}, 3:{crem}")
        # if servo1 !=0 or servo2 !=0 or crem !=0:
        # if servo1 !=0 or servo2 !=0:
        #     kit.servo[2].angle=(math.degrees(self.arrriba_rad)) #Servo Cremallera
        #     time.sleep(0.3)  # Pausa por 5 segundo
        #     self.mover_servos(0, 0, self.arrriba_rad)
        #     self.mover_servos(0, 0, self.abajo)
    
    #Funcion para mover los servos
    def mover_servos(self, theta1, theta2, theta_cre):
        # Convertir los �ngulos de radianes a grados (OPCIONAL)
        theta1 = math.degrees(theta1)
        theta2 = math.degrees(theta2)
        theta_cre = math.degrees(theta_cre)

        # kit.servo[0].angle=(theta1) #Servo 1
        # kit.servo[1].angle=(theta2) #Servo 2
        # time.sleep(0.3)
        # kit.servo[2].angle=(theta_cre) #Servo Cremallera
        # time.sleep(0.3)  # Pausa por 5 segundo
        
    def coordenadas(self,xu,yu):
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
            theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, 10)
            theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, 10)
            theta3P1_P2 = theta3_P1

            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0], theta2P1_P2[0], theta3P1_P2) 
            self.mover_servos(theta1P1_P2[0], theta2P1_P2[0], theta3P1_P2)

            for i in range(len(theta1P1_P2)):
                MTH = self.CD(theta1P1_P2[i], theta2P1_P2[i], theta3P1_P2) 
                self.mover_servos(theta1P1_P2[i], theta2P1_P2[i], theta3P1_P2)
                plt.figure("Trayectoria Robot")
                plt.plot(MTH.t[0], MTH.t[1], '*r')
                # Realizar accion para la ultima iteracion
                if i == len(theta1P1_P2) - 1: #Ultima Iteracion
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i], theta2P1_P2[i], self.abajo)
                    self.mover_servos(theta1P1_P2[i], theta2P1_P2[i], self.abajo)
                    # Guardar Coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]  
                    self.pzInicial = self.abajo 
                    
            # Mantener la figura abierta
            plt.show(block=True)            
        else:
            #Aqui va la imagen de error que no esta dentro del espacio de trabajo del Robot
            print("No esta dentro del espacio de trabajo del Robot")

    def esp_trabajo(self):
        #Cantidad de linspace y de iteraciones en los for
        can_puntos = 5
        
        #Para ir a Posición Inicial
        Px1 = self.pxInicial
        Py1 = self.pyInicial
        Pz1 = self.arrriba_cor
        theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)
        
        theta1P1_P2 = np.linspace(theta1_P1,0,can_puntos)
        theta2P1_P2 = np.linspace(theta2_P1,(5/6)*np.pi,can_puntos)

        # Subir Cremallera
        MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
        self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)
        
        for i in range(can_puntos):
            MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
            self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
        
        #Comienza entorno de trabajo
        theta1P2_P3 = 0
        theta2P2_P3 = np.linspace((5/6)*np.pi,0,can_puntos)
        for i in range(can_puntos):
            MTH = self.CD(theta1P2_P3,theta2P2_P3[i],self.abajo) 
            self.mover_servos(theta1P2_P3,theta2P2_P3[i],self.abajo)
            
        theta1P3_P4 = np.linspace(0,np.pi/2,can_puntos)
        theta2P3_P4 = 0
        for i in range(can_puntos):
            MTH = self.CD(theta1P3_P4[i],theta2P3_P4,self.abajo) 
            self.mover_servos(theta1P3_P4[i],theta2P3_P4,self.abajo)

        theta1P4_P5 = np.linspace(np.pi/2,np.pi,can_puntos)
        theta2P4_P5 = 0
        for i in range(can_puntos):
            MTH = self.CD(theta1P4_P5[i],theta2P4_P5,self.abajo) 
            self.mover_servos(theta1P4_P5[i],theta2P4_P5,self.abajo)

        theta1P5_P6 = np.pi
        theta2P5_P6 = np.linspace(0,(29/36)*np.pi,can_puntos) #145
        for i in range(can_puntos):
            MTH = self.CD(theta1P5_P6,theta2P5_P6[i],self.abajo) 
            self.mover_servos(theta1P5_P6,theta2P5_P6[i],self.abajo)
            # Realizar accion para la ultima iteracion
            if i == can_puntos - 1: #Ultima Iteracion
                self.pxInicial = MTH.t[0]
                self.pyInicial = MTH.t[1]
                self.pzInicial = self.abajo
    
    def imagenes(self,opcion):
        puntos = 3 #De a cada cuantos puntos se guardan imagenes
        can_puntos = 2 #Numero de puntos for y linspace
        
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
            # COMTORMO #1
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno1 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[0]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno1 = np.vstack([contorno1[0::puntos], contorno1[-1]])

            # COMTORMO #2
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno2 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[1]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno2 = np.vstack([contorno2[0::puntos], contorno2[-1]])

            # COMTORMO #3
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno3 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[2]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno3 = np.vstack([contorno3[0::puntos], contorno3[-1]])

            # COMTORMO #4
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno4 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[4]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno4 = np.vstack([contorno4[0::puntos], contorno4[-1]])

            # COMTORMO #5
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno5 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[3]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno5 = np.vstack([contorno5[0::puntos], contorno5[-1]])

            #Puntos iniciales para Contorno 1 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno1[0,0]
            Py2 = contorno1[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2,theta2_P2,theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
        
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(len(can_puntos)):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == len(can_puntos) - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    
            #AHORA SI DIBUJAR CONTORNOS
            #CONTORNO 1
            for i in range(len(contorno1)):
                theta1,theta2,theta3 = self.CI(contorno1[i][0],contorno1[i][1],self.abajo)
                MTH = self.CD(theta1,theta2,theta3) 
                self.mover_servos(theta1,theta2,theta3)
                if i == len(contorno1) - 1:
                    #Guardar ultimas coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                    self.pzInicial = self.abajo

            #Puntos iniciales para Contorno 2 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno2[0,0]
            Py2 = contorno2[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2,theta2_P2,theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
            
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(len(can_puntos)):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == len(can_puntos) - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
            
            #CONTORNO 2
            for i in range(len(contorno2)):
                theta1,theta2,theta3= self.CI(contorno2[i][0],contorno2[i][1],self.abajo)
                MTH = self.CD(theta1,theta2,theta3)
                self.mover_servos(theta1,theta2,theta3) 
                if i == len(contorno2) - 1:
                    #Guardar ultimas coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                    self.pzInicial = self.abajo
                    
            #Puntos iniciales para Contorno 3 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno3[0,0]
            Py2 = contorno3[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2,theta2_P2,theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
            
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(len(can_puntos)):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == len(can_puntos) - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)

            #CONTORNO 3
            for i in range(len(contorno3)):
                theta1,theta2,theta3 = self.CI(contorno3[i][0],contorno3[i][1],self.abajo)
                MTH = self.CD(theta1,theta2,theta3) 
                self.mover_servos(theta1,theta2,theta3)
                if i == len(contorno3) - 1:
                    #Guardar ultimas coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                    self.pzInicial = self.abajo
                    
            #Puntos iniciales para Contorno 4 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno4[0,0]
            Py2 = contorno4[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2,theta2_P2,theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
            
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(len(can_puntos)):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == len(can_puntos) - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)

            #CONTORNO 4
            for i in range(len(contorno4)):
                theta1,theta2,theta3 = self.CI(contorno4[i][0],contorno4[i][1],self.abajo)
                MTH = self.CD(theta1,theta2,theta3) 
                self.mover_servos(theta1,theta2,theta3)
                if i == len(contorno4) - 1:
                    #Guardar ultimas coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                    self.pzInicial = self.abajo

            #Puntos iniciales para Contorno 5 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno5[0,0]
            Py2 = contorno5[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2,theta2_P2,theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
            
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(len(can_puntos)):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == len(can_puntos) - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
            
            #CONTORNO 5
            for i in range(len(contorno5)):
                theta1, theta2 = self.CI(contorno5[i][0],contorno5[i][1])
                MTH = self.CD(theta1, theta2) 
                self.mover_servos(theta1, theta2)
                #Ultima Iteracion
                if i == len(contorno5) - 1: 
                    #Guardar ultimas coordenadas
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
            # COMTORMO #1
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno1 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+10.5] for punto in contornos[0]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno1 = np.vstack([contorno1[0::puntos], contorno1[-1]])

            # COMTORMO #2
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno2 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+10.5] for punto in contornos[1]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno2 = np.vstack([contorno2[0::puntos], contorno2[-1]])

            #Puntos iniciales para Contorno 1 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno1[0,0]
            Py2 = contorno1[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2, theta2_P2, theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
            
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(can_puntos):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == can_puntos - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
            
            #AHORA SI DIBUJAR CONTORNOS
            #CONTORNO 1
            for i in range(len(contorno1)):
                theta1,theta2,theta3 = self.CI(contorno1[i][0],contorno1[i][1],self.abajo)
                MTH = self.CD(theta1,theta2,theta3) 
                self.mover_servos(theta1,theta2,theta3)
                if i == len(contorno1) - 1: 
                    #Guardar ultimas coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                    self.pzInicial = self.abajo

            #Puntos iniciales para Contorno 2 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno2[0,0]
            Py2 = contorno2[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2,theta2_P2,theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
            
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(can_puntos):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == can_puntos - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
            
            #CONTORNO 2
            for i in range(len(contorno2)):
                theta1,theta2,theta3 = self.CI(contorno2[i][0],contorno2[i][1],self.abajo)
                MTH = self.CD(theta1,theta2,theta3) 
                self.mover_servos(theta1,theta2,theta3)
                #Ultima Iteracion
                if i == len(contorno2) - 1: 
                    #Guardar ultimas coordenadas
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
            # COMTORMO #1
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno1 = np.array([[(punto[0][0]/100)-15, ((punto[0][1]*-1+ofset)/100)-5] for punto in contornos[0]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno1 = np.vstack([contorno1[0::puntos], contorno1[-1]])

            # COMTORMO #2
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno2 = np.array([[(punto[0][0]/100)-15, ((punto[0][1]*-1+ofset)/100)-5] for punto in contornos[1]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno2 = np.vstack([contorno2[0::puntos], contorno2[-1]])

            #Puntos iniciales para Contorno 1 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno1[0,0]
            Py2 = contorno1[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2,theta2_P2,theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
            
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(len(can_puntos)):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == len(can_puntos) - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)

            #AHORA SI DIBUJAR CONTORNOS
            #CONTORNO 1
            for i in range(len(contorno1)):
                theta1,theta2,theta3 = self.CI(contorno1[i][0],contorno1[i][1],self.abajo)
                MTH = self.CD(theta1,theta2,theta3) 
                self.mover_servos(theta1,theta2,theta3)
                if i == len(contorno1) - 1: 
                    #Guardar ultimas coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                    self.pzInicial = self.abajo

            #Puntos iniciales para Contorno 2 (Cremallera)
            Px1 = self.pxInicial
            Py1 = self.pyInicial
            Pz1 = self.arrriba_cor
            theta1_P1,theta2_P1,theta3_P1 = self.CI(Px1,Py1,Pz1)

            Px2 = contorno2[0,0]
            Py2 = contorno2[0,1]
            Pz2 = self.arrriba_cor
            theta1_P2,theta2_P2,theta3_P2 = self.CI(Px2,Py2,Pz2)

            theta1P1_P2 = np.linspace(theta1_P1,theta1_P2,can_puntos)
            theta2P1_P2 = np.linspace(theta2_P1,theta2_P2,can_puntos)
            
            # Subir Cremallera
            MTH = self.CD(theta1P1_P2[0],theta2P1_P2[0],theta3_P1) 
            self.mover_servos(theta1P1_P2[0],theta2P1_P2[0],theta3_P1)

            for i in range(len(can_puntos)):
                MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],theta3_P1) 
                self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],theta3_P1)
                if i == len(can_puntos) - 1:
                    # Bajar Cremallera
                    MTH = self.CD(theta1P1_P2[i],theta2P1_P2[i],self.abajo)
                    self.mover_servos(theta1P1_P2[i],theta2P1_P2[i],self.abajo)

            #CONTORNO 2
            for i in range(len(contorno2)):
                theta1,theta2,theta3 = self.CI(contorno2[i][0],contorno2[i][1],self.abajo)
                MTH = self.CD(theta1,theta2,theta3) 
                self.mover_servos(theta1,theta2,theta3)
                #Ultima Iteracion
                if i == len(contorno2) - 1: 
                    #Guardar ultimas coordenadas
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                    self.pzInicial = self.abajo
                    
    #Cinematica Directa (Angulos a Coordenadas)
    def CD(self,theta1,theta2,theta_cre):
        theta_cre = math.degrees(theta_cre)
        d3 = theta_cre/50 # Convertir theta_cre en un movimeinto lineal
        
        q = np.array([theta1,theta2,d3])

        robot = SerialLink([
            RevoluteDH(d=0, alpha=0, a=self.l1, offset=0),
            RevoluteDH(d=0, alpha=0, a=self.l2, offset=0),
            PrismaticDH(theta=0, a=0, alpha=np.pi, offset=0)
        ], name=self.nombre)   
        # Visualizar el robot, con sus limites 
        robot.plot(q, limits=[-25, 25, -25, 25, -3, 3])
        
        MTH = robot.fkine(q)
        return MTH
    
    #Cinematica Inversa (Coordenadas a Angulos)
    def CI(self,px,py,pz):
        h1 = 5
        l3 = 5
        
        # Theta2
        b = np.sqrt(px**2 + py**2)
        cos_theta2 = (b**2-self.l2**2-self.l1**2)/(2*self.l2*self.l1)
        sen_theta2 = np.sqrt(1 - cos_theta2**2)
        theta2 = np.arctan2(sen_theta2, cos_theta2)
        # print(f'Theta2 = {np.degrees(theta2):.3f} grados')
        
        # Theta1
        alpha = np.arctan2(py,px)
        phi = np.arctan2(self.l2 * sen_theta2, self.l1 + self.l2 * cos_theta2)
        # Calcular theta1
        theta1 = alpha - phi
        theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1 #Otra forma de hacer el if
        # print(f'Theta1 = {np.degrees(theta1):.3f} grados')
        
        # d3
        d3 = -1 * (h1 - l3 - pz)
        theta_cre = d3 * 50
        # print(f'Theta3 = {theta_cre:.3f} grados')
        theta_cre = math.radians(theta_cre)
        
        #Retorno
        return theta1,theta2,theta_cre