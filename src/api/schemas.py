from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


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

    model_config = {"from_attributes": True}


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
    id_usuario_edicion: UUID | None = None


class CuotaRead(CuotaBase):
    id_cuota: UUID
    fecha_creacion: datetime | None = None
    id_usuario_edicion: UUID | None = None
    fecha_edicion: datetime | None = None

    model_config = {"from_attributes": True}


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
    id_usuario_edicion: UUID | None = None


class SucursalRead(SucursalBase):
    id_sucursal: UUID
    fecha_creacion: datetime | None = None
    id_usuario_edicion: UUID | None = None
    fecha_edicion: datetime | None = None

    model_config = {"from_attributes": True}


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

    model_config = {"from_attributes": True}


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


class CuentaBase(BaseModel):
    numero_cuenta: str
    id_usuario: UUID
    id_usuario_creacion: UUID
    id_tipo_cuenta: UUID | None = None
    saldo: float = 0.0
    estado: str = "Activa"


class CuentaCreate(CuentaBase):
    pass


class CuentaUpdate(BaseModel):
    id_usuario_edicion: UUID | None = None
    numero_cuenta: str | None = None
    id_tipo_cuenta: UUID | None = None
    id_usuario: UUID | None = None
    saldo: float | None = None
    estado: str | None = None


class CuentaRead(CuentaBase):
    id_cuenta: UUID
    fecha_apertura: date
    fecha_creacion: datetime
    id_usuario_edicion: UUID | None = None
    fecha_edicion: datetime | None = None

    model_config = {"from_attributes": True}


class CuentaList(BaseModel):
    data: list[CuentaRead]
    status: int
    message: str


class cuentaPost(BaseModel):
    data: CuentaRead
    status: int
    message: str


class cuentaPut(BaseModel):
    data: CuentaRead
    status: int
    message: str


class TarjetaBase(BaseModel):
    id_cuenta: UUID
    numero_tarjeta: str
    tipo_tarjeta: str
    fecha_emision: date
    fecha_vencimiento: date
    cvv: str
    limite_credito: float
    estado: str
    id_usuario_creacion: UUID


class TarjetaCreate(TarjetaBase):
    pass


class TarjetaUpdate(BaseModel):
    id_cuenta: UUID | None = None
    numero_tarjeta: str | None = None
    tipo_tarjeta: str | None = None
    fecha_emision: date | None = None
    fecha_vencimiento: date | None = None
    cvv: str | None = None
    limite_credito: float | None = None
    estado: str | None = None


class TarjetaRead(TarjetaBase):
    id_tarjeta: UUID
    id_usuario_edicion: UUID | None = None
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    model_config = {"from_attributes": True}


class TarjetaList(BaseModel):
    data: list[TarjetaRead]
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


class TipoCuentaBase(BaseModel):
    nombre: str
    descripcion: str = ""
    tasa_interes: float
    monto_minimo_apertura: float
    requiere_mantenimiento: bool = False
    estado: str = "Activo"
    id_usuario_creacion: UUID


class TipoCuentaCreate(TipoCuentaBase):
    pass


class TipoCuentaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    tasa_interes: float | None = None
    monto_minimo_apertura: float | None = None
    requiere_mantenimiento: bool | None = None
    estado: str | None = None
    id_usuario_edicion: UUID | None = None


class TipoCuentaRead(TipoCuentaBase):
    id_tipo_cuenta: UUID
    id_usuario_edicion: UUID | None = None
    fecha_creacion: date | None = None
    fecha_edicion: date | None = None

    model_config = {"from_attributes": True}


class TipoCuentaList(BaseModel):
    data: list[TipoCuentaRead]
    status: int
    message: str


class tipoCuentaPost(BaseModel):
    data: TipoCuentaRead
    status: int
    message: str


class tipoCuentaPut(BaseModel):
    data: TipoCuentaRead
    status: int
    message: str


class AccionBase(BaseModel):
    id_usuario: UUID
    tipo_accion: str
    descripcion: str = ""
    ip_origen: str | None = None
    resultado: str = "Exito"


class AccionCreate(AccionBase):
    pass


class AccionUpdate(BaseModel):
    tipo_accion: str | None = None
    descripcion: str | None = None
    ip_origen: str | None = None
    resultado: str | None = None


class AccionRead(AccionBase):
    id_accion: UUID
    fecha_accion: date

    model_config = {"from_attributes": True}


class AccionList(BaseModel):
    data: list[AccionRead]
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
