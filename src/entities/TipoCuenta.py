import uuid
from datetime import datetime, date
from uuid import UUID


class TipoCuenta:

    def __init__(
        self,
        nombre: str,
        descripcion: str,
        tasa_interes: float,
        monto_minimo_apertura: float,
        requiere_mantenimiento: bool,
        estado: str,
        id_usuario_creacion: UUID,
        id_usuario_edicion: UUID,
        fecha_creacion: datetime,
        fecha_edicion: datetime,
    ):
        self.id_tipo_cuenta: UUID = uuid.uuid4()
        self.nombre: str = nombre
        self.descripcion: str = descripcion
        self.tasa_interes: float = tasa_interes
        self.monto_minimo_apertura: float = monto_minimo_apertura
        self.requiere_mantenimiento: bool = requiere_mantenimiento
        self.estado: str = estado
        self.id_usuario_creacion: UUID = id_usuario_creacion
        self.id_usuario_edicion: UUID = id_usuario_edicion
        self.fecha_creacion: datetime = fecha_creacion
        self.fecha_edicion: datetime = fecha_edicion

    def get_id_tipo_cuenta(self) -> UUID:
        return self.id_tipo_cuenta

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, nombre: str) -> None:
        self.nombre = nombre

    def get_descripcion(self) -> str:
        return self.descripcion

    def set_descripcion(self, descripcion: str) -> None:
        self.descripcion = descripcion

    def get_tasa_interes(self) -> float:
        return self.tasa_interes

    def set_tasa_interes(self, tasa_interes: float) -> None:
        self.tasa_interes = tasa_interes

    def get_monto_minimo_apertura(self) -> float:
        return self.monto_minimo_apertura

    def set_monto_minimo_apertura(self, monto_minimo_apertura: float) -> None:
        self.monto_minimo_apertura = monto_minimo_apertura

    def get_requiere_mantenimiento(self) -> bool:
        return self.requiere_mantenimiento

    def set_requiere_mantenimiento(self, requiere_mantenimiento: bool) -> None:
        self.requiere_mantenimiento = requiere_mantenimiento

    def get_estado(self) -> str:
        return self.estado

    def get_id_usuario_creacion(self) -> UUID:
        return self.id_usuario_creacion

    def get_id_usuario_edicion(self) -> UUID:
        return self.id_usuario_edicion

    def get_fecha_creacion(self) -> datetime:
        return self.fecha_creacion

    def get_fecha_edicion(self) -> datetime:
        return self.fecha_edicion

    def calcular_interes(self, saldo: float) -> float:
        return saldo * (self.tasa_interes / 100)

    def cumple_monto_minimo(self, saldo: float) -> bool:
        return saldo >= self.monto_minimo_apertura

    def activar(self) -> None:
        self.estado = "Activo"

    def desactivar(self) -> None:
        self.estado = "Inactivo"

    def registrar_edicion(self, id_usuario_edicion: UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()
