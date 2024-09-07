from flask_restful import Resource, reqparse
from ..modelos import db, Cliente, Producto, PQR, Informe, Monitoreo, NotificacionFalla, LogBaseDatos, \
                    ClienteSchema, ProductoSchema, PQRSchema, InformeSchema, MonitoreoSchema, NotificacionFallaSchema, LogBaseDatosSchema

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)
pqr_schema = PQRSchema()
pqrs_schema = PQRSchema(many=True)
informe_schema = InformeSchema()
informes_schema = InformeSchema(many=True)


class VistaCliente(Resource):
    def get(self, cliente_id=None):
        if cliente_id:
            cliente = Cliente.query.get_or_404(cliente_id)
            return cliente_schema.dump(cliente), 200
        else:
            clientes = Cliente.query.all()
            return clientes_schema.dump(clientes), 200

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

    def delete(self, cliente_id):
        cliente = Cliente.query.get_or_404(cliente_id)
        db.session.delete(cliente)
        db.session.commit()
        return '', 204


class VistaProducto(Resource):
    def get(self, producto_id=None):
        if producto_id:
            producto = Producto.query.get_or_404(producto_id)
            return producto_schema.dump(producto), 200
        else:
            productos = Producto.query.all()
            return productos_schema.dump(productos), 200

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

    def delete(self, producto_id):
        producto = Producto.query.get_or_404(producto_id)
        db.session.delete(producto)
        db.session.commit()
        return '', 204


class VistaPQR(Resource):
    def get(self, pqr_id=None):
        if pqr_id:
            pqr = PQR.query.get_or_404(pqr_id)
            return pqr_schema.dump(pqr), 200
        else:
            pqrs = PQR.query.all()
            return pqrs_schema.dump(pqrs), 200

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

    def delete(self, pqr_id):
        pqr = PQR.query.get_or_404(pqr_id)
        db.session.delete(pqr)
        db.session.commit()
        return '', 204
