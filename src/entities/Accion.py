import uuid
from datetime import datetime, date
from uuid import UUID


class Accion:

    def __init__(
        self,
        id_usuario: UUID,
        tipo_accion: str,
        descripcion: str,
        ip_origen: str,
        resultado: str,
        fecha_accion: datetime,
    ):
        self.id_accion: UUID = uuid.uuid4()
        self.id_usuario: UUID = id_usuario
        self.tipo_accion: str = tipo_accion
        self.descripcion: str = descripcion
        self.ip_origen: str = ip_origen
        self.resultado: str = resultado
        self.fecha_accion: datetime = fecha_accion

    def get_id_accion(self) -> UUID:
        return self.id_accion

    def get_id_usuario(self) -> UUID:
        return self.id_usuario

    def get_tipo_accion(self) -> str:
        return self.tipo_accion

    def get_descripcion(self) -> str:
        return self.descripcion

    def get_fecha_accion(self) -> datetime:
        return self.fecha_accion

    def get_ip_origen(self) -> str:
        return self.ip_origen

    def get_resultado(self) -> str:
        return self.resultado

    def registrar_error(self, mensaje: str) -> None:
        self.resultado = "Error"
        self.descripcion = mensaje

    def fue_exitosa(self) -> bool:
        return self.resultado == "Exito"
