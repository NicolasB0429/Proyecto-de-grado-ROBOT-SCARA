from picamera2 import Picamera2
from PIL import Image
import time

def capture_image():
    picam2 = Picamera2()  # Crear una instancia de Picamera2
    picam2.start()  # Iniciar la c�mara

    # Esperar a que la c�mara se inicialice
    time.sleep(2)

    # Capturar una imagen
    image_array = picam2.capture_array()

    # Convertir el array a una imagen
    image = Image.fromarray(image_array)

    # Convertir la imagen a RGB antes de guardarla
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Guardar la imagen en formato JPEG
    image.save('pruebas/Camara/imagenes/image.jpg')

    picam2.stop()  # Detener la c�mara

if __name__ == "__main__":
    capture_image()
