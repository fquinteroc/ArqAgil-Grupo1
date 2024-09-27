import random
import string
import threading
import time
import requests

from flask import Flask
from datetime import datetime
from faker import Faker

app = Flask(__name__)

def crear_usuario_aleatorio():
    fake = Faker()
    nombre = fake.name()
    user = nombre.split()[0].lower()
    email = f"{user}@gmail.com"
    password = "1qaz!QAZ"

    data = {
        "nombre": nombre,
        "email": email,
        "password": password
    }

    response = requests.post("http://127.0.0.1:5000/signup", json=data)
    response.raise_for_status()

    print(f"Usuario {email} creado con éxito.")
    return {"nombre":nombre,"email": email, "password": password}

def obtener_token(usuario):
    data = {
        "email": usuario["email"],
        "password": usuario["password"]
    }

    response = requests.post("http://127.0.0.1:5000/login", json=data) #Pasar al microservicio autorizador
    response.raise_for_status()

    token = response.json()["access_token"]
    print(f"Token para {usuario['email']} obtenido con éxito.")
    return token

def validar_token(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://127.0.0.1:5002/autorizar-informe", headers=headers)
    if response.status_code == 200:
        print("Token válido.")
    else:
        print("Token inválido.")
    response.raise_for_status()
    return response

def certificar_componente(usuario):
    data = {"usuario": usuario}
    try:
        response = requests.post("http://127.0.0.1:5003/certificador/autorizar", json=data)
        response.raise_for_status()  # Esto lanzará una excepción si el código de estado es 4xx o 5xx
        print("Componente certificado.")
        return {"error": 200, "message": "Componente certificado correctamente"}  # Éxito
    except requests.exceptions.HTTPError as e:
        if response.status_code == 422:
            print("Componente NO Certificado.")
            return {"error": 422, "message": "Componente no certificado"}
        else:
            print("Error al certificar componente:", response.status_code)
            return {"error": response.status_code, "message": "Error al certificar componente"}  # Manejo de otros errores
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return {"error": 500, "message": "Error en la solicitud"}  # Maneja error de solicitud

def registrar_anomalia(data):
    url = "http://127.0.0.1:5004/detector/intruso"
    try:
        response = requests.post(url, json=data)
    except requests.exceptions.RequestException as intruso_e:
        print(getHora_actual(), "Error al reportar intruso:", str(intruso_e))
    response.raise_for_status()
    return response

def getHora_actual():
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M:%S")
    return hora_actual

def getfecha_actual():
    ahora = datetime.now()
    fecha_actual = ahora.strftime("%d/%m/%Y")
    return fecha_actual


def simulador_servicio_externo():
    #Creamos 5 usuarios aleatorios
    usuarios = [crear_usuario_aleatorio() for _ in range(10)]    
    cont = 0
    nombre_microservicio=""
    estado =""
    while cont<100:
        try:
            cont += 1
            print("\n\nContador:",cont)
            #Seleccionamos un usuario aleatoriamente de la lista creada
            usuario = random.choice(usuarios)
            usuario_tem = usuario.copy()
            #if(cont%7==0): #Cada 7 usuarios intentando logearse se equivoque en el password
            #     usuario_tem['password']="x"
            print("Iniciando simulación con usuario:", usuario["nombre"], "Para generar el reporte de facturación")
            print("==========================================================================================")
            print("1. Aplicando táctica de seguridad -> Resistir ataques - Auntentificar actores (palabras claves)...")
            try:
                token = obtener_token(usuario_tem)
                #Cada 3 usuarios alteramos el token
                print("2. Aplicando táctica de seguridad - Resistir ataques - Autorizar actores (Microservicio Autorizador)...")
                if(cont%3==0):
                  token += 'x'
                try:
                    validar_token(token)
                    print(f"El token del usuario {usuario['email']} es válido. Puede proceder a generar el reporte de facturación.")
                    print("3. Aplicando táctica de seguridad - Resistir ataques - Autentificar actores (Microservicio Certificador)...")
                    #Llamar a certificador
                    response = requests.post("http://127.0.0.1:5003/certificador/autorizar", json={"usuario": usuario["nombre"]})
                    response.raise_for_status()
                    # Llamamos al microservicio de generar informe, para generar el reporte de facturación
                    headers = {"Authorization": f"Bearer {token}"} 
                    response = requests.post("http://127.0.0.1:5001/informe/generar",headers=headers)
                    response.raise_for_status()
                    print(getHora_actual(),"El reporte se genero con normalidad")
                        
                except requests.exceptions.RequestException as e: #En caso no se valido correctamente
                    if response.status_code == 403:
                        print("4. Aplicando táctica de seguridad - Detectar ataques - Detectar intruciones (Microservicio detector_intruso)...")
                        print(getHora_actual(),"Se detecto un intruso:", str(e))#Registrar en la BD
                        nombre_microservicio = "Microservicio detector intruso"
                        estado ="Intruso"
                    elif (response.status_code == 422):
                        print(getHora_actual(),"El componente no paso la certificación")
                        nombre_microservicio ="Microservicio certificador"
                        estado ="Sin certificación"
                    else:
                        print(getHora_actual(),f"El token del usuario {usuario['email']} es inválido.")
                        nombre_microservicio ="Microservicio autorizador"
                        estado ="Posible Intruso"
                    data = {
                        "servicio": nombre_microservicio,
                        "mensaje":str(e),
                        "fecha":getfecha_actual(),
                        "hora":getHora_actual(),
                        "estado":estado
                    }
                    registrar_anomalia(data)
            except requests.exceptions.RequestException as e:
                print(getHora_actual(),"Error al obtener token:", str(e))
        #except requests.exceptions.RequestException as e:
        #    print(getHora_actual(), f"HTTP error occurido: {response.status_code}, {str(e)}")
        except Exception as e:  # Captura cualquier otra excepción que no sea de requests
            print(getHora_actual(), f"Error inesperado: {str(e)}")
        time.sleep(2)

# Continuar con el servidor Flask
@app.route("/")
def index():
    return "Aplicación ejecutándose"

if __name__ == "__main__":
    simulador_servicio_externo()