from datetime import date, datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from database.connection import get_session
from entities.cuenta import Cuenta


def _buscar_por_id(session, id_cuenta: UUID) -> Cuenta | None:
    return session.query(Cuenta).filter_by(id_cuenta=id_cuenta).first()


def crear(
    numero_cuenta: str,
    id_usuario: UUID,
    id_usuario_creacion: UUID,
    id_tipo_cuenta: UUID | None = None,
    saldo: float = 0.0,
    estado: str = "Activa",
) -> Cuenta | None:
    numero = numero_cuenta.strip()
    if not numero:
        return None
    session = get_session()
    try:
        if session.query(Cuenta).filter_by(numero_cuenta=numero).first():
            return None

        cuenta = Cuenta(
            numero_cuenta=numero,
            id_usuario=id_usuario,
            id_usuario_creacion=id_usuario_creacion,
            id_tipo_cuenta=id_tipo_cuenta,
            saldo=saldo,
            estado=estado.strip() or "Activa",
            fecha_apertura=date.today(),
        )
        session.add(cuenta)
        session.commit()
        session.refresh(cuenta)
        return cuenta
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_cuenta: UUID) -> bool:
    session = get_session()
    try:
        cuenta = _buscar_por_id(session, id_cuenta)
        if cuenta is None:
            return False
        session.delete(cuenta)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()


def actualizar(
    id_cuenta: UUID,
    id_usuario_edicion: UUID | None = None,
    numero_cuenta: str | None = None,
    id_tipo_cuenta: UUID | None = None,
    id_usuario: UUID | None = None,
    saldo: float | None = None,
    estado: str | None = None,
) -> Cuenta | None:
    session = get_session()
    try:
        cuenta = _buscar_por_id(session, id_cuenta)
        if cuenta is None:
            return None

        if numero_cuenta:
            numero = numero_cuenta.strip()
            existente = session.query(Cuenta).filter_by(numero_cuenta=numero).first()
            if existente is not None and existente.id_cuenta != id_cuenta:
                return None
            cuenta.numero_cuenta = numero
        if id_tipo_cuenta is not None:
            cuenta.id_tipo_cuenta = id_tipo_cuenta
        if id_usuario is not None:
            cuenta.id_usuario = id_usuario
        if saldo is not None:
            cuenta.saldo = saldo
        if estado:
            cuenta.estado = estado.strip()
        if id_usuario_edicion is not None:
            cuenta.id_usuario_edicion = id_usuario_edicion
        cuenta.fecha_edicion = datetime.now()

        session.commit()
        session.refresh(cuenta)
        return cuenta
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def obtener(id_cuenta: UUID) -> Cuenta | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_cuenta)
    finally:
        session.close()


def listar() -> list[Cuenta]:
    session = get_session()
    try:
        return session.query(Cuenta).all()
    finally:
        session.close()
