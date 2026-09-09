from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.schemas import UsuarioCreate, UsuarioLogin, UsuarioRead, UsuarioUpdate
from crud import usuario as usuario_crud

usuarios_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuarios_router.get("/", response_model=list[UsuarioRead])
def listar_usuarios():
    return usuario_crud.listar()


@usuarios_router.post("/login", response_model=UsuarioRead)
def iniciar_sesion(datos: UsuarioLogin):
    usuario = usuario_crud.obtener(datos.nombre_usuario, datos.clave)
    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Nombre de usuario o clave incorrectos",
        )
    return usuario


@usuarios_router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: UUID):
    usuario = usuario_crud.obtener_por_id(id_usuario)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@usuarios_router.post("/", response_model=UsuarioRead, status_code=201)
def crear_usuario(datos: UsuarioCreate):
    usuario = usuario_crud.crear(
        primer_nombre=datos.primer_nombre,
        segundo_nombre=datos.segundo_nombre,
        primer_apellido=datos.primer_apellido,
        segundo_apellido=datos.segundo_apellido,
        nombre_usuario=datos.nombre_usuario,
        clave=datos.clave,
    )
    if usuario is None:
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
    return usuario


@usuarios_router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(id_usuario: UUID, datos: UsuarioUpdate):
    if usuario_crud.obtener_por_id(id_usuario) is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario = usuario_crud.actualizar(
        id_usuario,
        **datos.model_dump(exclude_unset=True),
    )
    if usuario is None:
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
    return usuario


@usuarios_router.delete("/{id_usuario}", status_code=204)
def eliminar_usuario(id_usuario: UUID):
    if not usuario_crud.eliminar(id_usuario):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
