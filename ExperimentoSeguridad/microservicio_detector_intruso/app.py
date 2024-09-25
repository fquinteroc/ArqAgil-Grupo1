#Cada vez que detecta una anomalía en el comportamiento del usuario lo registra en un log

from microservicio_detector_intruso import create_app
from flask_restful import Resource, reqparse, Api
from flask import  jsonify, request
import requests

app = create_app('default')
app_context = app.app_context()
app_context.push()


api = Api(app)

class VistaDetectorIntruso(Resource):
    def post(self):
        datos = request.get_json()
        print("datos:",datos)
        #Registrar el posible intruso
        url = 'http://127.0.0.1:5000/anomalias'
        response= requests.post(url, json=datos)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return response.status_code
api.add_resource(VistaDetectorIntruso, "/detector/intruso")