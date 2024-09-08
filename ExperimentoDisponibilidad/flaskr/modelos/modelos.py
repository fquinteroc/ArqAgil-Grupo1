from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)

    pqrs = db.relationship('PQR', backref='cliente', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

class PQR(db.Model):
    __tablename__ = 'pqrs'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    problema = db.Column(db.String(500), nullable=False)
    posible_solucion = db.Column(db.String(500), nullable=True)
    tiempo_limite = db.Column(db.DateTime, nullable=False)
    fecha_solucion = db.Column(db.DateTime, nullable=True)
    hora_solucion = db.Column(db.Time, nullable=True)
    url_grabacion = db.Column(db.String(255), nullable=True)
    url_video = db.Column(db.String(255), nullable=True)
    url_imagenes = db.Column(db.String(255), nullable=True)
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

class Informe(db.Model):
    __tablename__ = 'informes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    fecha_creacion = db.Column(db.String(10), nullable=False)
    hora_creacion = db.Column(db.String(10), nullable=False)
    estado = db.Column(db.String(50), default='Generado')

    #cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    #pqr_id = db.Column(db.Integer, db.ForeignKey('pqrs.id'), nullable=True)

class Monitoreo(db.Model):
    __tablename__ = 'monitoreo'
    
    id = db.Column(db.Integer, primary_key=True)
    servicio = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    fecha_verificacion = db.Column(db.DateTime, nullable=False)

class NotificacionFalla(db.Model):
    __tablename__ = 'notificaciones_fallas'
    
    id = db.Column(db.Integer, primary_key=True)
    servicio = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.String(500), nullable=False)
    fecha_notificacion = db.Column(db.String(10), nullable=False)
    hora_notificacion = db.Column(db.String(10), nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')

class LogBaseDatos(db.Model):
    __tablename__ = 'logs_base_datos'
    
    id = db.Column(db.Integer, primary_key=True)
    tabla = db.Column(db.String(100), nullable=False)
    operacion = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)


# ESQUEMAS DE SERIALIZACIÓN
class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_relationships = True
        load_instance = True

    pqrs = Nested('PQRSchema', many=True)

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_relationships = True
        load_instance = True

class PQRSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PQR
        include_relationships = True
        load_instance = True

    cliente = Nested(ClienteSchema) 

class InformeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Informe
        include_relationships = True
        load_instance = True

    cliente = Nested(ClienteSchema)
    pqr = Nested(PQRSchema)

class MonitoreoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Monitoreo
        include_relationships = True
        load_instance = True

class NotificacionFallaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotificacionFalla
        include_relationships = True
        load_instance = True

class LogBaseDatosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LogBaseDatos
        include_relationships = True
        load_instance = True
