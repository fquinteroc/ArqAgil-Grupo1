import threading
import time
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

def simulador_servicio_externo():
    url = 'http://127.0.0.1:5000/certificador'

    # Realiza la petición POST
    response = requests.post(url, json={})

    # Verifica si la petición fue exitosa
    if response.status_code == 200:
        print("Certificador valida petición:", response.json())
        return "Certificador valida petición:"
    else:
        print("Certificador no autoriza:", response.status_code, response.text)
        return "Certificador no autoriza"

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