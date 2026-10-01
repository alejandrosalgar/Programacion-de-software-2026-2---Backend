import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Cuota(Base):
    __tablename__ = "cuotas"

    id_cuota: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_prestamo: Mapped[uuid.UUID]
    valor: Mapped[float] = mapped_column(Float)
    numero_cuota: Mapped[int]
    fecha_vencimiento: Mapped[date] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
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
            f"Cuota(id_cuota={self.id_cuota}, id_prestamo={self.id_prestamo}, "
            f"numero_cuota={self.numero_cuota}, valor={self.valor}, "
            f"estado={self.estado}, fecha_vencimiento={self.fecha_vencimiento})"
        )
