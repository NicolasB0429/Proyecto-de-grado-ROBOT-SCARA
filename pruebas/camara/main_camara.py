import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from interfaz_camara import Ui_MainWindow
from clase_camara import Camara
from PyQt5 import QtCore


def foto():
    camara_instance.capture_image()

# interfaz
app = QApplication(sys.argv)
Form = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(Form)

# Intancia camara
camara_instance = Camara(ui.camara)
# Autoescala de la camara
ui.camara.setScaledContents(True)
# Boton foto
ui.btn_foto.clicked.connect(foto)


Form.show()
sys.exit(app.exec_())
