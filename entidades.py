from datetime import datetime
from typing import Optional

class Cuenta:
    def __init__(self, id_cuenta: int, id_cliente: int, id_tipo_cuenta: int, 
                 id_usuario_creacion: int, id_usuario_edicion: Optional[int] = None, 
                 fecha_creacion: Optional[datetime] = None, fecha_edicion: Optional[datetime] = None):
        self.id_cuenta = id_cuenta
        self.id_cliente = id_cliente
        self.id_tipo_cuenta = id_tipo_cuenta
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_edicion = fecha_edicion

class Transaccion:
    def __init__(self, id_transaccion: int, id_cuenta: int, id_usuario: int, 
                 id_beneficiario: Optional[int], id_usuario_creacion: int, 
                 id_usuario_edicion: Optional[int] = None, 
                 fecha_creacion: Optional[datetime] = None, fecha_edicion: Optional[datetime] = None):
        self.id_transaccion = id_transaccion
        self.id_cuenta = id_cuenta
        self.id_usuario = id_usuario
        self.id_beneficiario = id_beneficiario
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_edicion = fecha_edicion

class Prestamo:
    def __init__(self, id_prestamo: int, id_cliente: int, 
                 id_usuario_creacion: int, id_usuario_edicion: Optional[int] = None, 
                 fecha_creacion: Optional[datetime] = None, fecha_edicion: Optional[datetime] = None):
        self.id_prestamo = id_prestamo
        self.id_cliente = id_cliente
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_edicion = fecha_edicion

class Beneficiario:
    def __init__(self, id_beneficiario: int, id_cliente: int, id_transaccion: Optional[int], 
                 id_usuario_creacion: int, id_usuario_edicion: Optional[int] = None, 
                 fecha_creacion: Optional[datetime] = None, fecha_edicion: Optional[datetime] = None):
        self.id_beneficiario = id_beneficiario
        self.id_cliente = id_cliente
        self.id_transaccion = id_transaccion
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_edicion = fecha_edicion