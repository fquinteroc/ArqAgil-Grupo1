import requests
import random
import string

def crear_usuario_aleatorio():
    nombre = ''.join(random.choices(string.ascii_lowercase, k=8))
    email = f"{nombre}@gmail.com"
    password = "1qaz!QAZ"

    data = {
        "nombre": nombre,
        "email": email,
        "password": password
    }

    response = requests.post("http://127.0.0.1:5000/signup", json=data)
    response.raise_for_status()

    print(f"Usuario {email} creado con éxito.")
    return {"email": email, "password": password}

def obtener_token(usuario):
    data = {
        "email": usuario["email"],
        "password": usuario["password"]
    }

    response = requests.post("http://127.0.0.1:5000/login", json=data)
    response.raise_for_status()

    token = response.json()["access_token"]
    print(f"Token para {usuario['email']} obtenido con éxito.")
    return token

def validar_token(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get("http://127.0.0.1:5002/autorizar-informe", headers=headers)
    
    if response.status_code == 200:
        print("Token válido.")
        return True
    else:
        print("Token inválido.")
        return False

def prueba_creacion_y_validacion_usuarios():
    usuarios = [crear_usuario_aleatorio() for _ in range(5)]
    
    tokens = []
    for usuario in usuarios:
        try:
            token = obtener_token(usuario)
            tokens.append(token)
        except requests.exceptions.RequestException as e:
            print(f"Error al procesar el usuario {usuario['email']}: {str(e)}")

    # Dañar el token de uno de los usuarios
    if tokens:
        print("Dañando el token del segundo usuario...")
        tokens[1] += 'x'  # Agregar una letra extra al final del token

    for i, token in enumerate(tokens):
        try:
            if validar_token(token):
                print(f"El token del usuario {usuarios[i]['email']} es válido. Puede proceder a generar informes.")
            else:
                print(f"El token del usuario {usuarios[i]['email']} es inválido.")
        except requests.exceptions.RequestException as e:
            print(f"Error al validar el token del usuario {usuarios[i]['email']}: {str(e)}")

if __name__ == "__main__":
    prueba_creacion_y_validacion_usuarios()
