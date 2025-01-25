import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from interfaz import Ui_MainWindow
from clase_robot import Robot, CanvasGrafica, Camara
from PyQt5.QtGui import QPixmap, QImage

# Crear la aplicación y el widget
app = QApplication(sys.argv)
Form = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(Form)

# Crear las instancias de CanvasGrafica
grafica_robot_nombre = CanvasGrafica(opcion=1,parent=Form)
grafica_robot_camara = CanvasGrafica(opcion=1,parent=Form)
grafica_camara = CanvasGrafica(opcion=2,parent=Form)
# Toca colocar el Qlabel para la camara
grafica_camara = QLabel()

# Ajustar tamaño y envia imagen
grafica_camara.setFixedSize(300, 300)
pixmap = QPixmap("imagenes/camara.png")
grafica_camara.setPixmap(pixmap)
grafica_camara.setScaledContents(True)

# Añadir los canvases a los layouts correspondientes
ui.verticalLayout_grafica.addWidget(grafica_robot_nombre)
ui.layaout_grafica_camara.addWidget(grafica_robot_camara)
ui.layout_camara.addWidget(grafica_camara)

# Inicializar la clase Camara y pasarle el QLabel como argumento
camara = Camara(grafica_camara)

# Crear una instancia de Robot 
robot_scara = Robot(
    nombre="Hacker", 
    l1=10, 
    l2=10, 
    pxInicial=20, 
    pyInicial=0, 
    pzInicial=0, 
    grafica_robot_nombre=grafica_robot_nombre, 
    grafica_robot_camara=grafica_robot_camara
)

# Definir una función que llame a robot_scara.palabra con los caracteres
def enviar_palabra():
    palabra = ui.txt_nombre.toPlainText()
    robot_scara.palabra(palabra)

# Función para cerrar la aplicación
def cerrar_aplicacion():
    QApplication.quit()
    
# Función para maximizar la ventana
def maximizar_ventana():
    Form.showMaximized()

# Función para minimizar la ventana
def minimizar_ventana():
    Form.showMinimized()

# Función para restaurar la ventana
def restaurar_ventana():
    Form.showNormal()

def cambiar_pagina(index):
    print(f"Índice seleccionado: {index}, Texto de la sección: {ui.toolBox.itemText(index)}")
    if ui.toolBox.itemText(index) == "Nombre":
        ui.stackedWidget.setCurrentIndex(0)
    elif ui.toolBox.itemText(index) == "Camara":
        ui.stackedWidget.setCurrentIndex(1)
    else:
        print("Sección no reconocida.")

# Funcion para poder cambiar la pagina, depediendo que escoja
ui.toolBox.currentChanged.connect(cambiar_pagina)

ui.aceptar_Nombre.clicked.connect(enviar_palabra)
ui.Iniciar_Camara.clicked.connect(camara.inicializar_camara)
ui.Detener_Camara.clicked.connect(camara.detener_camara)
ui.Tomar_Foto.clicked.connect(camara.capturar_imagen)
ui.Contornos.clicked.connect(camara.contorno)
ui.Realizar_Dibujo.clicked.connect(robot_scara.imagen_camara)

# Conectar los botones de control de ventana
ui.btn_cerrar.clicked.connect(cerrar_aplicacion)
ui.btn_maximizar.clicked.connect(maximizar_ventana)
ui.btn_minimizar.clicked.connect(minimizar_ventana)
ui.btn_restaurar.clicked.connect(restaurar_ventana)

# Mostrar el widget y ejecutar la aplicación
Form.show()
sys.exit(app.exec_())

