from flask_restful import Resource
from ..modelos import db, Usuario
from flask import request

class UsuarioVista(Resource):
    def get(self, id):
        usuario = Usuario.query.get(id)
        return usuario.to_dict()

    def post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass