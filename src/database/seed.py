from __future__ import annotations

import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import Base, engine, get_session
from entities.Accion import Accion
from entities.TipoCuenta import TipoCuenta
from entities.Tarjeta import Tarjeta
from entities.cuenta import Cuenta
from entities.cuota import Cuota
from entities.empleado import Empleado
from entities.sucursal import Sucursal
from entities.usuario import Usuario

MINIMO_POR_ENTIDAD = 30


def _contar(session, modelo) -> int:
    return session.query(modelo).count()


def _sembrar_usuarios(session) -> list[Usuario]:
    while _contar(session, Usuario) < MINIMO_POR_ENTIDAD:
        indice = _contar(session, Usuario) + 1
        nombre_usuario = f"semilla.usuario.{indice:03d}"
        if session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first():
            nombre_usuario = f"semilla.usuario.extra.{indice:03d}"

        session.add(
            Usuario(
                primer_nombre=f"Usuario{indice:03d}",
                segundo_nombre="Demo",
                primer_apellido="Semilla",
                segundo_apellido=f"Banco{indice:03d}",
                nombre_usuario=nombre_usuario,
                clave="demo-cambio-local",
            )
        )
        session.flush()

    return session.query(Usuario).order_by(Usuario.nombre_usuario).all()


def _sembrar_tipos_cuenta(session, usuarios: list[Usuario]) -> list[TipoCuenta]:
    tipos_iniciales = [
        ("Ahorros", "Cuenta de ahorro", 2.5, 50_000, False),
        ("Corriente", "Cuenta para operaciones frecuentes", 0.0, 200_000, True),
        ("Nomina", "Cuenta para recibir nómina", 1.0, 0, False),
    ]
    for nombre, descripcion, tasa, minimo, mantenimiento in tipos_iniciales:
        if not session.query(TipoCuenta).filter_by(nombre=nombre).first():
            session.add(
                TipoCuenta(
                    nombre=nombre,
                    descripcion=descripcion,
                    tasa_interes=tasa,
                    monto_minimo_apertura=minimo,
                    requiere_mantenimiento=mantenimiento,
                    estado="Activo",
                    id_usuario_creacion=usuarios[0].id_usuario,
                )
            )
            session.flush()

    while _contar(session, TipoCuenta) < MINIMO_POR_ENTIDAD:
        indice = _contar(session, TipoCuenta) + 1
        nombre = f"Tipo semilla {indice:03d}"
        if session.query(TipoCuenta).filter_by(nombre=nombre).first():
            nombre = f"Tipo semilla extra {indice:03d}"
        session.add(
            TipoCuenta(
                nombre=nombre,
                descripcion=f"Producto de demostración {indice:03d}",
                tasa_interes=round((indice % 8) * 0.35, 2),
                monto_minimo_apertura=indice * 10_000,
                requiere_mantenimiento=indice % 2 == 0,
                estado="Activo",
                id_usuario_creacion=usuarios[indice % len(usuarios)].id_usuario,
            )
        )
        session.flush()

    return session.query(TipoCuenta).order_by(TipoCuenta.nombre).all()


def _sembrar_sucursales(session, usuarios: list[Usuario]) -> list[Sucursal]:
    ciudades = ["Medellín", "Bogotá", "Cali", "Manizales", "Pereira"]
    while _contar(session, Sucursal) < MINIMO_POR_ENTIDAD:
        indice = _contar(session, Sucursal) + 1
        nombre = f"Sucursal Semilla {indice:03d}"
        if session.query(Sucursal).filter_by(nombre=nombre).first():
            nombre = f"Sucursal Semilla Extra {indice:03d}"
        session.add(
            Sucursal(
                nombre=nombre,
                direccion=f"Carrera {10 + indice} #{indice:02d}-20",
                ciudad=ciudades[(indice - 1) % len(ciudades)],
                telefono=f"60{(indice % 5) + 1}555{indice:04d}",
                id_usuario_creacion=usuarios[indice % len(usuarios)].id_usuario,
            )
        )
        session.flush()

    return session.query(Sucursal).order_by(Sucursal.id_sucursal).all()


def _sembrar_cuentas(
    session, usuarios: list[Usuario], tipos: list[TipoCuenta]
) -> list[Cuenta]:
    indice = 1
    while _contar(session, Cuenta) < MINIMO_POR_ENTIDAD:
        numero = f"2000{indice:06d}"
        indice += 1
        if session.query(Cuenta).filter_by(numero_cuenta=numero).first():
            continue

        usuario = usuarios[(indice - 2) % len(usuarios)]
        tipo = tipos[(indice - 2) % len(tipos)]
        session.add(
            Cuenta(
                numero_cuenta=numero,
                id_usuario=usuario.id_usuario,
                id_usuario_creacion=usuario.id_usuario,
                id_tipo_cuenta=tipo.id_tipo_cuenta,
                saldo=float(((indice * 137_000) % 8_000_000) + 50_000),
                estado="Activa",
                fecha_apertura=date.today() - timedelta(days=indice * 4),
                fecha_creacion=datetime.now(),
            )
        )
        session.flush()

    return session.query(Cuenta).order_by(Cuenta.numero_cuenta).all()


def _sembrar_tarjetas(session, cuentas: list[Cuenta]) -> None:
    indice = 1
    hoy = date.today()
    vencimiento = date(hoy.year + 4, hoy.month, min(hoy.day, 28))
    while _contar(session, Tarjeta) < MINIMO_POR_ENTIDAD:
        numero = f"99990000{indice:08d}"
        indice += 1
        if session.query(Tarjeta).filter_by(numero_tarjeta=numero).first():
            continue

        cuenta = cuentas[(indice - 2) % len(cuentas)]
        credito = indice % 2 == 0
        session.add(
            Tarjeta(
                id_cuenta=cuenta.id_cuenta,
                numero_tarjeta=numero,
                tipo_tarjeta="credito" if credito else "debito",
                fecha_emision=hoy,
                fecha_vencimiento=vencimiento,
                cvv="000",
                limite_credito=1_000_000.0 if credito else 0.0,
                estado="Activa",
                id_usuario_creacion=cuenta.id_usuario,
            )
        )
        session.flush()


def _sembrar_empleados(
    session, usuarios: list[Usuario], sucursales: list[Sucursal]
) -> None:
    existentes = {
        (fila.id_usuario, fila.id_sucursal)
        for fila in session.query(Empleado.id_usuario, Empleado.id_sucursal).all()
    }
    cargos = ["Asesor", "Cajero", "Analista", "Coordinador", "Gerente"]
    for usuario in usuarios:
        for sucursal in sucursales:
            if _contar(session, Empleado) >= MINIMO_POR_ENTIDAD:
                return
            llave = (usuario.id_usuario, sucursal.id_sucursal)
            if llave in existentes:
                continue
            session.add(
                Empleado(
                    id_usuario=usuario.id_usuario,
                    id_sucursal=sucursal.id_sucursal,
                    cargo=cargos[_contar(session, Empleado) % len(cargos)],
                    activo=True,
                    id_usuario_creacion=usuario.id_usuario,
                )
            )
            existentes.add(llave)
            session.flush()


def _sembrar_cuotas(session, usuarios: list[Usuario]) -> None:
    indice = 1
    while _contar(session, Cuota) < MINIMO_POR_ENTIDAD:
        numero = (indice - 1) % 10 + 1
        id_prestamo = uuid5(
            NAMESPACE_URL,
            f"banco-itm-semilla-prestamo-{(indice - 1) // 10 + 1}",
        )
        indice += 1
        if (
            session.query(Cuota)
            .filter_by(id_prestamo=id_prestamo, numero_cuota=numero)
            .first()
        ):
            continue

        session.add(
            Cuota(
                id_prestamo=id_prestamo,
                numero_cuota=numero,
                valor=float(150_000 + numero * 25_000),
                fecha_vencimiento=date.today() + timedelta(days=30 * numero),
                estado="pendiente" if numero % 3 else "pagada",
                id_usuario_creacion=usuarios[(indice - 2) % len(usuarios)].id_usuario,
            )
        )
        session.flush()


def _sembrar_acciones(session, usuarios: list[Usuario]) -> None:
    indice = 1
    while _contar(session, Accion) < MINIMO_POR_ENTIDAD:
        tipo = f"Operacion semilla {indice:03d}"
        ip_origen = f"198.51.100.{indice}"
        indice += 1
        if (
            session.query(Accion)
            .filter_by(tipo_accion=tipo, ip_origen=ip_origen)
            .first()
        ):
            continue

        session.add(
            Accion(
                id_usuario=usuarios[(indice - 2) % len(usuarios)].id_usuario,
                tipo_accion=tipo,
                descripcion=f"Registro de auditoría de demostración {indice - 1:03d}",
                ip_origen=ip_origen,
                resultado="Error" if indice % 7 == 0 else "Exito",
                fecha_accion=date.today() - timedelta(days=indice % 30),
            )
        )
        session.flush()


def seed() -> dict[str, int]:
    Base.metadata.create_all(bind=engine)
    session = get_session()
    try:
        usuarios = _sembrar_usuarios(session)
        tipos = _sembrar_tipos_cuenta(session, usuarios)
        sucursales = _sembrar_sucursales(session, usuarios)
        cuentas = _sembrar_cuentas(session, usuarios, tipos)
        _sembrar_tarjetas(session, cuentas)
        _sembrar_empleados(session, usuarios, sucursales)
        _sembrar_cuotas(session, usuarios)
        _sembrar_acciones(session, usuarios)
        session.commit()
        return {
            "usuarios": _contar(session, Usuario),
            "cuentas": _contar(session, Cuenta),
            "cuotas": _contar(session, Cuota),
            "sucursales": _contar(session, Sucursal),
            "empleados": _contar(session, Empleado),
            "tarjetas": _contar(session, Tarjeta),
            "tipos_cuenta": _contar(session, TipoCuenta),
            "acciones": _contar(session, Accion),
        }
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    resultado = seed()
    for entidad, total in resultado.items():
        print(f"{entidad}: {total}")
