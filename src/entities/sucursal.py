from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Sucursal:
    nombre: str
    direccion: str
    ciudad: str
    telefono: str
    id_sucursal: UUID = field(default_factory=uuid4)
    id_usuario_creacion: UUID | None = None
    fecha_creacion: date = field(default_factory=date.today)
    id_usuario_edicion: UUID | None = None
    fecha_edicion: date | None = None

    def __str__(self) -> str:
        return (
            f"Sucursal(id_sucursal={self.id_sucursal}, nombre={self.nombre}, "
            f"direccion={self.direccion}, ciudad={self.ciudad}, telefono={self.telefono})"
        )
