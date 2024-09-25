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
contador_invocaciones = 0
contador_informes=0

class VistaReporteFacturacion(Resource):
    def post(self):
        global contador_informes
        contador_informes = contador_informes +1
        #Traer el último id generado y validar que sea múltiplo de 5, para generar error en el reporte
        url = 'http://127.0.0.1:5000/informes'
        estado ="OK"
        anomalia=False
        if(contador_informes%10 == 0):
            anomalia=True #Se utiliza para simular una anomalía en el comportamiento del usuario cada 10 solicitudes
            estado ="Anomalía"
        ahora = datetime.now()
        hora_actual = ahora.strftime("%H:%M:%S")
        # Los datos que enviarás en la petición POST
        data = {
            'nombre': fake.name() ,
            'descripcion': fake.text(),
            'fecha_creacion': '25/09/2024',
            'hora_creacion': hora_actual,
            'estado': estado
        }
        
        # Realiza la petición POST
        response = requests.post(url, json=data)
        
        if anomalia ==True:
            #Indicar el consumidor del microservicio sobre un posible ataque al sistema 
            abort(403, description="Posible ataque al sistema a la hora de generar el reporte de facturación")
        else:
            # Verifica si la petición fue exitosa
            if response.status_code == 201:
                print("Informe creado exitosamente:", response.json())
                return "Informe creado exitosamente:"+estado
            else:
                print("Eror al crear informe:", response.status_code, response.text)
                return "Eror al crear informe:"
            
api.add_resource(VistaReporteFacturacion, "/informe/generar")





