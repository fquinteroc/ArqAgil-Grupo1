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

class VistaGeneracionInforme(Resource):
    #Generamos un reporte en función PQR
    #Debemos guardar en una tabla el número de veces que se consulta, y simular falla cada 5
    def get(self, cliente_id=None):
        #Leer de la BD el número de informe generado
        # nro  = NroInforme()
        #if (nro mod 5==0): simular la falla
        #else: continuar con el reporte
        if cliente_id:
            pqr = PQR.query.get_or_404(cliente_id)
            return pqr_schema.dump(pqr), 200
        else:
            pqrs = PQR.query.all()
            return pqrs_schema.dump(pqrs), 200

class VistaInformes(Resource):
    def get(self, informe_id=None):
        if informe_id:
            informe = Informe.query.get_or_404(informe_id)
            return informe_schema.dump(informe), 200
        else:
            informes = Informe.query.all()
            return informes_schema.dump(informes), 200

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
        return cliente_schema.dump(informe), 200

    def delete(self, informe_id):
        informe = Informe.query.get_or_404(informe_id)
        db.session.delete(informe)
        db.session.commit()
        return '', 204
          
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
