from clase_robot import Robot

# Crear una instancia de Robot 
Robot_2R = Robot(nombre="Hacker", l1=10, l2=10, pxInicial=20, pyInicial=0,pzInicial=0)

# Definir una funcion que llame a Robot_2R.coordenadas con los valores actuales de x e y
def enviar_coordenadas():
    x = 10.5
    y = 10
    Robot_2R.coordenadas(x, y)

# Definir una funcion que llame a Robot_2R.palabra con los caracteres
def enviar_palabra():
    print("Hola")
# COORDENADAS
enviar_coordenadas()
# ESPACIO DE TRABAJO
# ui.btn_2.clicked.connect(Robot_2R.esp_trabajo)
# # NOMBRE O CARACTERES
# ui.btn_3.clicked.connect(enviar_palabra)
# # IMAGENES
# ui.btn_4.clicked.connect(Robot_2R.imagenes(1))
# ui.btn_5.clicked.connect(Robot_2R.imagenes(2))
# ui.btn_6.clicked.connect(Robot_2R.imagenes(3))