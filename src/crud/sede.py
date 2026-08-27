from datetime import date
from uuid import UUID

from entities.sede import Sede

sedes: list[Sede] = []


def _buscar_por_id(id_sede: UUID) -> Sede | None:
    for sede in sedes:
        if sede.id_sede == id_sede:
            return sede
    return None


def crear(
    nombre: str,
    direccion: str,
    ciudad: str,
    telefono: str,
    id_usuario_creacion: UUID,
) -> Sede:
    sede = Sede(
        nombre=nombre,
        direccion=direccion,
        ciudad=ciudad,
        telefono=telefono,
        id_usuario_creacion=id_usuario_creacion,
    )
    sedes.append(sede)
    return sede


def eliminar(id_sede: UUID) -> bool:
    sede = _buscar_por_id(id_sede)
    if sede is None:
        return False
    sedes.remove(sede)
    return True


def actualizar(
    id_sede: UUID,
    id_usuario_edicion: UUID,
    nombre: str | None = None,
    direccion: str | None = None,
    ciudad: str | None = None,
    telefono: str | None = None,
) -> Sede | None:
    sede = _buscar_por_id(id_sede)
    if sede is None:
        return None

    if nombre:
        sede.nombre = nombre
    if direccion:
        sede.direccion = direccion
    if ciudad:
        sede.ciudad = ciudad
    if telefono:
        sede.telefono = telefono

    sede.id_usuario_edicion = id_usuario_edicion
    sede.fecha_edicion = date.today()
    return sede


def obtener(id_sede: UUID) -> Sede | None:
    return _buscar_por_id(id_sede)


def listar() -> list[Sede]:
    return list(sedes)
