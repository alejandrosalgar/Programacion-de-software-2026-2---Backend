import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Sucursal(Base):
    __tablename__ = "sucursales"

    id_sucursal: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(100))
    direccion: Mapped[str] = mapped_column(String(200))
    ciudad: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(30))
    id_usuario_creacion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_edicion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __str__(self) -> str:
        return (
            f"Sucursal(id_sucursal={self.id_sucursal}, nombre={self.nombre}, "
            f"direccion={self.direccion}, ciudad={self.ciudad}, telefono={self.telefono})"
        )
