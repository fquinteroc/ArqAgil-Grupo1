from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    contrasena = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre, correo, contrasena, rol):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol

    def __repr__(self):
        return '<Usuario %r>' % self.nombre