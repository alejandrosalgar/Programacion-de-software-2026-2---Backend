import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Cuenta(Base):
    __tablename__ = "cuentas"

    id_cuenta: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    numero_cuenta: Mapped[str] = mapped_column(String(20), unique=True)
    id_tipo_cuenta: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id_usuario"))
    saldo: Mapped[float] = mapped_column(Float, default=0.0)
    estado: Mapped[str] = mapped_column(String(20), default="Activa")
    fecha_apertura: Mapped[date] = mapped_column(Date, default=date.today)
    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("usuarios.id_usuario")
    )
    id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    fecha_edicion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __str__(self) -> str:
        return (
            f"ID: {self.id_cuenta}\n"
            f"Numero: {self.numero_cuenta}\n"
            f"Titular: {self.id_usuario}\n"
            f"Tipo de cuenta: {self.id_tipo_cuenta or 'N/A'}\n"
            f"Saldo: {self.saldo}\n"
            f"Estado: {self.estado}\n"
            f"Fecha apertura: {self.fecha_apertura}"
        )
