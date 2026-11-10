from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from database.connection import get_session
from entities.sucursal import Sucursal


def _buscar_por_id(session, id_sucursal: UUID) -> Sucursal | None:
    return session.query(Sucursal).filter_by(id_sucursal=id_sucursal).first()


def crear(
    nombre: str,
    direccion: str,
    ciudad: str,
    telefono: str,
    id_usuario_creacion: UUID | None = None,
) -> Sucursal:
    session = get_session()
    try:
        sucursal = Sucursal(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            id_usuario_creacion=id_usuario_creacion,
        )
        session.add(sucursal)
        session.commit()
        session.refresh(sucursal)
        return sucursal
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_sucursal: UUID) -> bool:
    session = get_session()
    try:
        sucursal = _buscar_por_id(session, id_sucursal)
        if sucursal is None:
            return False
        session.delete(sucursal)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()


def actualizar(
    id_sucursal: UUID,
    nombre: str | None = None,
    direccion: str | None = None,
    ciudad: str | None = None,
    telefono: str | None = None,
    id_usuario_edicion: UUID | None = None,
) -> Sucursal | None:
    session = get_session()
    try:
        sucursal = _buscar_por_id(session, id_sucursal)
        if sucursal is None:
            return None

        if nombre is not None:
            sucursal.nombre = nombre
        if direccion is not None:
            sucursal.direccion = direccion
        if ciudad is not None:
            sucursal.ciudad = ciudad
        if telefono is not None:
            sucursal.telefono = telefono
        if id_usuario_edicion is not None:
            sucursal.id_usuario_edicion = id_usuario_edicion
        sucursal.fecha_edicion = datetime.now()

        session.commit()
        session.refresh(sucursal)
        return sucursal
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def obtener(id_sucursal: UUID) -> Sucursal | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_sucursal)
    finally:
        session.close()


def listar() -> list[Sucursal]:
    session = get_session()
    try:
        return session.query(Sucursal).all()
    finally:
        session.close()
