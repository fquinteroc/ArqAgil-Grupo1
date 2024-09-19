from flaskr import create_app  
from .modelos import db, Usuario
from flask_restful import Api
from .vistas import UsuarioVista


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(UsuarioVista, '/usuarios/<int:id>', '/usuarios')