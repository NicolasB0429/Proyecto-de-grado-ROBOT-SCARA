<h1 align="center">DESARROLLO DE UN ROBOT SCARA CON RASPBERRY PI PARA EL PROCESAMIENTO DE IMAGENES Y MODELO DE RED NEURONAL 🤖🦾<br> 
Version 3.0 ✨<br>
Nicolas Barrera y Angie Mancipe<br>
Universidad Ecci 🏫</h1><br>

## Descripción 📝
<div style="text-align: justify;">
Se desarrolla el brazo robótico SCARA de 3 grados de libertad (3GDL), programado en Python. El sistema cuenta con 4 modos de operación: el primero ejecuta una trayectoria basada en las coordenadas proporcionadas por el usuario, el segundo traza el área de trabajo del robot, el tercero permite escribir caracteres alfanuméricos, y el último realiza un reconocimiento de imágenes en tiempo real para el trazo de contornos detectados. Además, ofrece la opción de reemplazar la Cinemática Inversa por un modelo de Red Neuronal.
</div>

## Materiales 🛠️
1. Raspberry Pi 4 8GB RAM
2. Camara raspberry Pi de 5MP
3. Controlador de servomotores PCA9685
4. Dos servomotores TD8120MG de 20Kg
5. Un servomotor Mg90

## Software y Librerías 💻
### Software Utilizado
- **Python** `3.x`: Lenguaje de programación para controlar el brazo robótico SCARA.
- **Raspberry Pi OS**: Sistema operativo utilizado en la Raspberry Pi.

### Librerías de Python
- **NumPy**: Operaciones numéricas y cálculos matriciales.
- **Math**: Módulo integrado de Python que proporciona funciones matemáticas básicas.
- **Matplotlib**: Gráficas de trayectorias y áreas de trabajo del robot.
- **OpenCV**: Reconocimiento de imágenes en tiempo real.
- **PyQt5**: Interfaz gráfica.
- **roboticstoolbox**: Librería para la simulación y control de robots, que facilita el desarrollo de algoritmos de robótica.
- **adafruit_servokit**: Librería para controlar servomotores utilizando el kit de Adafruit, ideal para aplicaciones de robótica.
- **scikit-learn**: Entrenamiento de la Red Neuronal.

### Herramientas y Plataformas
- **Google Colab**: Plataforma en la nube utilizada para desarrollar y entrenar el modelo de red neuronal.

## Planos del Proyecto 📐
Este proyecto incluye archivos de diseño CAD que representan los planos del brazo robótico SCARA.

## Resultados ☑️
