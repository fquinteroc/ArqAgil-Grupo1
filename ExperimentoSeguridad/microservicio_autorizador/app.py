from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_restful import Api, Resource
import requests 

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'grupo_5'

jwt = JWTManager(app)
api = Api(app)

class AutorizarGeneracionInforme(Resource):
    def get(self):
        try:
            verify_jwt_in_request()
            identidad = get_jwt_identity()

            try:
                response = requests.post(
                    'http://127.0.0.1:5000/guardar-historial-tokens',
                    json={
                        "token": request.headers.get('Authorization'),
                        "resultado": "Éxito",
                        "identidad": identidad,
                        "descripcion": "Token validado correctamente."
                    }
                )
                if response.status_code != 201:
                    return {"message": "Error al guardar el historial de validación"}, 500
            except Exception as e:
                return {"message": f"Error al comunicarse con el microservicio de historial: {str(e)}"}, 500

            return {"message": "Autorización exitosa", "identity": identidad}, 200

        except Exception as e:
            try:
                response = requests.post(
                    'http://127.0.0.1:5000/guardar-historial-tokens',
                    json={
                        "token": request.headers.get('Authorization'),
                        "resultado": "Fallo",
                        "descripcion": f"Error: {str(e)}"
                    }
                )
                if response.status_code != 201:
                    return {"message": "Error al guardar el historial de fallo"}, 500
            except Exception as e_hist:
                return {"message": f"Error al comunicarse con el microservicio de historial: {str(e_hist)}"}, 500

            return {"message": f"Autorización fallida. Token inválido o ausente. Error: {str(e)}"}, 401

# Añade la vista al API
api.add_resource(AutorizarGeneracionInforme, '/autorizar-informe')

if __name__ == '__main__':
    app.run(debug=True)
