from microservicio_generacion_informes import create_app
from flask_restful import Resource, Api, abort
from flask import Flask, request
import requests
from faker import Faker
from datetime import datetime

app = create_app('default')
app_context = app.app_context()
app_context.push()


api = Api(app)
fake = Faker()

class VistaCertificadorTest(Resource):
    def post(self):
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
            
api.add_resource(VistaCertificadorTest, "/certificador/test")