from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.schemas import (
    TarjetaCreate,
    TarjetaList,
    TarjetaRead,
    TarjetaUpdate,
    tarjetaPost,
    tarjetaPut,
)
from crud.Tarjeta_crud import TarjetaCRUD
from database.connection import get_session
from entities.Tarjeta import Tarjeta

tarjeta_router = APIRouter(prefix="/tarjetas", tags=["tarjetas"])


@tarjeta_router.get("/", response_model=TarjetaList)
def get_tarjetas() -> Dict[str, Any]:
    tarjetas = TarjetaCRUD.obtener_tarjetas()

    if not tarjetas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron tarjetas",
        )

    return {
        "data": tarjetas,
        "status": HTTPStatus.OK.value,
        "message": "Tarjetas encontradas",
    }


@tarjeta_router.get("/{id_tarjeta}", response_model=TarjetaRead)
def obtener_tarjeta(id_tarjeta: UUID):
    db = get_session()
    try:
        tarjeta = TarjetaCRUD.obtener_tarjeta(db, id_tarjeta)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    finally:
        db.close()
    return tarjeta


@tarjeta_router.post("/", response_model=tarjetaPost, status_code=201)
def crear_tarjeta(datos: TarjetaCreate):
    db = get_session()
    nueva_tarjeta = Tarjeta(**datos.model_dump())
    try:
        tarjeta = TarjetaCRUD.crear_tarjeta(db, nueva_tarjeta)
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail=str(error))
    finally:
        db.close()

    return {
        "data": tarjeta,
        "status": HTTPStatus.CREATED.value,
        "message": f"Tarjeta {tarjeta.numero_tarjeta} creada",
    }


@tarjeta_router.put("/{id_tarjeta}", response_model=tarjetaPut)
def actualizar_tarjeta(id_tarjeta: UUID, datos: TarjetaUpdate):
    db = get_session()
    campos = datos.model_dump(exclude_unset=True)
    id_usuario_edicion = campos.pop("id_usuario_edicion", None)

    try:
        tarjeta = TarjetaCRUD.actualizar_tarjeta(
            db, id_tarjeta, id_usuario_edicion=id_usuario_edicion, **campos
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    finally:
        db.close()

    return {
        "data": tarjeta,
        "status": HTTPStatus.OK.value,
        "message": f"Tarjeta {tarjeta.numero_tarjeta} actualizada",
    }


@tarjeta_router.delete("/{id_tarjeta}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_tarjeta(id_tarjeta: UUID):
    db = get_session()
    try:
        TarjetaCRUD.eliminar_tarjeta(db, id_tarjeta)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    finally:
        db.close()
