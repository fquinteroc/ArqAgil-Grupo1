# Experimentación 1 - Disponibilidad
Este proyecto consiste en la ejecución de varios microservicios utilizando Flask. Cada microservicio tiene su propia funcionalidad y se ejecuta en diferentes puertos. A continuación se detallan los pasos para configurar y ejecutar los microservicios.

## Pasos de instalación
1. Clona el repositorio en tu máquina local con el siguiente comando:

```bash
git clone https://github.com/fquinteroc/ArqAgil-Grupo5.git
```

2. Ve al directorio del proyecto:
```bash
cd Grupo5-Arquitectura
cd ExperimentoSeguridad
```

4. Estando en la carpeta de seguridad, si no tienes `virtualenv` instalado, puedes hacerlo ejecutando:
```bash
py -m pip install --user virtualenv
```

5. Crea un entorno virtual en el proyecto:
```bash
py -m venv venv
```
6. Activa el entorno virtual que acabas de crear:
```bash
.\venv\Scripts\activate
```
7. Instala las librerías necesarias utilizando el archivo `requirements.txt`:
```bash
py -m pip install -r requirements.txt
```
## Ejecución de la aplicación y microservicios

7. Ejecutar la aplicación principal

7.1 Ve a la carpeta de la aplicación principal:
```bash
cd ExperimentoSeguridad/flaskr/
```
7.2 Ejecuta la aplicación Flask en el puerto 5000:
```bash
flask run -p 5000
```
8. Ejecutar el microservicio Generador de informes

8.1 En una nueva terminal, ve a la carpeta del microservicio generador de informes:
```bash
cd ExperimentoSeguridad/microservicio_generacion_informes/
```
8.2 Ejecuta este microservicio en el puerto 5001:
```bash
flask run -p 5001
```
9. Ejecutar el microservicio Autorizador

9.1 Ve a la carpeta del microservicio autorizador:
```bash
cd ExperimentoSeguridad/microservicio_autorizador/
```
9.2 Ejecuta este microservicio en el puerto 5002:
```bash
flask run -p 5002
```
10. Ejecutar el microservicio certificador

10.1 Ve a la carpeta del microservicio certificador:
```bash
cd ExperimentoSeguridad/microservicio_certificador/
```
10.2 Ejecuta este microservicio en el puerto 5003:
```bash
flask run -p 5003
```
11. Ejecutar el microservicio detector de intruso

11.1 Ve a la carpeta del microservicio detector de intruso:
```bash
cd ExperimentoSeguridad/microservicio_detector_intruso/
```
10.2 Ejecuta este microservicio en el puerto 5004:
```bash
flask run -p 5004
```

12. Simulación

12 Ve ahora a la carpeta main:
```bash
cd ExperimentoSeguridad/main/
```
11.2 Ejecuta el script `simulador.py`, que contiene las iteraciones para generar errores, desde la creación de usuario hasta la generación de informes:
```bash
py simulador.py
```
## Notas adicionales
- Asegúrate de que todos los puertos (5000, 5001, 5002, 5003, 5004) estén disponibles antes de ejecutar las aplicaciones.
- Si experimentas algún problema, verifica que todas las dependencias se instalaron correctamente y que el entorno virtual esté activado.
