from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.schemas import (
    TipoCuentaCreate,
    TipoCuentaList,
    TipoCuentaRead,
    TipoCuentaUpdate,
    tipoCuentaPost,
    tipoCuentaPut,
)
from crud.TipoCuenta_crud import TipoCuentaCRUD
from database.connection import get_session
from entities.TipoCuenta import TipoCuenta

tipocuenta_router = APIRouter(prefix="/tipocuentas", tags=["tipocuentas"])


@tipocuenta_router.get("/", response_model=TipoCuentaList)
def get_tipocuentas() -> Dict[str, Any]:
    tipocuentas = TipoCuentaCRUD.obtener_tipos_cuenta()

    if not tipocuentas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron tipos de cuenta",
        )

    return {
        "data": tipocuentas,
        "status": HTTPStatus.OK.value,
        "message": "Tipo de cuentas obtenidas correctamente",
    }


@tipocuenta_router.get("/{id_tipo_cuenta}", response_model=TipoCuentaRead)
def obtener_tipocuenta(id_tipo_cuenta: UUID):
    db = get_session()
    try:
        try:
            tipo_cuenta = TipoCuentaCRUD.obtener_tipo_cuenta(db, id_tipo_cuenta)
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value,
                detail="Tipo de cuenta no encontrado",
            )
    finally:
        db.close()
    return tipo_cuenta


@tipocuenta_router.get("/{id_tipo_cuenta}", response_model=TipoCuentaRead)
def obtener_tipocuenta(id_tipo_cuenta: UUID): ...


@tipocuenta_router.post(
    "/", response_model=tipoCuentaPost, status_code=HTTPStatus.CREATED.value
)
def crear_tipocuenta(datos: TipoCuentaCreate):
    db = get_session()
    try:
        nuevo_tipo = TipoCuenta(**datos.model_dump())
        try:
            tipo_cuenta = TipoCuentaCRUD.crear_tipo_cuenta(db, nuevo_tipo)
        except ValueError as error:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT.value,
                detail=str(error),
            )
    finally:
        db.close()

    return {
        "data": tipo_cuenta,
        "status": HTTPStatus.CREATED.value,
        "message": f"Tipo de cuenta {tipo_cuenta.nombre} creado",
    }


@tipocuenta_router.put("/{id_tipo_cuenta}", response_model=tipoCuentaPut)
def actualizar_tipocuenta(id_tipo_cuenta: UUID, datos: TipoCuentaUpdate):
    db = get_session()
    try:
        campos = datos.model_dump(exclude_unset=True)
        id_usuario_edicion = campos.pop("id_usuario_edicion", None)
        try:
            tipo_cuenta = TipoCuentaCRUD.actualizar_tipo_cuenta(
                db, id_tipo_cuenta, id_usuario_edicion=id_usuario_edicion, **campos
            )
        except ValueError as error:
            code = (
                HTTPStatus.NOT_FOUND.value
                if "no encontrado" in str(error)
                else HTTPStatus.CONFLICT.value
            )
            raise HTTPException(status_code=code, detail=str(error))
    finally:
        db.close()

    return {
        "data": tipo_cuenta,
        "status": HTTPStatus.OK.value,
        "message": f"Tipo de cuenta {tipo_cuenta.nombre} actualizado",
    }


@tipocuenta_router.delete("/{id_tipo_cuenta}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_tipocuenta(id_tipo_cuenta: UUID):
    db = get_session()
    try:
        try:
            TipoCuentaCRUD.eliminar_tipo_cuenta(db, id_tipo_cuenta)
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value,
                detail="Tipo de cuenta no encontrado",
            )
    finally:
        db.close()
