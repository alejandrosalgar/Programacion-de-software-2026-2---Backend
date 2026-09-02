import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Tarjeta(Base):
    __tablename__ = "tarjetas"

    id_tarjeta: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_cuenta: Mapped[uuid.UUID] = mapped_column(ForeignKey("cuentas.id_cuenta"))
    numero_tarjeta: Mapped[str] = mapped_column(String(19), unique=True)
    tipo_tarjeta: Mapped[str] = mapped_column(String(20))
    fecha_emision: Mapped[date] = mapped_column(Date)
    fecha_vencimiento: Mapped[date] = mapped_column(Date)
    cvv: Mapped[str] = mapped_column(String(4))
    limite_credito: Mapped[float] = mapped_column(Float)
    estado: Mapped[str] = mapped_column(String(20))
    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("usuarios.id_usuario")
    )
    id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    fecha_edicion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

