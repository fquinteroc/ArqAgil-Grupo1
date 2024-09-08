from microservicio_generacion_reportes import create_app
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
contador_invocaciones = 0
contador_informes=0

class VistaInforme(Resource):
    def post(self):
        global contador_informes
        contador_informes = contador_informes +1
        #Traer el último id generado y validar que sea múltiplo de 5, para generar error en el reporte
        url = 'http://127.0.0.1:5000/informes'
        response = requests.get(url)
        estado ="OK"
        caida=False
        #data1 = response.json() 
        #print("longitud data1:",len(data1))
        #if data1.status_code != 404: #Validamos que no este vacía
        #    if len(data1)>0:
        #id = data1[-1].get("id","no encontrado")
        #print("Id:",id)
        if(contador_informes%5 == 0): estado="Error" #Se utiliza para indicar que hubo error en el reporte
        if(contador_informes%10 == 0):
            caida=True #Se utiliza para simular la caida cada 10 solicitudes
            estado ="caida"
        ahora = datetime.now()
        hora_actual = ahora.strftime("%H:%M:%S")
        # Los datos que enviarás en la petición POST
        data = {
            'nombre': fake.name() ,
            'descripcion': fake.text(),
            'fecha_creacion': '08/09/2024',
            'hora_creacion': hora_actual,
            'estado': estado
        }
        
        # Realiza la petición POST
        response = requests.post(url, json=data)
        
        if caida ==True:
            #Simular una caida de la ejecución del reporte cada 10 solicitudes de reportes 
            abort(400, description="Se ha producido al generar el reporte")
        else:
            # Verifica si la petición fue exitosa
            if response.status_code == 201:
                print("Informe creado exitosamente:", response.json())
                return "Informe creado exitosamente:"+estado
            else:
                print("Eror al crear informe:", response.status_code, response.text)
                return "Eror al crear informe:"
            

   
class VistaEstado(Resource):#Sirve para responder el estado de salud del servicio
    def get(self):
        global contador_invocaciones
        contador_invocaciones += 1
        print("contador:",contador_invocaciones)
        estado ="OK "+str(contador_invocaciones)
        #Cada 5 invocaciones el servicio similara una caida
        if (contador_invocaciones%5 !=0):
            return estado, 200
        else:
            abort(400, description="Se ha producido un error en la solicitud")

api.add_resource(VistaInforme, "/informe/generar")
api.add_resource(VistaEstado, "/informe/estado")




