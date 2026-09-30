from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.schemas import (
    CuotaCreate,
    CuotaList,
    CuotaRead,
    CuotaUpdate,
    cuotaPost,
    cuotaPut,
)
from crud import cuota as cuota_crud

cuotas_router = APIRouter(prefix="/cuotas", tags=["cuotas"])


@cuotas_router.get("/", response_model=CuotaList)
def get_cuotas() -> Dict[str, Any]:
    cuotas = cuota_crud.listar()

    if not cuotas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron cuotas",
        )

    return {
        "data": cuotas,
        "status": HTTPStatus.OK.value,
        "message": "Cuotas encontradas",
    }


@cuotas_router.get("/{id_cuota}", response_model=CuotaRead)
def obtener_cuota(id_cuota: UUID):
    cuota = cuota_crud.obtener(id_cuota)
    if cuota is None:
        raise HTTPException(status_code=404, detail="Cuota no encontrada")
    return cuota


@cuotas_router.post("/", response_model=cuotaPost, status_code=201)
def crear_cuota(datos: CuotaCreate):
    cuota = cuota_crud.crear(**datos.model_dump())

    if cuota is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="La cuota ya existe",
        )

    return {
        "data": cuota,
        "status": HTTPStatus.CREATED.value,
        "message": f"Cuota {cuota.id_cuota} creada",
    }


@cuotas_router.put("/{id_cuota}", response_model=cuotaPut)
def actualizar_cuota(id_cuota: UUID, datos: CuotaUpdate):
    if cuota_crud.obtener(id_cuota) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Cuota no encontrada",
        )

    cuota = cuota_crud.actualizar(
        id_cuota,
        **datos.model_dump(exclude_unset=True),
    )
    if cuota is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="No se pudo actualizar la cuota",
        )
    return {
        "data": cuota,
        "status": HTTPStatus.OK.value,
        "message": f"Cuota {cuota.id_cuota} actualizada",
    }


@cuotas_router.delete("/{id_cuota}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_cuota(id_cuota: UUID):
    if not cuota_crud.eliminar(id_cuota):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Cuota no encontrada",
        )
