from datetime import date, datetime
from typing import List
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


class usuarioPost(BaseModel):
    data: UsuarioRead
    status: int
    message: str


class UsuarioList(BaseModel):
    data: List[UsuarioRead]
    status: int
    message: str
    message: str


class usuarioPut(BaseModel):
    data: UsuarioRead
    status: int
    message: str


class TipoCuentaCreate(BaseModel):
    nombre: str
    descripcion: str = ""
    tasa_interes: float
    monto_minimo_apertura: float
    requiere_mantenimiento: bool = False
    estado: str = "Activo"
    id_usuario_creacion: UUID


class TipoCuentaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    tasa_interes: float | None = None
    monto_minimo_apertura: float | None = None
    requiere_mantenimiento: bool | None = None
    estado: str | None = None
    id_usuario_edicion: UUID | None = None


class TipoCuentaRead(BaseModel):
    id_tipo_cuenta: UUID
    nombre: str
    descripcion: str
    tasa_interes: float
    monto_minimo_apertura: float
    requiere_mantenimiento: bool
    estado: str
    id_usuario_creacion: UUID
    id_usuario_edicion: UUID | None
    fecha_creacion: date
    fecha_edicion: date | None


class tipoCuentaPost(BaseModel):
    data: TipoCuentaRead
    status: int
    message: str


class tipoCuentaPut(BaseModel):
    data: TipoCuentaRead
    status: int
    message: str


class TipoCuentaList(BaseModel):
    data: List[TipoCuentaRead]
    status: int
    message: str


class AccionCreate(BaseModel):
    id_usuario: UUID
    tipo_accion: str
    descripcion: str = ""
    ip_origen: str | None = None
    resultado: str = "Exito"


class AccionUpdate(BaseModel):
    tipo_accion: str | None = None
    descripcion: str | None = None
    ip_origen: str | None = None
    resultado: str | None = None


class AccionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_accion: UUID
    id_usuario: UUID
    tipo_accion: str
    descripcion: str
    ip_origen: str | None
    resultado: str
    fecha_accion: date


class AccionList(BaseModel):
    data: List[AccionRead]
    status: int
    message: str


class accionPost(BaseModel):
    data: AccionRead
    status: int
    message: str


class accionPut(BaseModel):
    data: AccionRead
    status: int
    message: str


class TarjetaCreate(BaseModel):
    id_cuenta: UUID
    numero_tarjeta: str
    tipo_tarjeta: str
    fecha_emision: date
    fecha_vencimiento: date
    cvv: str
    limite_credito: float
    estado: str = "Activa"
    id_usuario_creacion: UUID


class TarjetaUpdate(BaseModel):
    numero_tarjeta: str | None = None
    tipo_tarjeta: str | None = None
    fecha_vencimiento: date | None = None
    cvv: str | None = None
    limite_credito: float | None = None
    estado: str | None = None
    id_cuenta: UUID | None = None
    id_usuario_edicion: UUID | None = None


class TarjetaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_tarjeta: UUID
    id_cuenta: UUID
    numero_tarjeta: str
    tipo_tarjeta: str
    fecha_emision: date
    fecha_vencimiento: date
    cvv: str
    limite_credito: float
    estado: str
    id_usuario_creacion: UUID
    id_usuario_edicion: UUID | None
    fecha_creacion: datetime
    fecha_edicion: datetime | None


class TarjetaList(BaseModel):
    data: List[TarjetaRead]
    status: int
    message: str


class tarjetaPost(BaseModel):
    data: TarjetaRead
    status: int
    message: str


class tarjetaPut(BaseModel):
    data: TarjetaRead
    status: int
    message: str
