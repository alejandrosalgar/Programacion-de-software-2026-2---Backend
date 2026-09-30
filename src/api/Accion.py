from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, HTTPException

from api.schemas import (
    AccionCreate,
    AccionList,
    AccionRead,
    AccionUpdate,
    accionPost,
    accionPut,
)
from crud.Accion_crud import AccionCRUD
from database.connection import get_session
from entities.Accion import Accion

accion_router = APIRouter(prefix="/acciones", tags=["acciones"])


@accion_router.get("/", response_model=AccionList)
def get_acciones() -> Dict[str, Any]:
    db = get_session()
    try:
        acciones = AccionCRUD.obtener_acciones()
    finally:
        db.close()

    if not acciones:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron acciones"
        )

    return {
        "data": acciones,
        "status": HTTPStatus.OK.value,
        "message": "Acciones encontradas",
    }


@accion_router.get("/usuario/{id_usuario}", response_model=AccionList)
def get_acciones_por_usuario(id_usuario: UUID) -> Dict[str, Any]:
    db = get_session()
    try:
        acciones = AccionCRUD.obtener_acciones_por_usuario(db, id_usuario)
    finally:
        db.close()

    return {
        "data": acciones,
        "status": HTTPStatus.OK.value,
        "message": "Acciones encontradas",
    }


@accion_router.get("/{id_accion}", response_model=AccionRead)
def obtener_accion(id_accion: UUID):
    db = get_session()
    try:
        try:
            accion = AccionCRUD.obtener_accion(db, id_accion)
        except ValueError:
            raise HTTPException(status_code=404, detail="Acción no encontrada")
    finally:
        db.close()
    return accion


@accion_router.post("/", response_model=accionPost, status_code=201)
def crear_accion(datos: AccionCreate):
    db = get_session()
    try:
        nueva_accion = Accion(**datos.model_dump())
        accion = AccionCRUD.crear_accion(db, nueva_accion)
    except (ValueError, IntegrityError) as error:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="Error al crear la acción. Verifique que el id_usuario exista.",
        )
    finally:
        db.close()

    return {
        "data": accion,
        "status": HTTPStatus.CREATED.value,
        "message": f"Acción {accion.tipo_accion} creada",
    }


@accion_router.put("/{id_accion}", response_model=accionPut)
def actualizar_accion(id_accion: UUID, datos: AccionUpdate):
    db = get_session()
    try:
        try:
            accion = AccionCRUD.actualizar_accion(
                db, id_accion, **datos.model_dump(exclude_unset=True)
            )
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))
    finally:
        db.close()

    return {
        "data": accion,
        "status": HTTPStatus.OK.value,
        "message": f"Acción {accion.tipo_accion} actualizada",
    }


@accion_router.delete("/{id_accion}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_accion(id_accion: UUID):
    db = get_session()
    try:
        try:
            AccionCRUD.eliminar_accion(db, id_accion)
        except ValueError:
            raise HTTPException(status_code=404, detail="Acción no encontrada")
    finally:
        db.close()
