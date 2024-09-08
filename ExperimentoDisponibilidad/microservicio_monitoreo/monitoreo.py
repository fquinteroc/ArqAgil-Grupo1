import threading
import time
import requests
from flask import Flask

app = Flask(__name__)

def monitor_servicio_externo():
    while True:
        try:
            # Intentar llamar al servicio externo
            response = requests.get("http://127.0.0.1:5001/informe/generar")
            response.raise_for_status()
            print("El servicio está activo")
        except requests.exceptions.RequestException as e:
            # Aquí puedes realizar alguna acción en caso de fallo, como enviar un email o registrar el error
            print("El servicio está caído:", str(e))#Registrar en la BD
        
        # Esperar 30 segundos antes de volver a verificar
        time.sleep(30)

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