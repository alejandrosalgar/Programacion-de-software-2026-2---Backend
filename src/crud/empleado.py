from datetime import date
from uuid import UUID

from entities.empleado import Empleado

empleados: list[Empleado] = []


def _buscar_por_id(id_empleado: UUID) -> Empleado | None:
    for empleado in empleados:
        if empleado.id_empleado == id_empleado:
            return empleado
    return None


def crear(
    id_usuario: UUID,
    id_sucursal: UUID,
    cargo: str,
    activo: bool = True,
    id_usuario_creacion: UUID | None = None,
) -> Empleado:
    empleado = Empleado(
        id_usuario=id_usuario,
        id_sucursal=id_sucursal,
        cargo=cargo,
        activo=activo,
        id_usuario_creacion=id_usuario_creacion,
    )
    empleados.append(empleado)
    return empleado


def eliminar(id_empleado: UUID) -> bool:
    empleado = _buscar_por_id(id_empleado)
    if empleado is None:
        return False
    empleados.remove(empleado)
    return True


def actualizar(
    id_empleado: UUID,
    id_usuario_edicion: UUID,
    id_usuario: UUID | None = None,
    id_sucursal: UUID | None = None,
    cargo: str | None = None,
    activo: bool | None = None,
) -> Empleado | None:
    empleado = _buscar_por_id(id_empleado)
    if empleado is None:
        return None

    if id_usuario is not None:
        empleado.id_usuario = id_usuario
    if id_sucursal is not None:
        empleado.id_sucursal = id_sucursal
    if cargo is not None:
        empleado.cargo = cargo
    if activo is not None:
        empleado.activo = activo

    empleado.id_usuario_edicion = id_usuario_edicion
    empleado.fecha_edicion = date.today()
    return empleado


def obtener(id_empleado: UUID) -> Empleado | None:
    return _buscar_por_id(id_empleado)


def listar() -> list[Empleado]:
    return list(empleados)
