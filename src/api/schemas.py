from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UsuarioCreate(BaseModel):
    primer_nombre: str
    segundo_nombre: str = ""
    primer_apellido: str
    segundo_apellido: str = ""
    nombre_usuario: str
    clave: str


class UsuarioUpdate(BaseModel):
    primer_nombre: str | None = None
    segundo_nombre: str | None = None
    primer_apellido: str | None = None
    segundo_apellido: str | None = None
    nombre_usuario: str | None = None
    clave: str | None = None


class UsuarioRead(BaseModel):

    id_usuario: UUID
    primer_nombre: str
    segundo_nombre: str
    primer_apellido: str
    segundo_apellido: str
    nombre_usuario: str


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    clave: str
