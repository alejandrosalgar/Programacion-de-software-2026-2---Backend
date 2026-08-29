from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Empleado:
    id_usuario: UUID
    id_sucursal: UUID
    cargo: str
    id_empleado: UUID = field(default_factory=uuid4)
    activo: bool = True
    id_usuario_creacion: UUID | None = None
    fecha_creacion: date = field(default_factory=date.today)
    id_usuario_edicion: UUID | None = None
    fecha_edicion: date | None = None

    def __str__(self) -> str:
        return (
            f"Empleado(id_empleado={self.id_empleado}, id_usuario={self.id_usuario}, "
            f"id_sucursal={self.id_sucursal}, cargo={self.cargo}, activo={self.activo})"
        )
