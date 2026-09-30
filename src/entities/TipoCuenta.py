import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base

if TYPE_CHECKING:
    from entities.cuenta import (
        Cuenta,
    )


class TipoCuenta(Base):
    __tablename__ = "tipo_cuenta"

    id_tipo_cuenta: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    nombre: Mapped[str] = mapped_column(String(80), unique=True)
    descripcion: Mapped[str] = mapped_column(String(255), default="")
    tasa_interes: Mapped[float] = mapped_column()
    monto_minimo_apertura: Mapped[float] = mapped_column()
    requiere_mantenimiento: Mapped[bool] = mapped_column(default=False)
    estado: Mapped[str] = mapped_column(String(20), default="Activo")

    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("usuarios.id_usuario")
    )
    id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[date] = mapped_column(default=date.today)
    fecha_edicion: Mapped[date | None] = mapped_column(nullable=True)
    cuentas: Mapped[list["Cuenta"]] = relationship(back_populates="tipo_cuenta")

    def calcular_interes(self, saldo: float) -> float:
        return saldo * (self.tasa_interes / 100)

    def cumple_monto_minimo(self, saldo: float) -> bool:
        return saldo >= self.monto_minimo_apertura

    def activar(self) -> None:
        self.estado = "Activo"

    def desactivar(self) -> None:
        self.estado = "Inactivo"

    def registrar_edicion(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = date.today()
