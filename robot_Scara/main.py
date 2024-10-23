import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from interfaz import Ui_MainWindow
from clase_robot import Robot, CanvasGrafica

# Crear la aplicación y el widget
app = QApplication(sys.argv)
Form = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(Form)

# Crear las instancias de CanvasGrafica
canvas_grafica = CanvasGrafica(parent=Form)
canvas_robot = CanvasGrafica(parent=Form)

# Añadir los canvases a los layouts correspondientes
ui.verticalLayout_grafica.addWidget(canvas_grafica)
ui.verticalLayout_robot.addWidget(canvas_robot)

# Crear una instancia de Robot 
Robot_2R = Robot(
    nombre="Hacker", 
    l1=10, 
    l2=10, 
    pxInicial=20, 
    pyInicial=0, 
    pzInicial=0, 
    canvas_grafica=canvas_grafica, 
    canvas_robot=canvas_robot
)

# Definir una función que llame a Robot_2R.coordenadas con los valores actuales de x e y
def enviar_coordenadas():
    x_str = ui.coor_x.toPlainText()
    y_str = ui.coor_y.toPlainText()
    x_formateado = "{:.2f}".format(float(x_str))
    y_formateado = "{:.2f}".format(float(y_str))
    x = float(x_formateado)
    y = float(y_formateado)
    Robot_2R.coordenadas(x, y)
       
# Definir una función que llame a Robot_2R.palabra con los caracteres
def enviar_palabra():
    palabra = ui.txt_nombre.toPlainText()
    Robot_2R.palabra(palabra)

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

# COORDENADAS
ui.aceptar_coor.clicked.connect(enviar_coordenadas)
# ESPACIO DE TRABAJO
ui.aceptar_areatrabajo.clicked.connect(Robot_2R.esp_trabajo)
# NOMBRE O CARACTERES
ui.aceptar_Nombre.clicked.connect(enviar_palabra)
# IMAGENES
ui.hyundai.clicked.connect(lambda: Robot_2R.imagenes(1))
ui.chevrolet.clicked.connect(lambda: Robot_2R.imagenes(2))
ui.Tesla.clicked.connect(lambda: Robot_2R.imagenes(3))

# Conectar los botones de control de ventana
ui.btn_cerrar.clicked.connect(cerrar_aplicacion)
ui.btn_maximizar.clicked.connect(maximizar_ventana)
ui.btn_minimizar.clicked.connect(minimizar_ventana)
ui.btn_restaurar.clicked.connect(restaurar_ventana)

# Mostrar el widget y ejecutar la aplicación
Form.show()
sys.exit(app.exec_())
