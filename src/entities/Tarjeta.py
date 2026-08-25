import uuid
from datetime import datetime, date
from uuid import UUID

class Tarjeta:
    def __init__(
        self,
        id_cuenta: UUID,
        numero_tarjeta: str,
        tipo_tarjeta: str,
        fecha_emision: date,
        fecha_vencimiento: date,
        cvv: str,
        limite_credito: float,
        estado: str,
        id_usuario_creacion: UUID,
        id_usuario_edicion: UUID,
        fecha_creacion: datetime,
        fecha_edicion: datetime,
    ):
        self.id_tarjeta: UUID = uuid.uuid4()
        self.id_cuenta: UUID = id_cuenta
        self.numero_tarjeta: str = numero_tarjeta
        self.tipo_tarjeta: str = tipo_tarjeta
        self.fecha_emision: date = fecha_emision
        self.fecha_vencimiento: date = fecha_vencimiento
        self.cvv: str = cvv
        self.limite_credito: float = limite_credito
        self.estado: str = estado
        self.id_usuario_creacion: UUID = id_usuario_creacion
        self.id_usuario_edicion: UUID = id_usuario_edicion
        self.fecha_creacion: datetime = fecha_creacion
        self.fecha_edicion: datetime = fecha_edicion

    def get_id_tarjeta(self) -> UUID:
        return self.id_tarjeta

    def get_id_cuenta(self) -> UUID:
        return self.id_cuenta

    def set_id_cuenta(self, id_cuenta: UUID) -> None:
        self.id_cuenta = id_cuenta

    def get_numero_tarjeta(self) -> str:
        return self.numero_tarjeta

    def set_numero_tarjeta(self, numero_tarjeta: str) -> None:
        self.numero_tarjeta = numero_tarjeta

    def get_tipo_tarjeta(self) -> str:
        return self.tipo_tarjeta

    def set_tipo_tarjeta(self, tipo_tarjeta: str) -> None:
        self.tipo_tarjeta = tipo_tarjeta

    def get_fecha_emision(self) -> date:
        return self.fecha_emision

    def set_fecha_emision(self, fecha_emision: date) -> None:
        self.fecha_emision = fecha_emision

    def get_fecha_vencimiento(self) -> date:
        return self.fecha_vencimiento

    def set_fecha_vencimiento(self, fecha_vencimiento: date) -> None:
        self.fecha_vencimiento = fecha_vencimiento

    def get_cvv(self) -> str:
        return self.cvv

    def set_cvv(self, cvv: str) -> None:
        self.cvv = cvv

    def get_limite_credito(self) -> float:
        return self.limite_credito

    def set_limite_credito(self, limite_credito: float) -> None:
        self.limite_credito = limite_credito

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

    def esta_vencida(self) -> bool:
        return date.today() > self.fecha_vencimiento

    def bloquear(self) -> None:
        self.estado = "Bloqueada"

    def activar(self) -> None:
        self.estado = "Activa"

    def tiene_cupo_disponible(self, monto: float) -> bool:
        if self.tipo_tarjeta.lower() != "credito":
            return True  
        return monto <= self.limite_credito

    def enmascarar_numero(self) -> str:
        return "**** **** **** " + self.numero_tarjeta[-4:]

    def registrar_edicion(self, id_usuario_edicion: UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()
