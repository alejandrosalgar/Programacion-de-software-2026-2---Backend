import uuid
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Accion(Base):
    """
    Registro de auditoría de las acciones/eventos ejecutados por un usuario
    en el sistema (ej.: inicio de sesión, creación de tarjeta, edición de cuenta).
    """

    __tablename__ = "accion"

    id_accion: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id_usuario"))

    tipo_accion: Mapped[str] = mapped_column(
        String(50)
    )  # p.ej. "Login", "CrearTarjeta"
    descripcion: Mapped[str] = mapped_column(String(255), default="")
    ip_origen: Mapped[str | None] = mapped_column(String(45), nullable=True)
    resultado: Mapped[str] = mapped_column(
        String(20), default="Exito"
    )  # "Exito" / "Error"
    fecha_accion: Mapped[date] = mapped_column(default=date.today)

    # ---- Métodos de negocio conservados del primer parcial ----

    def registrar_error(self, mensaje: str) -> None:
        self.resultado = "Error"
        self.descripcion = mensaje

    def fue_exitosa(self) -> bool:
        return self.resultado == "Exito"
