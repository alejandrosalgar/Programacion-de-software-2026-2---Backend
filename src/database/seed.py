import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import Base, engine, get_session
from entities.cuenta import Cuenta
from entities.Tarjeta import Tarjeta
from entities.usuario import Usuario
from entities.TipoCuenta import TipoCuenta
from entities.Accion import Accion
from entities.sede import Sede

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

TIPOS_CUENTA_SEED = [
    {
        "nombre": "Ahorros",
        "descripcion": "Cuenta de ahorros tradicional",
        "tasa_interes": 2.5,
        "monto_minimo_apertura": 50_000.0,
        "requiere_mantenimiento": False,
        "estado": "Activo",
    },
    {
        "nombre": "Corriente",
        "descripcion": "Cuenta corriente para uso transaccional frecuente",
        "tasa_interes": 0.0,
        "monto_minimo_apertura": 200_000.0,
        "requiere_mantenimiento": True,
        "estado": "Activo",
    },
    {
        "nombre": "Nomina",
        "descripcion": "Cuenta de nómina sin cuota de manejo",
        "tasa_interes": 1.0,
        "monto_minimo_apertura": 0.0,
        "requiere_mantenimiento": False,
        "estado": "Activo",
    },
]

CUENTAS_SEED = [
    {
        "nombre_usuario": "ana.restrepo",
        "numero_cuenta": "1001000001",
        "saldo": 2_500_000.0,
        "estado": "Activa",
        "tipo_cuenta": "Ahorros",
    },
    {
        "nombre_usuario": "carlos.ruiz",
        "numero_cuenta": "1001000002",
        "saldo": 800_000.0,
        "estado": "Activa",
        "tipo_cuenta": "Corriente",
    },
    {
        "nombre_usuario": "laura.mendez",
        "numero_cuenta": "1001000003",
        "saldo": 150_000.0,
        "estado": "Activa",
        "tipo_cuenta": "Nomina",
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

ACCIONES_SEED = [
    {
        "nombre_usuario": "ana.restrepo",
        "tipo_accion": "Login",
        "descripcion": "Inicio de sesión exitoso",
        "ip_origen": "192.168.1.10",
        "resultado": "Exito",
    },
    {
        "nombre_usuario": "carlos.ruiz",
        "tipo_accion": "CrearTarjeta",
        "descripcion": "Creación de tarjeta de crédito",
        "ip_origen": "192.168.1.15",
        "resultado": "Exito",
    },
    {
        "nombre_usuario": "laura.mendez",
        "tipo_accion": "Login",
        "descripcion": "Intento fallido de inicio de sesión",
        "ip_origen": "192.168.1.22",
        "resultado": "Error",
    },
]


SEDES_SEED = [
    {
        "nombre": "Sede Principal Medellin",
        "direccion": "Carrera 50 # 30-40",
        "ciudad": "Medellin",
        "telefono": "6042345678",
        "nombre_usuario_creador": "ana.restrepo",
    },
    {
        "nombre": "Sede Norte Bogota",
        "direccion": "Calle 100 # 15-20",
        "ciudad": "Bogota",
        "telefono": "6013456789",
        "nombre_usuario_creador": "carlos.ruiz",
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


def seed_tipos_cuenta(session, usuarios: dict[str, Usuario]) -> dict[str, TipoCuenta]:
    tipos: dict[str, TipoCuenta] = {}
    usuario_auditoria = next(iter(usuarios.values()))

    for datos in TIPOS_CUENTA_SEED:
        existente = session.query(TipoCuenta).filter_by(nombre=datos["nombre"]).first()
        if existente:
            print(f"  TipoCuenta '{datos['nombre']}' ya existe.")
            tipos[datos["nombre"]] = existente
            continue

        tipo = TipoCuenta(
            nombre=datos["nombre"],
            descripcion=datos["descripcion"],
            tasa_interes=datos["tasa_interes"],
            monto_minimo_apertura=datos["monto_minimo_apertura"],
            requiere_mantenimiento=datos["requiere_mantenimiento"],
            estado=datos["estado"],
            id_usuario_creacion=usuario_auditoria.id_usuario,
            fecha_creacion=date.today(),
        )
        session.add(tipo)
        tipos[datos["nombre"]] = tipo
        print(f"  TipoCuenta '{datos['nombre']}' creado.")

    session.flush()
    return tipos


def seed_cuentas(
    session, usuarios: dict[str, Usuario], tipos_cuenta: dict[str, TipoCuenta]
) -> dict[str, Cuenta]:
def seed_cuentas(session, usuarios: dict[str, Usuario]) -> dict[str, Cuenta]:
    cuentas: dict[str, Cuenta] = {}
    ahora = datetime.now()
    for datos in CUENTAS_SEED:
        existente = (
            session.query(Cuenta)
            .filter_by(numero_cuenta=datos["numero_cuenta"])
            .first()
            session.query(Cuenta).filter_by(numero_cuenta=datos["numero_cuenta"]).first()
        )
        if existente:
            print(f"  Cuenta '{datos['numero_cuenta']}' ya existe.")
            cuentas[datos["numero_cuenta"]] = existente
            continue

        titular = usuarios[datos["nombre_usuario"]]
        tipo_cuenta = tipos_cuenta[datos["tipo_cuenta"]]
        cuenta = Cuenta(
            numero_cuenta=datos["numero_cuenta"],
            id_usuario=titular.id_usuario,
            id_tipo_cuenta=tipo_cuenta.id_tipo_cuenta,
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
        print(
            f"  Cuenta '{datos['numero_cuenta']}' creada (tipo: {datos['tipo_cuenta']})."
        )
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

    session.flush()


def seed_acciones(session, usuarios: dict[str, Usuario]) -> None:
    for datos in ACCIONES_SEED:
        usuario = usuarios[datos["nombre_usuario"]]

        existente = (
            session.query(Accion)
            .filter_by(
                id_usuario=usuario.id_usuario,
                tipo_accion=datos["tipo_accion"],
                ip_origen=datos["ip_origen"],
            )
            .first()
        )
        if existente:
            print(
                f"  Accion '{datos['tipo_accion']}' para '{datos['nombre_usuario']}' ya existe."
            )
            continue

        accion = Accion(
            id_usuario=usuario.id_usuario,
            tipo_accion=datos["tipo_accion"],
            descripcion=datos["descripcion"],
            ip_origen=datos["ip_origen"],
            resultado=datos["resultado"],
            fecha_accion=date.today(),
        )
        session.add(accion)
        print(
            f"  Accion '{datos['tipo_accion']}' para '{datos['nombre_usuario']}' creada."
        )

    session.flush()


def seed_sedes(session, usuarios: dict[str, Usuario]) -> None:
    for datos in SEDES_SEED:
        existente = session.query(Sede).filter_by(nombre=datos["nombre"]).first()
        if existente:
            print(f"  Sede '{datos['nombre']}' ya existe.")
            continue

        usuario_creador = usuarios[datos["nombre_usuario_creador"]]

        sede = Sede(
            nombre=datos["nombre"],
            direccion=datos["direccion"],
            ciudad=datos["ciudad"],
            telefono=datos["telefono"],
            id_usuario_creacion=usuario_creador.id_usuario,
            fecha_creacion=date.today(),
        )
        session.add(sede)
        print(f"  Sede '{datos['nombre']}' creada.")

    session.flush()


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    session = get_session()
    try:
        print("Sembrando usuarios...")
        usuarios = seed_usuarios(session)

        print("Sembrando tipos de cuenta...")
        tipos_cuenta = seed_tipos_cuenta(session, usuarios)

        print("Sembrando cuentas...")
        cuentas = seed_cuentas(session, usuarios, tipos_cuenta)

        print("Sembrando tarjetas...")
        seed_tarjetas(session, cuentas)

        print("Sembrando acciones...")
        seed_acciones(session, usuarios)

        print("Sembrando sedes...")
        seed_sedes(session, usuarios)

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
