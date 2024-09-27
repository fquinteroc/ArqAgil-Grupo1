from microservicio_certificador import create_app
from flask_restful import Resource, Api, abort
from flask import Flask, request
import requests
from datetime import datetime

app = create_app('default')
app_context = app.app_context()
app_context.push()


api = Api(app)
contador_certificados = 0
class VistaCertificador(Resource):
    def post(self):
        global contador_certificados
        contador_certificados +=1
        certificar = True
        estado ="OK"
        resultado ="Firmado y validado correctamente"
        datos = request.get_json()
        print("datos de autorizador:",datos)
        if (contador_certificados%7==0):
            certificar = False
            estado ="Falló"
            resultado ="Componente no pasó la certificación"
        url = 'http://127.0.0.1:5000/certificador'
        data={
            "usuario" : datos["usuario"],
            "componente" :"Generador de informes",
            "resultado" : resultado,
            "fecha" : datetime.now().strftime("%d/%m/%Y"),
            "hora":datetime.now().strftime("%H:%M:%S"),
            "estado" : estado
        }
        print("Antes de response")
        response = requests.post(url, json=data)
        print("Response desde certificador:",response)
        if (certificar == True):
            print("Certificador ok")
            return response.status_code
        else :
            print("no certificado")
            #return  422
            abort(422, description="No certificado")
api.add_resource(VistaCertificador, "/certificador/autorizar")