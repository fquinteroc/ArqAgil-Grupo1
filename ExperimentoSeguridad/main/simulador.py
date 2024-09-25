import threading
import time
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

def simulador_servicio_externo():
    while True:
        try:
            # Llamamos al microservicio de generar informe, para generar el reporte de facturación
            response = requests.post("http://127.0.0.1:5001/informe/generar")
            response.raise_for_status()
            ahora = datetime.now()
            hora_actual = ahora.strftime("%H:%M:%S")
            print(hora_actual,"El reporte se genero con normalidad")
        except requests.exceptions.RequestException as e:
            ahora = datetime.now()
            hora_actual = ahora.strftime("%H:%M:%S")
            # Como al generar el reporte nos devolvió error, validaresmo si se trata de un posible intruso
            if response.status_code == 403:
                print(hora_actual,"Se detecto un intruso:", str(e))#Registrar en la BD
                #crear JSON
                url = "http://127.0.0.1:5003/detector/intruso"
                data = {
                    "servicio": "Microservicio generador de reporte",
                    "mensaje":str(e),
                    "fecha":"25/09/2024",
                    "hora":hora_actual,
                    "estado":"Posible intruso"
                }
                response = requests.post(url, json=data)
                response.raise_for_status()
            else:
                print(hora_actual, f"HTTP error occurred: {response.status_code}, {str(e)}")
        # Esperar 1 segundos antes de volver simular la generación de otro reporte
        time.sleep(1)

# Iniciar el simulador en segundo plano
monitoring_thread = threading.Thread(target=simulador_servicio_externo)
monitoring_thread.daemon = True
monitoring_thread.start()

# Continuar con el servidor Flask
@app.route("/")
def index():
    return "Aplicación ejecutándose"

if __name__ == "__main__":
    app.run(debug=True)