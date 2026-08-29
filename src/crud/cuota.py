from datetime import date
from uuid import UUID

from entities.cuota import Cuota

cuotas: list[Cuota] = []


def _buscar_por_id(id_cuota: UUID) -> Cuota | None:
    for cuota in cuotas:
        if cuota.id_cuota == id_cuota:
            return cuota
    return None


def crear(
    id_prestamo: UUID,
    valor: float,
    numero_cuota: int,
    fecha_vencimiento: date,
    estado: str = "pendiente",
    id_usuario_creacion: UUID | None = None,
) -> Cuota:
    cuota = Cuota(
        id_prestamo=id_prestamo,
        valor=valor,
        numero_cuota=numero_cuota,
        fecha_vencimiento=fecha_vencimiento,
        estado=estado,
        id_usuario_creacion=id_usuario_creacion,
    )
    cuotas.append(cuota)
    return cuota


def eliminar(id_cuota: UUID) -> bool:
    cuota = _buscar_por_id(id_cuota)
    if cuota is None:
        return False
    cuotas.remove(cuota)
    return True


def actualizar(
    id_cuota: UUID,
    id_usuario_edicion: UUID,
    id_prestamo: UUID | None = None,
    valor: float | None = None,
    numero_cuota: int | None = None,
    fecha_vencimiento: date | None = None,
    estado: str | None = None,
) -> Cuota | None:
    cuota = _buscar_por_id(id_cuota)
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

    cuota.id_usuario_edicion = id_usuario_edicion
    cuota.fecha_edicion = date.today()
    return cuota


def obtener(id_cuota: UUID) -> Cuota | None:
    return _buscar_por_id(id_cuota)


def listar() -> list[Cuota]:
    return list(cuotas)
