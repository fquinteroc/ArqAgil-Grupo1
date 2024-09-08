from microservicio_monitoreo import create_app
from flask_restful import Resource, reqparse, Api
from flask import  jsonify, request
import requests

app = create_app('default')
app_context = app.app_context()
app_context.push()


api = Api(app)

class VistaNotificacionFalla(Resource):
    def post(self):
        datos = request.get_json()
        print("datos:",datos)
        #Consultar el estado de salud del microservicio generar_reporte
        url = 'http://127.0.0.1:5000/notificacionfalla'
        response = requests.post(url, json=datos)

api.add_resource(VistaNotificacionFalla, "/notificacion/falla")