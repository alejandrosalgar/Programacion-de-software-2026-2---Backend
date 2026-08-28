from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Cuota:
    id_prestamo: UUID
    valor: float
    numero_cuota: int
    fecha_vencimiento: date
    estado: str = "pendiente"
    id_cuota: UUID = field(default_factory=uuid4)
    id_usuario_creacion: UUID | None = None
    fecha_creacion: date = field(default_factory=date.today)
    id_usuario_edicion: UUID | None = None
    fecha_edicion: date | None = None

    def __str__(self) -> str:
        return (
            f"Cuota(id_cuota={self.id_cuota}, id_prestamo={self.id_prestamo}, "
            f"numero_cuota={self.numero_cuota}, valor={self.valor}, "
            f"estado={self.estado}, fecha_vencimiento={self.fecha_vencimiento})"
        )
