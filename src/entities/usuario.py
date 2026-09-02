import uuid

from database.connection import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    primer_nombre: Mapped[str] = mapped_column(String(80))
    segundo_nombre: Mapped[str] = mapped_column(String(80), default="")
    primer_apellido: Mapped[str] = mapped_column(String(80))
    segundo_apellido: Mapped[str] = mapped_column(String(80), default="")
    nombre_usuario: Mapped[str] = mapped_column(String(80), unique=True)
    clave: Mapped[str] = mapped_column(String(255))
