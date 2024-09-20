from flaskr import create_app
from flaskr.vistas.vistas import VistaNotificacionFalla
from .modelos import db, Cliente
from .modelos import ClienteSchema
from flask_restful import Api
from .vistas import VistaCliente, VistaProducto, VistaPQR, VistaInformes

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

from .modelos import db, Cliente, ClienteSchema

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

# Crear la instancia de la API
api = Api(app)

# Agregar recursos (vistas) a la API
api.add_resource(VistaCliente, '/clientes')
api.add_resource(VistaProducto, '/productos')
api.add_resource(VistaPQR, '/pqrs')
api.add_resource(VistaInformes, '/informes')
api.add_resource(VistaNotificacionFalla,'/notificacionfalla')