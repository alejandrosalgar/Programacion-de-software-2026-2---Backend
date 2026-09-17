import uuid
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Sede(Base):
    __tablename__ = "sede"

    id_sede: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(100))
    direccion: Mapped[str] = mapped_column(String(150))
    ciudad: Mapped[str] = mapped_column(String(80))
    telefono: Mapped[str] = mapped_column(String(20))

    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("usuarios.id_usuario")
    )
    id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[date] = mapped_column(default=date.today)
    fecha_edicion: Mapped[date | None] = mapped_column(nullable=True)

    def registrar_edicion(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = date.today()

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
