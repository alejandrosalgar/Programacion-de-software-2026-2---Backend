from datetime import date, datetime
from uuid import UUID, uuid4

from entities.cuenta import Cuenta

cuentas: list[Cuenta] = []


def _buscar_por_id(id_cuenta: UUID) -> Cuenta | None:
    for cuenta in cuentas:
        if cuenta.id_cuenta == id_cuenta:
            return cuenta
    return None


def _buscar_por_numero(numero_cuenta: str) -> Cuenta | None:
    numero = numero_cuenta.strip()
    for cuenta in cuentas:
        if cuenta.numero_cuenta == numero:
            return cuenta
    return None


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
    if _buscar_por_numero(numero):
        return None

    cuenta = Cuenta(
        id_cuenta=uuid4(),
        numero_cuenta=numero,
        id_usuario=id_usuario,
        id_usuario_creacion=id_usuario_creacion,
        id_tipo_cuenta=id_tipo_cuenta,
        saldo=saldo,
        estado=estado.strip() or "Activa",
        fecha_apertura=date.today(),
        fecha_creacion=datetime.now(),
    )
    cuentas.append(cuenta)
    return cuenta


def eliminar(id_cuenta: UUID) -> bool:
    cuenta = _buscar_por_id(id_cuenta)
    if cuenta is None:
        return False
    cuentas.remove(cuenta)
    return True


def actualizar(
    id_cuenta: UUID,
    id_usuario_edicion: UUID,
    numero_cuenta: str | None = None,
    id_tipo_cuenta: UUID | None = None,
    id_usuario: UUID | None = None,
    saldo: float | None = None,
    estado: str | None = None,
) -> Cuenta | None:
    cuenta = _buscar_por_id(id_cuenta)
    if cuenta is None:
        return None

    if numero_cuenta:
        numero = numero_cuenta.strip()
        existente = _buscar_por_numero(numero)
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

    cuenta.id_usuario_edicion = id_usuario_edicion
    cuenta.fecha_edicion = datetime.now()
    return cuenta


def obtener(id_cuenta: UUID) -> Cuenta | None:
    return _buscar_por_id(id_cuenta)


def listar() -> list[Cuenta]:
    return list(cuentas)
