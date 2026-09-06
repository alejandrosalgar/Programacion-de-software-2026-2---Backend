import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import Base, engine, get_session
from entities.cuenta import Cuenta
from entities.Tarjeta import Tarjeta
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
            session.query(Cuenta).filter_by(numero_cuenta=datos["numero_cuenta"]).first()
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
        session.commit()
        print("\nSeeder completado.")
    except Exception:
        session.rollback()
        print("\nError en el seeder. Se revirtio la transaccion.")
        raise
    finally:
        session.close()



seed()
