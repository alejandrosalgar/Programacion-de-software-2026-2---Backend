from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from database.connection import get_session
from entities.empleado import Empleado


def _buscar_por_id(session, id_empleado: UUID) -> Empleado | None:
    return session.query(Empleado).filter_by(id_empleado=id_empleado).first()


def crear(
    id_usuario: UUID,
    id_sucursal: UUID,
    cargo: str,
    activo: bool = True,
    id_usuario_creacion: UUID | None = None,
) -> Empleado:
    session = get_session()
    try:
        empleado = Empleado(
            id_usuario=id_usuario,
            id_sucursal=id_sucursal,
            cargo=cargo,
            activo=activo,
            id_usuario_creacion=id_usuario_creacion,
        )
        session.add(empleado)
        session.commit()
        session.refresh(empleado)
        return empleado
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_empleado: UUID) -> bool:
    session = get_session()
    try:
        empleado = _buscar_por_id(session, id_empleado)
        if empleado is None:
            return False
        session.delete(empleado)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()


def actualizar(
    id_empleado: UUID,
    id_usuario: UUID | None = None,
    id_sucursal: UUID | None = None,
    cargo: str | None = None,
    activo: bool | None = None,
    id_usuario_creacion: UUID | None = None,
) -> Empleado | None:
    session = get_session()
    try:
        empleado = _buscar_por_id(session, id_empleado)
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
        if id_usuario_creacion is not None:
            empleado.id_usuario_creacion = id_usuario_creacion

        empleado.fecha_edicion = datetime.now()
        session.commit()
        session.refresh(empleado)
        return empleado
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def obtener(id_empleado: UUID) -> Empleado | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_empleado)
    finally:
        session.close()


def listar() -> list[Empleado]:
    session = get_session()
    try:
        return session.query(Empleado).all()
    finally:
        session.close()
