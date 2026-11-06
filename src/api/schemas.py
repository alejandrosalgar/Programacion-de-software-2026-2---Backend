from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class UsuarioBase(BaseModel):
    primer_nombre: str
    segundo_nombre: str | None = None
    primer_apellido: str
    segundo_apellido: str | None = None
    nombre_usuario: str
    clave: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    primer_nombre: str | None = None
    segundo_nombre: str | None = None
    primer_apellido: str | None = None
    segundo_apellido: str | None = None
    nombre_usuario: str | None = None
    clave: str | None = None


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    clave: str


class UsuarioRead(UsuarioBase):
    id_usuario: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None


class UsuarioList(BaseModel):
    data: list[UsuarioRead]
    status: int
    message: str


class usuarioPost(BaseModel):
    data: UsuarioRead
    status: int
    message: str


class usuarioPut(BaseModel):
    data: UsuarioRead
    status: int
    message: str


class CuotaBase(BaseModel):
    id_prestamo: UUID
    valor: float
    numero_cuota: int
    fecha_vencimiento: date
    estado: str = "pendiente"
    id_usuario_creacion: UUID | None = None


class CuotaCreate(CuotaBase):
    pass


class CuotaUpdate(BaseModel):
    id_prestamo: UUID | None = None
    valor: float | None = None
    numero_cuota: int | None = None
    fecha_vencimiento: date | None = None
    estado: str | None = None
    id_usuario_creacion: UUID | None = None


class CuotaRead(CuotaBase):
    id_cuota: UUID
    fecha_creacion: datetime | None = None
    id_usuario_edicion: UUID | None = None
    fecha_edicion: datetime | None = None


class CuotaList(BaseModel):
    data: list[CuotaRead]
    status: int
    message: str


class cuotaPost(BaseModel):
    data: CuotaRead
    status: int
    message: str


class cuotaPut(BaseModel):
    data: CuotaRead
    status: int
    message: str


class SucursalBase(BaseModel):
    nombre: str
    direccion: str
    ciudad: str
    telefono: str
    id_usuario_creacion: UUID | None = None


class SucursalCreate(SucursalBase):
    pass


class SucursalUpdate(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    ciudad: str | None = None
    telefono: str | None = None
    id_usuario_creacion: UUID | None = None


class SucursalRead(SucursalBase):
    id_sucursal: UUID
    fecha_creacion: datetime | None = None
    id_usuario_edicion: UUID | None = None
    fecha_edicion: datetime | None = None


class SucursalList(BaseModel):
    data: list[SucursalRead]
    status: int
    message: str


class sucursalPost(BaseModel):
    data: SucursalRead
    status: int
    message: str


class sucursalPut(BaseModel):
    data: SucursalRead
    status: int
    message: str


class EmpleadoBase(BaseModel):
    id_usuario: UUID
    id_sucursal: UUID
    cargo: str
    activo: bool = True
    id_usuario_creacion: UUID | None = None


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    id_usuario: UUID | None = None
    id_sucursal: UUID | None = None
    cargo: str | None = None
    activo: bool | None = None
    id_usuario_creacion: UUID | None = None


class EmpleadoRead(EmpleadoBase):
    id_empleado: UUID
    fecha_creacion: datetime | None = None
    id_usuario_edicion: UUID | None = None
    fecha_edicion: datetime | None = None


class EmpleadoList(BaseModel):
    data: list[EmpleadoRead]
    status: int
    message: str


class empleadoPost(BaseModel):
    data: EmpleadoRead
    status: int
    message: str


class empleadoPut(BaseModel):
    data: EmpleadoRead
    status: int
    message: str
