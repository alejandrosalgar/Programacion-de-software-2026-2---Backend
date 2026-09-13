import sys
from datetime import date, datetime
from pathlib import Path
from uuid import UUID

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import Base, engine, get_session
from entities.cuenta import Cuenta
from entities.Tarjeta import Tarjeta
from entities.cuota import Cuota
from entities.empleado import Empleado
from entities.sucursal import Sucursal
from entities.usuario import Usuario

USUARIOS_SEED = [
    {
        "primer_nombre": "Ana",
        "segundo_nombre": "Maria",
        "primer_apellido": "Restrepo",
        "segundo_apellido": "Lopez",
        "nombre_usuario": "ana.restrepo",
        "clave": "123456",
    },
    {
        "primer_nombre": "Carlos",
        "segundo_nombre": "Andres",
        "primer_apellido": "Ruiz",
        "segundo_apellido": "Gomez",
        "nombre_usuario": "carlos.ruiz",
        "clave": "123456",
    },
    {
        "primer_nombre": "Laura",
        "segundo_nombre": "",
        "primer_apellido": "Mendez",
        "segundo_apellido": "Castro",
        "nombre_usuario": "laura.mendez",
        "clave": "123456",
    },
]

CUENTAS_SEED = [
    {
        "nombre_usuario": "ana.restrepo",
        "numero_cuenta": "1001000001",
        "saldo": 2_500_000.0,
        "estado": "Activa",
    },
    {
        "nombre_usuario": "carlos.ruiz",
        "numero_cuenta": "1001000002",
        "saldo": 800_000.0,
        "estado": "Activa",
    },
    {
        "nombre_usuario": "laura.mendez",
        "numero_cuenta": "1001000003",
        "saldo": 150_000.0,
        "estado": "Activa",
    },
]

TARJETAS_SEED = [
    {
        "numero_cuenta": "1001000001",
        "numero_tarjeta": "4532123456789012",
        "tipo_tarjeta": "debito",
        "cvv": "123",
        "limite_credito": 0.0,
        "estado": "Activa",
    },
    {
        "numero_cuenta": "1001000001",
        "numero_tarjeta": "5412345678901234",
        "tipo_tarjeta": "credito",
        "cvv": "456",
        "limite_credito": 5_000_000.0,
        "estado": "Activa",
    },
    {
        "numero_cuenta": "1001000002",
        "numero_tarjeta": "4111222233334444",
        "tipo_tarjeta": "credito",
        "cvv": "789",
        "limite_credito": 3_000_000.0,
        "estado": "Activa",
    },
    {
        "numero_cuenta": "1001000003",
        "numero_tarjeta": "4000123412341234",
        "tipo_tarjeta": "debito",
        "cvv": "321",
        "limite_credito": 0.0,
        "estado": "Activa",
    },
]

SUCURSALES_SEED = [
    {
        "nombre": "Sucursal Centro",
        "direccion": "Carrera 7 # 12-34",
        "ciudad": "Bogota",
        "telefono": "6015550101",
    },
    {
        "nombre": "Sucursal Norte",
        "direccion": "Calle 100 # 15-20",
        "ciudad": "Bogota",
        "telefono": "6015550102",
    },
    {
        "nombre": "Sucursal Medellin",
        "direccion": "Carrera 43A # 1-50",
        "ciudad": "Medellin",
        "telefono": "6045550103",
    },
    {
        "nombre": "Sucursal Cali",
        "direccion": "Calle 10 # 4-25",
        "ciudad": "Cali",
        "telefono": "6025550104",
    },
    {
        "nombre": "Sucursal Barranquilla",
        "direccion": "Carrera 53 # 80-10",
        "ciudad": "Barranquilla",
        "telefono": "6055550105",
    },
]

EMPLEADOS_SEED = [
    {
        "nombre_usuario": "ana.restrepo",
        "nombre_sucursal": "Sucursal Centro",
        "cargo": "Gerente",
    },
    {
        "nombre_usuario": "carlos.ruiz",
        "nombre_sucursal": "Sucursal Norte",
        "cargo": "Asesor",
    },
    {
        "nombre_usuario": "laura.mendez",
        "nombre_sucursal": "Sucursal Medellin",
        "cargo": "Cajera",
    },
    {
        "nombre_usuario": "ana.restrepo",
        "nombre_sucursal": "Sucursal Cali",
        "cargo": "Asesora comercial",
    },
    {
        "nombre_usuario": "carlos.ruiz",
        "nombre_sucursal": "Sucursal Barranquilla",
        "cargo": "Analista de credito",
    },
]

CUOTAS_SEED = [
    {
        "id_prestamo": UUID("00000000-0000-0000-0000-000000000001"),
        "numero_cuota": 1,
        "valor": 450_000.0,
        "fecha_vencimiento": date(2026, 10, 15),
        "estado": "pendiente",
        "nombre_usuario": "ana.restrepo",
    },
    {
        "id_prestamo": UUID("00000000-0000-0000-0000-000000000001"),
        "numero_cuota": 2,
        "valor": 450_000.0,
        "fecha_vencimiento": date(2026, 11, 15),
        "estado": "pendiente",
        "nombre_usuario": "ana.restrepo",
    },
    {
        "id_prestamo": UUID("00000000-0000-0000-0000-000000000001"),
        "numero_cuota": 3,
        "valor": 450_000.0,
        "fecha_vencimiento": date(2026, 12, 15),
        "estado": "pendiente",
        "nombre_usuario": "ana.restrepo",
    },
    {
        "id_prestamo": UUID("00000000-0000-0000-0000-000000000002"),
        "numero_cuota": 1,
        "valor": 275_000.0,
        "fecha_vencimiento": date(2026, 10, 30),
        "estado": "pendiente",
        "nombre_usuario": "carlos.ruiz",
    },
    {
        "id_prestamo": UUID("00000000-0000-0000-0000-000000000002"),
        "numero_cuota": 2,
        "valor": 275_000.0,
        "fecha_vencimiento": date(2026, 11, 30),
        "estado": "pendiente",
        "nombre_usuario": "carlos.ruiz",
    },
    {
        "id_prestamo": UUID("00000000-0000-0000-0000-000000000003"),
        "numero_cuota": 1,
        "valor": 180_000.0,
        "fecha_vencimiento": date(2026, 12, 5),
        "estado": "pagada",
        "nombre_usuario": "laura.mendez",
    },
]


def seed_usuarios(session) -> dict[str, Usuario]:
    usuarios: dict[str, Usuario] = {}
    for datos in USUARIOS_SEED:
        existente = (
            session.query(Usuario)
            .filter_by(nombre_usuario=datos["nombre_usuario"])
            .first()
        )
        if existente:
            print(f"  Usuario '{datos['nombre_usuario']}' ya existe.")
            usuarios[datos["nombre_usuario"]] = existente
            continue

        usuario = Usuario(**datos)
        session.add(usuario)
        usuarios[datos["nombre_usuario"]] = usuario
        print(f"  Usuario '{datos['nombre_usuario']}' creado.")

    session.flush()
    return usuarios


def seed_cuentas(session, usuarios: dict[str, Usuario]) -> dict[str, Cuenta]:
    cuentas: dict[str, Cuenta] = {}
    ahora = datetime.now()
    for datos in CUENTAS_SEED:
        existente = (
            session.query(Cuenta)
            .filter_by(numero_cuenta=datos["numero_cuenta"])
            .first()
        )
        if existente:
            print(f"  Cuenta '{datos['numero_cuenta']}' ya existe.")
            cuentas[datos["numero_cuenta"]] = existente
            continue

        titular = usuarios[datos["nombre_usuario"]]
        cuenta = Cuenta(
            numero_cuenta=datos["numero_cuenta"],
            id_usuario=titular.id_usuario,
            saldo=datos["saldo"],
            estado=datos["estado"],
            fecha_apertura=date.today(),
            id_usuario_creacion=titular.id_usuario,
            fecha_creacion=ahora,
        )
        session.add(cuenta)
        cuentas[datos["numero_cuenta"]] = cuenta
        print(f"  Cuenta '{datos['numero_cuenta']}' creada.")

    session.flush()
    return cuentas


def seed_tarjetas(session, cuentas: dict[str, Cuenta]) -> None:
    fecha_emision = date(2026, 1, 15)
    fecha_vencimiento = date(2030, 1, 31)
    ahora = datetime.now()

    for datos in TARJETAS_SEED:
        existente = (
            session.query(Tarjeta)
            .filter_by(numero_tarjeta=datos["numero_tarjeta"])
            .first()
        )
        if existente:
            print(f"  Tarjeta '{datos['numero_tarjeta']}' ya existe.")
            continue

        cuenta = cuentas[datos["numero_cuenta"]]
        tarjeta = Tarjeta(
            id_cuenta=cuenta.id_cuenta,
            numero_tarjeta=datos["numero_tarjeta"],
            tipo_tarjeta=datos["tipo_tarjeta"],
            fecha_emision=fecha_emision,
            fecha_vencimiento=fecha_vencimiento,
            cvv=datos["cvv"],
            limite_credito=datos["limite_credito"],
            estado=datos["estado"],
            id_usuario_creacion=cuenta.id_usuario,
            fecha_creacion=ahora,
        )
        session.add(tarjeta)
        print(f"  Tarjeta '{datos['numero_tarjeta']}' creada.")


def seed_sucursales(session, usuario_creacion: Usuario) -> dict[str, Sucursal]:
    sucursales: dict[str, Sucursal] = {}
    for datos in SUCURSALES_SEED:
        existente = session.query(Sucursal).filter_by(nombre=datos["nombre"]).first()
        if existente:
            print(f"  Sucursal '{datos['nombre']}' ya existe.")
            sucursales[datos["nombre"]] = existente
            continue

        sucursal = Sucursal(
            **datos,
            id_usuario_creacion=usuario_creacion.id_usuario,
        )
        session.add(sucursal)
        sucursales[datos["nombre"]] = sucursal
        print(f"  Sucursal '{datos['nombre']}' creada.")

    session.flush()
    return sucursales


def seed_empleados(
    session, usuarios: dict[str, Usuario], sucursales: dict[str, Sucursal]
) -> None:
    for datos in EMPLEADOS_SEED:
        usuario = usuarios[datos["nombre_usuario"]]
        sucursal = sucursales[datos["nombre_sucursal"]]
        existente = (
            session.query(Empleado)
            .filter_by(id_usuario=usuario.id_usuario, id_sucursal=sucursal.id_sucursal)
            .first()
        )
        if existente:
            print(f"  Empleado '{datos['nombre_usuario']}' ya existe.")
            continue

        empleado = Empleado(
            id_usuario=usuario.id_usuario,
            id_sucursal=sucursal.id_sucursal,
            cargo=datos["cargo"],
            id_usuario_creacion=usuario.id_usuario,
        )
        session.add(empleado)
        print(f"  Empleado '{datos['nombre_usuario']}' creado.")

    session.flush()


def seed_cuotas(session, usuarios: dict[str, Usuario]) -> None:
    for datos in CUOTAS_SEED:
        usuario = usuarios[datos["nombre_usuario"]]
        existente = (
            session.query(Cuota)
            .filter_by(
                id_prestamo=datos["id_prestamo"],
                numero_cuota=datos["numero_cuota"],
            )
            .first()
        )
        if existente:
            print(
                f"  Cuota {datos['numero_cuota']} del prestamo "
                f"'{datos['id_prestamo']}' ya existe."
            )
            continue

        cuota = Cuota(
            id_prestamo=datos["id_prestamo"],
            numero_cuota=datos["numero_cuota"],
            valor=datos["valor"],
            fecha_vencimiento=datos["fecha_vencimiento"],
            estado=datos["estado"],
            id_usuario_creacion=usuario.id_usuario,
        )
        session.add(cuota)
        print(f"  Cuota {datos['numero_cuota']} creada.")

    session.flush()


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    session = get_session()
    try:
        print("Sembrando usuarios...")
        usuarios = seed_usuarios(session)
        print("Sembrando cuentas...")
        cuentas = seed_cuentas(session, usuarios)
        print("Sembrando tarjetas...")
        seed_tarjetas(session, cuentas)
        print("Sembrando sucursales...")
        sucursales = seed_sucursales(session, usuarios["ana.restrepo"])
        print("Sembrando empleados...")
        seed_empleados(session, usuarios, sucursales)
        print("Sembrando cuotas...")
        seed_cuotas(session, usuarios)
        session.commit()
        print("\nSeeder completado.")
    except Exception:
        session.rollback()
        print("\nError en el seeder. Se revirtio la transaccion.")
        raise
    finally:
        session.close()


seed()
