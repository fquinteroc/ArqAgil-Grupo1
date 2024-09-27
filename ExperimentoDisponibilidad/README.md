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
```

4. Si no tienes `virtualenv` instalado, puedes hacerlo ejecutando:
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
cd ExperimentoDisponibilidad/flaskr/
```
7.2 Ejecuta la aplicación Flask en el puerto 5000:
```bash
flask run -p 5000
```
8. Ejecutar el microservicio de generación de reportes

8.1 En una nueva terminal, ve a la carpeta del microservicio de generación de reportes:
```bash
cd ExperimentoDisponibilidad/microservicio_generacion_reportes/
```
8.2 Ejecuta este microservicio en el puerto 5001:
```bash
flask run -p 5001
```
9. Ejecutar el microservicio de monitoreo

9.1 Ve a la carpeta del microservicio de monitoreo:
```bash
cd ExperimentoDisponibilidad/microservicio_monitoreo/
```
9.2 Ejecuta este microservicio en el puerto 5002:
```bash
flask run -p 5002
```
10. Ejecutar el microservicio de notificación de fallas

10.1 Ve a la carpeta del microservicio de notificación de fallas:
```bash
cd ExperimentoDisponibilidad/microservicio_notificacion_falla/
```
10.2 Ejecuta este microservicio en el puerto 5003:
```bash
flask run -p 5003
```
11. Simular errores en el microservicio de monitoreo

11.1 Ve nuevamente a la carpeta del microservicio de monitoreo:
```bash
cd ExperimentoDisponibilidad/microservicio_monitoreo/
```
11.2 Ejecuta el script `monitoreo.py`, que contiene las iteraciones para generar errores:
```bash
py monitoreo.py
```
## Notas adicionales
- Asegúrate de que todos los puertos (5000, 5001, 5002, 5003) estén disponibles antes de ejecutar las aplicaciones.
- Si experimentas algún problema, verifica que todas las dependencias se instalaron correctamente y que el entorno virtual esté activado.
