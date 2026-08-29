from datetime import date
from uuid import UUID

from entities.sucursal import Sucursal

sucursales: list[Sucursal] = []


def _buscar_por_id(id_sucursal: UUID) -> Sucursal | None:
    for sucursal in sucursales:
        if sucursal.id_sucursal == id_sucursal:
            return sucursal
    return None


def crear(
    nombre: str,
    direccion: str,
    ciudad: str,
    telefono: str,
    id_usuario_creacion: UUID | None = None,
) -> Sucursal:
    sucursal = Sucursal(
        nombre=nombre,
        direccion=direccion,
        ciudad=ciudad,
        telefono=telefono,
        id_usuario_creacion=id_usuario_creacion,
    )
    sucursales.append(sucursal)
    return sucursal


def eliminar(id_sucursal: UUID) -> bool:
    sucursal = _buscar_por_id(id_sucursal)
    if sucursal is None:
        return False
    sucursales.remove(sucursal)
    return True


def actualizar(
    id_sucursal: UUID,
    id_usuario_edicion: UUID,
    nombre: str | None = None,
    direccion: str | None = None,
    ciudad: str | None = None,
    telefono: str | None = None,
) -> Sucursal | None:
    sucursal = _buscar_por_id(id_sucursal)
    if sucursal is None:
        return None

    if nombre:
        sucursal.nombre = nombre
    if direccion:
        sucursal.direccion = direccion
    if ciudad:
        sucursal.ciudad = ciudad
    if telefono:
        sucursal.telefono = telefono

    sucursal.id_usuario_edicion = id_usuario_edicion
    sucursal.fecha_edicion = date.today()
    return sucursal


def obtener(id_sucursal: UUID) -> Sucursal | None:
    return _buscar_por_id(id_sucursal)


def listar() -> list[Sucursal]:
    return list(sucursales)
