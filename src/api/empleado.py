from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.schemas import (
    EmpleadoCreate,
    EmpleadoList,
    EmpleadoRead,
    EmpleadoUpdate,
    empleadoPost,
    empleadoPut,
)
from crud import empleado as empleado_crud

empleados_router = APIRouter(prefix="/empleados", tags=["empleados"])


@empleados_router.get("/", response_model=EmpleadoList)
def get_empleados() -> Dict[str, Any]:
    empleados = empleado_crud.listar()

    if not empleados:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron empleados",
        )

    return {
        "data": empleados,
        "status": HTTPStatus.OK.value,
        "message": "Empleados encontrados",
    }


@empleados_router.get("/{id_empleado}", response_model=EmpleadoRead)
def obtener_empleado(id_empleado: UUID):
    empleado = empleado_crud.obtener(id_empleado)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@empleados_router.post("/", response_model=empleadoPost, status_code=201)
def crear_empleado(datos: EmpleadoCreate):
    empleado = empleado_crud.crear(**datos.model_dump())

    if empleado is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El empleado ya existe",
        )

    return {
        "data": empleado,
        "status": HTTPStatus.CREATED.value,
        "message": f"Empleado {empleado.id_empleado} creado",
    }


@empleados_router.put("/{id_empleado}", response_model=empleadoPut)
def actualizar_empleado(id_empleado: UUID, datos: EmpleadoUpdate):
    if empleado_crud.obtener(id_empleado) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Empleado no encontrado",
        )

    empleado = empleado_crud.actualizar(
        id_empleado,
        **datos.model_dump(exclude_unset=True),
    )
    if empleado is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="No se pudo actualizar el empleado",
        )
    return {
        "data": empleado,
        "status": HTTPStatus.OK.value,
        "message": f"Empleado {empleado.id_empleado} actualizado",
    }


@empleados_router.delete("/{id_empleado}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_empleado(id_empleado: UUID):
    if not empleado_crud.eliminar(id_empleado):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Empleado no encontrado",
        )
