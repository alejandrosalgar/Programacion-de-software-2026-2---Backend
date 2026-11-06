import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Empleado(Base):
    __tablename__ = "empleados"

    id_empleado: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id_usuario"))
    id_sucursal: Mapped[uuid.UUID] = mapped_column(ForeignKey("sucursales.id_sucursal"))
    cargo: Mapped[str] = mapped_column(String(100))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
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
            f"Empleado(id_empleado={self.id_empleado}, id_usuario={self.id_usuario}, "
            f"id_sucursal={self.id_sucursal}, cargo={self.cargo}, activo={self.activo})"
        )
