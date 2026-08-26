import uuid
from datetime import date


class Sede:
    def __init__(
        self,
        nombre: str,
        direccion: str,
        ciudad: str,
        telefono: str,
        id_usuario_creacion: uuid.UUID,
        id_sede: uuid.UUID | None = None,
        id_usuario_edicion: uuid.UUID | None = None,
        fecha_creacion: date | None = None,
        fecha_edicion: date | None = None,
    ):
        self.id_sede = id_sede if id_sede is not None else uuid.uuid4()
        self.nombre = nombre.strip()
        self.direccion = direccion.strip()
        self.ciudad = ciudad.strip()
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
            f"ID: {self.id_sede}\n"
            f"Nombre: {self.nombre}\n"
            f"Direccion: {self.direccion}\n"
            f"Ciudad: {self.ciudad}\n"
            f"Telefono: {self.telefono}\n"
            f"ID usuario creacion: {self.id_usuario_creacion}\n"
            f"ID usuario edicion: {id_edicion}\n"
            f"Fecha creacion: {self.fecha_creacion}\n"
            f"Fecha edicion: {fecha_edicion}"
        )
