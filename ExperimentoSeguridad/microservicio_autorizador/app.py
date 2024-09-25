from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_restful import Api, Resource

app = Flask(__name__)

# Configuración del JWT
app.config['JWT_SECRET_KEY'] = 'grupo_5'

jwt = JWTManager(app)
api = Api(app)

class AutorizarGeneracionInforme(Resource):
    def get(self):
        try:
            verify_jwt_in_request()  # Verifica si el token está presente en la petición
            identidad = get_jwt_identity()
            return {"message": "Autorización exitosa", "identity": identidad}, 200

        except Exception as e:
            return {"message": f"Autorización fallida. Token inválido o ausente. Error: {str(e)}"}, 401

api.add_resource(AutorizarGeneracionInforme, '/autorizar-informe')

if __name__ == '__main__':
    app.run(debug=True)
