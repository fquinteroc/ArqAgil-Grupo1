from microservicio_monitoreo import create_app
from flask_restful import Resource, Api
from flask import  jsonify, request
import requests

app = create_app('default')
app_context = app.app_context()
app_context.push()


api = Api(app)

class VistaMonitoreo(Resource):
    def get(self):
        #Consultar el estado de salud del microservicio generar_reporte
        url = 'http://127.0.0.1:5001/informe/estado'
        response = requests.get(url)

        # Verifica si la petición fue exitosa
        if response.status_code == 200:
            print("Generar_reporte ok:", response.json())
            #Verificamos si el reporte se genero correctamente
            url = 'http://127.0.0.1:5001/informe/estado'
            response = requests.get(url)
            return "Microservicio generar reporte OK"
        else:
            print("Eror al crear informe:", response.status_code, response.text)
            return "Se detecto la Falla en el microservicio GenerarReporte:",response.status_code, response.text

class VistaDetectarFalla(Resource):
    def get(self):
        try:
            url = 'http://127.0.0.1:5001/informe/estado'
            # Intentando llamar a un servicio externo
            
            response = requests.get(url)

            # Si hay una respuesta con error, manejarlo aquí
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            # Interceptar cualquier tipo de error de red o HTTP
            return jsonify({"error": "Error al comunicarse con el servicio externo", "detalles": str(e)}), 503

api.add_resource(VistaMonitoreo, "/monitoreoEstado")
api.add_resource(VistaDetectarFalla, "/monitoreoFalla")

if __name__ == "__main__":
    app.run(debug=True)






