from datetime import date, datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from database.connection import get_session
from entities.cuota import Cuota


def _buscar_por_id(session, id_cuota: UUID) -> Cuota | None:
    return session.query(Cuota).filter_by(id_cuota=id_cuota).first()


def crear(
    id_prestamo: UUID,
    valor: float,
    numero_cuota: int,
    fecha_vencimiento: date,
    estado: str = "pendiente",
    id_usuario_creacion: UUID | None = None,
) -> Cuota:
    session = get_session()
    try:
        cuota = Cuota(
            id_prestamo=id_prestamo,
            valor=valor,
            numero_cuota=numero_cuota,
            fecha_vencimiento=fecha_vencimiento,
            estado=estado,
            id_usuario_creacion=id_usuario_creacion,
        )
        session.add(cuota)
        session.commit()
        session.refresh(cuota)
        return cuota
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_cuota: UUID) -> bool:
    session = get_session()
    try:
        cuota = _buscar_por_id(session, id_cuota)
        if cuota is None:
            return False
        session.delete(cuota)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()


def actualizar(
    id_cuota: UUID,
    id_usuario_edicion: UUID | None = None,
    id_prestamo: UUID | None = None,
    valor: float | None = None,
    numero_cuota: int | None = None,
    fecha_vencimiento: date | None = None,
    estado: str | None = None,
) -> Cuota | None:
    session = get_session()
    try:
        cuota = _buscar_por_id(session, id_cuota)
        if cuota is None:
            return None

        if id_prestamo is not None:
            cuota.id_prestamo = id_prestamo
        if valor is not None:
            cuota.valor = valor
        if numero_cuota is not None:
            cuota.numero_cuota = numero_cuota
        if fecha_vencimiento is not None:
            cuota.fecha_vencimiento = fecha_vencimiento
        if estado is not None:
            cuota.estado = estado
        if id_usuario_edicion is not None:
            cuota.id_usuario_edicion = id_usuario_edicion
        cuota.fecha_edicion = datetime.now()

        session.commit()
        session.refresh(cuota)
        return cuota
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def obtener(id_cuota: UUID) -> Cuota | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_cuota)
    finally:
        session.close()


def listar() -> list[Cuota]:
    session = get_session()
    try:
        return session.query(Cuota).all()
    finally:
        session.close()
