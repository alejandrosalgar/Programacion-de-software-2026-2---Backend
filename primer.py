from datetime import datetime


class Cuota:

    def __init__(self, id_cuota: int, id_prestamo: int, id_usuario_creacion: int):
        self.id_cuota = id_cuota
        self.id_prestamo = id_prestamo
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion = 0  # valor inicial por defecto
        self.fecha_creacion = datetime.now()
        self.fecha_edicion = datetime.now()

    def editar(self, id_usuario_edicion: int):
        """Actualiza los campos de edición con el usuario y la fecha actual."""
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()


class Sucursal:

    def __init__(self, id_sucursal: int, id_usuario_creacion: int):
        self.id_sucursal = id_sucursal
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion = 0  # valor inicial por defecto
        self.fecha_creacion = datetime.now()
        self.fecha_edicion = datetime.now()

    def editar(self, id_usuario_edicion: int):
        """Actualiza los campos de edición con el usuario y la fecha actual."""
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()


class Empleado:

    def __init__(
        self,
        id_empleado: int,
        id_usuario: int,
        id_sucursal: int,
        id_usuario_creacion: int,
    ):
        self.id_empleado = id_empleado
        self.id_usuario = id_usuario  # FK hacia Usuario
        self.id_sucursal = id_sucursal  # FK hacia Sucursal
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion = 0  # valor inicial por defecto
        self.fecha_creacion = datetime.now()
        self.fecha_edicion = datetime.now()

    def editar(self, id_usuario_edicion: int):
        """Actualiza los campos de edición con el usuario y la fecha actual."""
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()
