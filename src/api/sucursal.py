from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.schemas import (
    SucursalCreate,
    SucursalList,
    SucursalRead,
    SucursalUpdate,
    sucursalPost,
    sucursalPut,
)
from crud import sucursal as sucursal_crud

sucursales_router = APIRouter(prefix="/sucursales", tags=["sucursales"])


@sucursales_router.get("/", response_model=SucursalList)
def get_sucursales() -> Dict[str, Any]:
    sucursales = sucursal_crud.listar()

    if not sucursales:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron sucursales",
        )

    return {
        "data": sucursales,
        "status": HTTPStatus.OK.value,
        "message": "Sucursales encontradas",
    }


@sucursales_router.get("/{id_sucursal}", response_model=SucursalRead)
def obtener_sucursal(id_sucursal: UUID):
    sucursal = sucursal_crud.obtener(id_sucursal)
    if sucursal is None:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal


@sucursales_router.post("/", response_model=sucursalPost, status_code=201)
def crear_sucursal(datos: SucursalCreate):
    sucursal = sucursal_crud.crear(**datos.model_dump())

    if sucursal is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="La sucursal ya existe",
        )

    return {
        "data": sucursal,
        "status": HTTPStatus.CREATED.value,
        "message": f"Sucursal {sucursal.nombre} creada",
    }


@sucursales_router.put("/{id_sucursal}", response_model=sucursalPut)
def actualizar_sucursal(id_sucursal: UUID, datos: SucursalUpdate):
    if sucursal_crud.obtener(id_sucursal) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Sucursal no encontrada",
        )

    sucursal = sucursal_crud.actualizar(
        id_sucursal,
        **datos.model_dump(exclude_unset=True),
    )
    if sucursal is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="No se pudo actualizar la sucursal",
        )
    return {
        "data": sucursal,
        "status": HTTPStatus.OK.value,
        "message": f"Sucursal {sucursal.nombre} actualizada",
    }


@sucursales_router.delete("/{id_sucursal}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_sucursal(id_sucursal: UUID):
    if not sucursal_crud.eliminar(id_sucursal):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Sucursal no encontrada",
        )
