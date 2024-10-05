<h1 align="center">✨ ROBOT SCARA ✨<br>
Proyecto de Grado 🎓<br>
Nicolas Barrera y Angie Mancipe 👨‍🎓👩‍🎓<br>
Universidad Ecci 🏫</h1><br>

## Descripción del Proyecto 📝
<div style="text-align: justify;">
Este repositorio contiene el código y la documentación para el desarrollo de un brazo robótico Scara, realizado como parte del proyecto de grado de Ingeniería Mecatrónica. El objetivo de este proyecto es diseñar e implementar un brazo robótico que pueda realizar tareas de seguimiento de trayectorias, espacio de trabajo del robot, escritura de caracteres alfanumericos y trazo de contornos de imágenes.
</div>

## Motivación 🔥 
Nuestro interés en la robótica y la automatización nace de una profunda curiosidad por cómo funcionan los sistemas mecánicos y electrónicos. Este proyecto representa una oportunidad emocionante para **explorar y aplicar conceptos de robótica** en un contexto práctico, lo que me permitirá **desarrollar habilidades técnicas** y **resolver desafíos reales**.

El diseño de un **sistema autónomo** no solo nos permite aprender sobre **control de motores** y **programación**, sino que también nos brinda la satisfacción de ver cómo nuestras ideas toman forma y se convierten en algo tangible. Cada etapa del proyecto, desde la planificación hasta la ejecución, está impulsada por el deseo de innovar y crear soluciones que puedan tener un impacto positivo.

## Etapas del Proyecto 🔍
El desarrollo del brazo robótico SCARA se llevó a cabo en varias etapas, cada una de las cuales está representada en una rama diferente en este repositorio. A continuación se describen las etapas:

### Etapa 1: Brazo Robótico con MATLAB y Arduino Uno
- **Descripción**: "Desarrollo inicial del control del brazo robótico utilizando MATLAB para simular y validar la cinemática, y Arduino Uno para controlar el movimiento de los actuadores (servomotores).
- **Rama**: `matlab-arduino`
- **Enlace**: [Ver rama MATLAB y Arduino Uno](https://github.com/NicolasB0429/Proyecto-de-grado-ROBOT-SCARA/tree/matlab-arduino?tab=readme-ov-file)

### Etapa 2: Integración de PIC18F46K22
- **Descripción**: Se realiza el cambio del Arduino Uno por el microcontrolador PIC18F46K22 en la implementación del control del brazo robótico, integrando el controlador de servomotores PCA9685 y una pantalla LCD 16x2 para la visualización de los ángulos del robot. Además realizando un reconocimiento de contornos con imagenes preestablecidas.
- **Rama**: `matlab-pic`
- **Enlace**: [Ver rama Matlab y PIC18F46K22](https://github.com/NicolasB0429/Proyecto-de-grado-ROBOT-SCARA/tree/matlab-pic?tab=readme-ov-file)

### Etapa 3: Brazo Robótico con Raspberry Pi 4
- **Descripción**: Adaptación de todo el sistema utilizando la Raspberry Pi, lo que permite su integración con tecnologías vanguardistas y la incorporación de reconocimiento de contornos de imágenes en tiempo real.
- **Rama**: `raspberry-only`
- **Enlace**: [Ver rama Raspberry Pi](https://github.com/NicolasB0429/Proyecto-de-grado-ROBOT-SCARA/tree/raspberry-only)

### Etapa 4: Integración de STM32F746ZG
- **Descripción**: Se realiza el cambio de los servomotores por motores DC, donde se incorpora el microcontrolador STM32F746ZG y se realiza un control cascada para sus articulaciones.
- **Rama**: `raspberry-stm`
- **Enlace**: [Ver rama Raspberry y STM32F746ZG](https://github.com/usuario/brazo-robotico-scara/tree/stm32-version)






