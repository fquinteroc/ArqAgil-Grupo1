import threading
import time
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

def monitor_servicio_externo():
    while True:
        try:
            # Intentar llamar al servicio externo
            response = requests.post("http://127.0.0.1:5001/informe/generar")
            response.raise_for_status()
            ahora = datetime.now()
            hora_actual = ahora.strftime("%H:%M:%S")
            print(hora_actual,"El servicio está activo")
        except requests.exceptions.RequestException as e:
            ahora = datetime.now()
            hora_actual = ahora.strftime("%H:%M:%S")
            # Aquí puedes realizar alguna acción en caso de fallo, como enviar un email o registrar el error
            print(hora_actual,"El servicio está caído:", str(e))#Registrar en la BD
            #crear JSON
            url = "http://127.0.0.1:5003/notificacion/falla"
            # Los datos que enviarás en la petición POST
            data = {
                "servicio": "Microservicio generador de reporte",
                "mensaje":str(e),
                "fecha_notificacion":"08/09/2024",
                "hora_notificacion":hora_actual,
                "estado":"ok"
            }
            
            # Realiza la petición POST
            response = requests.post(url, json=data)
            response.raise_for_status()
        # Esperar 30 segundos antes de volver a verificar
        time.sleep(1)

# Iniciar el monitoreo en segundo plano
monitoring_thread = threading.Thread(target=monitor_servicio_externo)
monitoring_thread.daemon = True
monitoring_thread.start()

# Continuar con el servidor Flask
@app.route("/")
def index():
    return "Aplicación ejecutándose"

if __name__ == "__main__":
    app.run(debug=True)