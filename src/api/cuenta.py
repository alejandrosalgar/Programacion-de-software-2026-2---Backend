from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.schemas import (
    CuentaCreate,
    CuentaList,
    CuentaRead,
    CuentaUpdate,
    cuentaPost,
    cuentaPut,
)
from crud import cuenta as cuenta_crud

cuentas_router = APIRouter(prefix="/cuentas", tags=["cuentas"])


@cuentas_router.get("/", response_model=CuentaList)
def get_cuentas() -> dict[str, Any]:
    cuentas = cuenta_crud.listar()
    return {
        "data": cuentas,
        "status": HTTPStatus.OK.value,
        "message": "Cuentas encontradas" if cuentas else "No hay cuentas",
    }


@cuentas_router.get("/{id_cuenta}", response_model=CuentaRead)
def obtener_cuenta(id_cuenta: UUID):
    cuenta = cuenta_crud.obtener(id_cuenta)
    if cuenta is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Cuenta no encontrada"
        )
    return cuenta


@cuentas_router.post(
    "/", response_model=cuentaPost, status_code=HTTPStatus.CREATED.value
)
def crear_cuenta(datos: CuentaCreate):
    cuenta = cuenta_crud.crear(**datos.model_dump())
    if cuenta is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="La cuenta ya existe o las referencias no son válidas",
        )
    return {
        "data": cuenta,
        "status": HTTPStatus.CREATED.value,
        "message": f"Cuenta {cuenta.numero_cuenta} creada",
    }


@cuentas_router.put("/{id_cuenta}", response_model=cuentaPut)
def actualizar_cuenta(id_cuenta: UUID, datos: CuentaUpdate):
    cuenta = cuenta_crud.actualizar(id_cuenta, **datos.model_dump(exclude_unset=True))
    if cuenta is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Cuenta no encontrada o datos duplicados/no válidos",
        )
    return {
        "data": cuenta,
        "status": HTTPStatus.OK.value,
        "message": f"Cuenta {cuenta.numero_cuenta} actualizada",
    }


@cuentas_router.delete("/{id_cuenta}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_cuenta(id_cuenta: UUID):
    if cuenta_crud.obtener(id_cuenta) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Cuenta no encontrada",
        )
    if not cuenta_crud.eliminar(id_cuenta):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="No se puede eliminar la cuenta porque tiene tarjetas u otros registros asociados",
        )
