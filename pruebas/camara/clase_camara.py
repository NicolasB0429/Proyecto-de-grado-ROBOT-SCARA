import os
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from picamera2 import Picamera2 # Maneja la camara
from PIL import Image # Maneja imagenes y realiza conversiones
import numpy as np
from PyQt5 import QtCore

class Camara(QWidget):
    def __init__(self, camara_label, parent=None):
        super().__init__(parent)

        # qlabel para visualizar la camara
        self.preview_label = camara_label
        
      # Inicializar la cï¿½mara sin iniciar aï¿½n
        self.picam2 = Picamera2()

        # Intentar detener la cï¿½mara si estï¿½ en funcionamiento
        if self.picam2.camera_config:
            self.picam2.stop()

        # Obtener los modos de la cï¿½mara
        config = self.picam2.create_still_configuration(main={"size": self.picam2.sensor_resolution})

        # Configurar la cï¿½mara con la mï¿½xima resoluciï¿½n disponible
        self.picam2.configure(config)

        # Iniciar la cï¿½mara despuï¿½s de configurarla
        self.picam2.start()

        # Configuraracion temporsizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(10)  # Actualizar cada medio segundo

        # Verificar que la cartea de imagenes exista
        if not os.path.exists("pruebas/Camara/imagenes"):
            os.makedirs("pruebas/Camara/imagenes")

    def update_preview(self): #actualizacion_vista previa
        # Capturar la imagen 
        image_array = self.picam2.capture_array()

        # Convertir el array a una imagen de PIL
        image = Image.fromarray(image_array)

        # Convertir la imagen a RGB antes de convertir a QImage
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convertir la imagen a un formato compatible con QImage
        data = np.array(image)
        q_image = QImage(data, data.shape[1], data.shape[0], data.strides[0], QImage.Format_RGB888)

        # Convertir QImage a QPixmap para mostrar en el QLabel
        qt_image = QPixmap.fromImage(q_image)

        # Redimensionar el QPixmap al tamaï¿½o del QLabel
        qt_image = qt_image.scaled(self.preview_label.width(), self.preview_label.height(), QtCore.Qt.KeepAspectRatio)

        # Mostrar la imagen redimensionada en el QLabel
        self.preview_label.setPixmap(qt_image)


    def capture_image(self):
        # Capturar una imagen
        image_array = self.picam2.capture_array()

        # Convertir el array a una imagen de PIL
        image = Image.fromarray(image_array)

        # Convertir la imagen a RGB antes de guardarla
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Guardar la imagen en formato JPEG
        image.save('pruebas/Camara/imagenes/captura.jpg')

        # print("Imagen capturada y guardada en 'pruebas/Camara/imagenes/image.jpg'")
    
    def __del__(self):
        # Detener la cï¿½mara cuando el objeto sea destruido
        self.picam2.stop()
