from flaskr import create_app
from flaskr.modelos import db, Cliente, ClienteSchema
from flaskr.vistas import VistaCliente, VistaProducto, VistaPQR, VistaInformes, VistaNotificacionFalla, VistaSignUp, VistaLogIn
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = create_app('default')

with app.app_context():
    db.init_app(app)
    db.create_all()

api = Api(app)

api.add_resource(VistaCliente, '/clientes')
api.add_resource(VistaProducto, '/productos')
api.add_resource(VistaPQR, '/pqrs')
api.add_resource(VistaInformes, '/informes')
api.add_resource(VistaNotificacionFalla, '/notificacionfalla')
api.add_resource(VistaSignUp, '/signup')  # Vista de registro
api.add_resource(VistaLogIn, '/login')    # Vista de inicio de sesión

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
