import uuid
from datetime import date
from entities.beneficiario import Beneficiario

_beneficiarios: list[Beneficiario] = []


def crear(
    id_cliente: uuid.UUID,
    nombre_completo: str,
    parentesco: str,
    telefono: str,
    id_usuario_creacion: uuid.UUID,
) -> Beneficiario:
    beneficiario = Beneficiario(
        id_cliente=id_cliente,
        nombre_completo=nombre_completo,
        parentesco=parentesco,
        telefono=telefono,
        id_usuario_creacion=id_usuario_creacion,
    )
    _beneficiarios.append(beneficiario)
    return beneficiario


def listar() -> list[Beneficiario]:
    return _beneficiarios.copy()


def obtener(id_beneficiario: uuid.UUID) -> Beneficiario | None:
    for beneficiario in _beneficiarios:
        if beneficiario.id_beneficiario == id_beneficiario:
            return beneficiario
    return None


def actualizar(
    id_beneficiario: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    nombre_completo: str | None = None,
    parentesco: str | None = None,
    telefono: str | None = None,
) -> Beneficiario | None:
    beneficiario = obtener(id_beneficiario)
    if beneficiario is None:
        return None

    if nombre_completo is not None:
        beneficiario.nombre_completo = nombre_completo.strip()
    if parentesco is not None:
        beneficiario.parentesco = parentesco.strip()
    if telefono is not None:
        beneficiario.telefono = telefono.strip()

    beneficiario.id_usuario_edicion = id_usuario_edicion
    beneficiario.fecha_edicion = date.today()
    return beneficiario


def eliminar(id_beneficiario: uuid.UUID) -> bool:
    beneficiario = obtener(id_beneficiario)
    if beneficiario is None:
        return False
    _beneficiarios.remove(beneficiario)
    return True