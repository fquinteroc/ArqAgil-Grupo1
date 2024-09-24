from flask_restful import Resource, reqparse
from ..modelos import db, Cliente, Producto, PQR, Informe, Monitoreo, NotificacionFalla, LogBaseDatos, \
                    ClienteSchema, ProductoSchema, PQRSchema, InformeSchema, MonitoreoSchema, NotificacionFallaSchema, LogBaseDatosSchema
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)
pqr_schema = PQRSchema()
pqrs_schema = PQRSchema(many=True)
informe_schema = InformeSchema()
informes_schema = InformeSchema(many=True)
notificacion_schema = NotificacionFallaSchema()
notificaciones_schema = NotificacionFallaSchema(many=True)

class VistaSignUp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        # Verificar si el email ya existe
        if Cliente.query.filter_by(email=args['email']).first():
            return {"message": "El usuario con ese email ya existe"}, 400

        nuevo_cliente = Cliente(
            nombre=args['nombre'],
            email=args['email'],
            password=generate_password_hash(args['password'])
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return cliente_schema.dump(nuevo_cliente), 201


class VistaLogIn(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        cliente = Cliente.query.filter_by(email=args['email']).first()

        if not cliente or not check_password_hash(cliente.password, args['password']):
            return {"message": "Credenciales incorrectas"}, 401

        # Crear un token de acceso
        access_token = create_access_token(identity=cliente.id)
        return {"access_token": access_token}, 200


class VistaNotificacionFalla(Resource):
    @jwt_required()
    def get(self, notificacion_id=None):
        if notificacion_id:
            notificacion = NotificacionFalla.query.get_or_404(notificacion_id)
            return notificacion_schema.dump(notificacion), 200
        else:
            notificaciones = NotificacionFalla.query.all()
            return notificaciones_schema.dump(notificaciones), 200
        
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('servicio', type=str, required=True)
        parser.add_argument('mensaje', type=str, required=True)
        parser.add_argument('fecha_notificacion', type=str, required=False)
        parser.add_argument('hora_notificacion', type=str, required=False)
        parser.add_argument('estado', type=str, required=False)

        args = parser.parse_args()

        nueva_notificacion = NotificacionFalla(
            servicio=args['servicio'],
            mensaje=args['mensaje'],
            fecha_notificacion=args.get('fecha_notificacion'),
            hora_notificacion=args.get("hora_notificacion"),
            estado=args.get('estado'),
        )
        db.session.add(nueva_notificacion)
        db.session.commit()
        return notificacion_schema.dump(nueva_notificacion), 201


class VistaInformes(Resource):
    @jwt_required()
    def get(self, informe_id=None):
        if informe_id:
            informe = Informe.query.get_or_404(informe_id)
            return informe_schema.dump(informe), 200
        else:
            informes = Informe.query.all()
            return informes_schema.dump(informes), 200

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str, required=True)
        parser.add_argument('descripcion', type=str, required=True)
        parser.add_argument('fecha_creacion', type=str, required=False)
        parser.add_argument('hora_creacion', type=str, required=False)
        parser.add_argument('estado', type=str, required=False)

        args = parser.parse_args()

        nuevo_informe = Informe(
            nombre=args['nombre'],
            descripcion=args['descripcion'],
            fecha_creacion=args.get('fecha_creacion'),
            hora_creacion=args.get("hora_creacion"),
            estado=args.get('estado'),
        )
        db.session.add(nuevo_informe)
        db.session.commit()
        return informe_schema.dump(nuevo_informe), 201

    @jwt_required()
    def put(self, informe_id):
        informe = Informe.query.get_or_404(informe_id)
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str)
        parser.add_argument('descripcion', type=str)
        parser.add_argument('fecha_creacion', type=str)
        parser.add_argument('hora_creacion', type=str)
        parser.add_argument('estado', type=str)
        args = parser.parse_args()

        if args['nombre']:
            informe.nombre = args['nombre']
        if args['descripcion']:
            informe.descripcion = args['descripcion']
        if args['fecha_creacion']:
            informe.fecha_creacion = args['fecha_creacion']
        if args['hora_creacion']:
            informe.hora_creacion = args['hora_creacion']
        if args['estado']:
            informe.estado = args['estado']

        db.session.commit()
        return informe_schema.dump(informe), 200

    @jwt_required()
    def delete(self, informe_id):
        informe = Informe.query.get_or_404(informe_id)
        db.session.delete(informe)
        db.session.commit()
        return '', 204


class VistaCliente(Resource):
    @jwt_required()
    def get(self, cliente_id=None):
        if cliente_id:
            cliente = Cliente.query.get_or_404(cliente_id)
            return cliente_schema.dump(cliente), 200
        else:
            clientes = Cliente.query.all()
            return clientes_schema.dump(clientes), 200

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('telefono', type=str, required=False)
        parser.add_argument('direccion', type=str, required=False)
        args = parser.parse_args()

        nuevo_cliente = Cliente(
            nombre=args['nombre'],
            email=args['email'],
            telefono=args.get('telefono'),
            direccion=args.get('direccion')
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return cliente_schema.dump(nuevo_cliente), 201

    @jwt_required()
    def put(self, cliente_id):
        cliente = Cliente.query.get_or_404(cliente_id)
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('telefono', type=str)
        parser.add_argument('direccion', type=str)
        args = parser.parse_args()

        if args['nombre']:
            cliente.nombre = args['nombre']
        if args['email']:
            cliente.email = args['email']
        if args['telefono']:
            cliente.telefono = args['telefono']
        if args['direccion']:
            cliente.direccion = args['direccion']

        db.session.commit()
        return cliente_schema.dump(cliente), 200

    @jwt_required()
    def delete(self, cliente_id):
        cliente = Cliente.query.get_or_404(cliente_id)
        db.session.delete(cliente)
        db.session.commit()
        return '', 204


class VistaProducto(Resource):
    @jwt_required()
    def get(self, producto_id=None):
        if producto_id:
            producto = Producto.query.get_or_404(producto_id)
            return producto_schema.dump(producto), 200
        else:
            productos = Producto.query.all()
            return productos_schema.dump(productos), 200

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str, required=True)
        parser.add_argument('tipo', type=str, required=True)
        args = parser.parse_args()

        nuevo_producto = Producto(
            nombre=args['nombre'],
            tipo=args['tipo']
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return producto_schema.dump(nuevo_producto), 201

    @jwt_required()
    def put(self, producto_id):
        producto = Producto.query.get_or_404(producto_id)
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str)
        parser.add_argument('tipo', type=str)
        args = parser.parse_args()

        if args['nombre']:
            producto.nombre = args['nombre']
        if args['tipo']:
            producto.tipo = args['tipo']

        db.session.commit()
        return producto_schema.dump(producto), 200

    @jwt_required()
    def delete(self, producto_id):
        producto = Producto.query.get_or_404(producto_id)
        db.session.delete(producto)
        db.session.commit()
        return '', 204


class VistaPQR(Resource):
    @jwt_required()
    def get(self, pqr_id=None):
        if pqr_id:
            pqr = PQR.query.get_or_404(pqr_id)
            return pqr_schema.dump(pqr), 200
        else:
            pqrs = PQR.query.all()
            return pqrs_schema.dump(pqrs), 200

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fecha', type=str, required=True)
        parser.add_argument('problema', type=str, required=True)
        parser.add_argument('posible_solucion', type=str, required=False)
        parser.add_argument('tiempo_limite', type=str, required=True)
        parser.add_argument('cliente_id', type=int, required=True)
        args = parser.parse_args()

        nueva_pqr = PQR(
            fecha=args['fecha'],
            problema=args['problema'],
            posible_solucion=args.get('posible_solucion'),
            tiempo_limite=args['tiempo_limite'],
            cliente_id=args['cliente_id']
        )
        db.session.add(nueva_pqr)
        db.session.commit()
        return pqr_schema.dump(nueva_pqr), 201

    @jwt_required()
    def put(self, pqr_id):
        pqr = PQR.query.get_or_404(pqr_id)
        parser = reqparse.RequestParser()
        parser.add_argument('problema', type=str)
        parser.add_argument('posible_solucion', type=str)
        parser.add_argument('fecha_solucion', type=str)
        args = parser.parse_args()

        if args['problema']:
            pqr.problema = args['problema']
        if args['posible_solucion']:
            pqr.posible_solucion = args['posible_solucion']
        if args['fecha_solucion']:
            pqr.fecha_solucion = args['fecha_solucion']

        db.session.commit()
        return pqr_schema.dump(pqr), 200

    @jwt_required()
    def delete(self, pqr_id):
        pqr = PQR.query.get_or_404(pqr_id)
        db.session.delete(pqr)
        db.session.commit()
        return '', 204