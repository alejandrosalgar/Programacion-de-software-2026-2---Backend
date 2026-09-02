import uuid
from datetime import date


class Beneficiario:
    def __init__(
        self,
        id_cliente: uuid.UUID,
        nombre_completo: str,
        parentesco: str,
        telefono: str,
        id_usuario_creacion: uuid.UUID,
        id_beneficiario: uuid.UUID | None = None,
        id_usuario_edicion: uuid.UUID | None = None,
        fecha_creacion: date | None = None,
        fecha_edicion: date | None = None,
    ):
        self.id_beneficiario = (
            id_beneficiario if id_beneficiario is not None else uuid.uuid4()
        )
        self.id_cliente = id_cliente
        self.nombre_completo = nombre_completo.strip()
        self.parentesco = parentesco.strip()
        self.telefono = telefono.strip()
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_creacion = (
            fecha_creacion if fecha_creacion is not None else date.today()
        )
        self.fecha_edicion = fecha_edicion

    def __str__(self) -> str:
        id_edicion = self.id_usuario_edicion if self.id_usuario_edicion else "N/A"
        fecha_edicion = self.fecha_edicion if self.fecha_edicion else "N/A"
        return (
            f"ID Beneficiario: {self.id_beneficiario}\n"
            f"ID Cliente: {self.id_cliente}\n"
            f"Nombre Completo: {self.nombre_completo}\n"
            f"Parentesco: {self.parentesco}\n"
            f"Telefono: {self.telefono}\n"
            f"ID usuario creacion: {self.id_usuario_creacion}\n"
            f"ID usuario edicion: {id_edicion}\n"
            f"Fecha creacion: {self.fecha_creacion}\n"
            f"Fecha edicion: {fecha_edicion}"
        )