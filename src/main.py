import os
import sys
from getpass import getpass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from crud import sede as sede_crud
from crud import usuario as usuario_crud
from crud import TipoCuenta_crud as tipo_cuenta_crud
from crud import Tarjeta_crud as tarjeta_crud
from crud import Accion_crud as accion_crud
from crud import cuota as cuota_crud
from crud import empleado as empleado_crud
from crud import sucursal as sucursal_crud
from crud import beneficiario as beneficiario_crud
from crud import cuenta as cuenta_crud

sesion = None


def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    input("\nPresione Enter para continuar...")


def titulo(texto: str) -> None:
    print("=" * 50)
    print(texto.center(50))
    print("=" * 50)


def leer_texto(etiqueta: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(f"{etiqueta}: ").strip()
        if valor or not obligatorio:
            return valor
        print("Este campo es obligatorio.")


def leer_float(etiqueta: str, obligatorio: bool = True) -> float | None:
    while True:
        valor = input(f"{etiqueta}: ").strip()
        if not valor and not obligatorio:
            return None
        try:
            return float(valor)
        except ValueError:
            print("Ingrese un numero valido.")


def mostrar_usuario(usuario) -> None:
    print(usuario)


def mostrar_sede(sede) -> None:
    print("-" * 50)
    print(sede)
    print("-" * 50)


def crear_usuario() -> None:
    limpiar_pantalla()
    titulo("CREAR USUARIO")

    primer_nombre = leer_texto("Primer nombre")
    segundo_nombre = leer_texto("Segundo nombre", obligatorio=False)
    primer_apellido = leer_texto("Primer apellido")
    segundo_apellido = leer_texto("Segundo apellido", obligatorio=False)
    nombre_usuario = leer_texto("Nombre de usuario")
    clave = getpass("Clave: ").strip()
    if not clave:
        print("\nLa clave es obligatoria.")
        pausar()
        return

    confirmacion = getpass("Confirmar clave: ").strip()
    if clave != confirmacion:
        print("\nLas claves no coinciden.")
        pausar()
        return

    usuario = usuario_crud.crear(
        primer_nombre=primer_nombre,
        segundo_nombre=segundo_nombre,
        primer_apellido=primer_apellido,
        segundo_apellido=segundo_apellido,
        nombre_usuario=nombre_usuario,
        clave=clave,
    )
    if usuario is None:
        print("\nYa existe un usuario con ese nombre de usuario.")
        pausar()
        return

    print("\nUsuario creado correctamente.")
    mostrar_usuario(usuario)
    pausar()


def iniciar_sesion() -> None:
    global sesion
    limpiar_pantalla()
    titulo("INICIAR SESION")

    nombre_usuario = leer_texto("Nombre de usuario")
    clave = getpass("Clave: ").strip()
    sesion = usuario_crud.obtener(nombre_usuario, clave)

    if sesion is None:
        print("\nNombre de usuario o clave incorrectos.")
        pausar()
        return

    print(f"\nBienvenido, {sesion.nombre_completo()}.")
    pausar()
    menu_entidades()


# --- SEDES ---
def listar_sedes() -> None:
    limpiar_pantalla()
    titulo("LISTAR SEDES")
    sedes = sede_crud.listar()
    if not sedes:
        print("No hay sedes registradas.")
        pausar()
        return
    for indice, sede in enumerate(sedes, start=1):
        print(f"{indice}. {sede.nombre} | {sede.ciudad} | {sede.id_sede}")
        mostrar_sede(sede)
    pausar()


def seleccionar_sede():
    sedes = sede_crud.listar()
    if not sedes:
        print("No hay sedes registradas.")
        return None
    print("\nSedes disponibles:")
    for indice, sede in enumerate(sedes, start=1):
        print(f"{indice}. {sede.nombre} ({sede.ciudad})")
    opcion = leer_texto("Seleccione el numero de la sede")
    if not opcion.isdigit():
        print("Opcion invalida.")
        return None
    indice = int(opcion) - 1
    if indice < 0 or indice >= len(sedes):
        print("Opcion invalida.")
        return None
    return sedes[indice]


def crear_sede() -> None:
    limpiar_pantalla()
    titulo("CREAR SEDE")
    if sesion is None:
        print("Debe iniciar sesion para crear una sede.")
        pausar()
        return
    nombre = leer_texto("Nombre")
    direccion = leer_texto("Direccion")
    ciudad = leer_texto("Ciudad")
    telefono = leer_texto("Telefono")
    sede = sede_crud.crear(
        nombre=nombre,
        direccion=direccion,
        ciudad=ciudad,
        telefono=telefono,
        id_usuario_creacion=sesion.id_usuario,
    )
    print("\nSede creada correctamente.")
    mostrar_sede(sede)
    pausar()


def ver_sede() -> None:
    limpiar_pantalla()
    titulo("VER SEDE")
    seleccion = seleccionar_sede()
    if seleccion is None:
        pausar()
        return
    sede = sede_crud.obtener(seleccion.id_sede)
    if sede is None:
        print("No se encontro la sede.")
        pausar()
        return
    print("\nDetalle de la sede:")
    mostrar_sede(sede)
    pausar()


def editar_sede() -> None:
    limpiar_pantalla()
    titulo("EDITAR SEDE")
    if sesion is None:
        print("Debe iniciar sesion para editar una sede.")
        pausar()
        return
    seleccion = seleccionar_sede()
    if seleccion is None:
        pausar()
        return
    sede = sede_crud.obtener(seleccion.id_sede)
    if sede is None:
        print("No se encontro la sede.")
        pausar()
        return
    print("\nDeje el campo vacio para conservar el valor actual.\n")
    nombre = leer_texto(f"Nombre [{sede.nombre}]", obligatorio=False)
    direccion = leer_texto(f"Direccion [{sede.direccion}]", obligatorio=False)
    ciudad = leer_texto(f"Ciudad [{sede.ciudad}]", obligatorio=False)
    telefono = leer_texto(f"Telefono [{sede.telefono}]", obligatorio=False)
    actualizado = sede_crud.actualizar(
        id_sede=sede.id_sede,
        id_usuario_edicion=sesion.id_usuario,
        nombre=nombre or None,
        direccion=direccion or None,
        ciudad=ciudad or None,
        telefono=telefono or None,
    )
    if actualizado is None:
        print("No se pudo actualizar la sede.")
        pausar()
        return
    print("\nSede actualizada correctamente.")
    mostrar_sede(actualizado)
    pausar()


def eliminar_sede() -> None:
    limpiar_pantalla()
    titulo("ELIMINAR SEDE")
    seleccion = seleccionar_sede()
    if seleccion is None:
        pausar()
        return
    confirmacion = leer_texto(f"¿Eliminar la sede '{seleccion.nombre}'? (s/n)").lower()
    if confirmacion != "s":
        print("Operacion cancelada.")
        pausar()
        return
    if not sede_crud.eliminar(seleccion.id_sede):
        print("No se pudo eliminar la sede.")
        pausar()
        return
    print("Sede eliminada correctamente.")
    pausar()


def menu_sedes() -> None:
    while True:
        limpiar_pantalla()
        titulo("CRUD SEDES")
        print("1. Listar sedes")
        print("2. Crear sede")
        print("3. Ver sede")
        print("4. Editar sede")
        print("5. Eliminar sede")
        print("0. Volver")

        opcion = leer_texto("\nSeleccione una opcion")
        if opcion == "1":
            listar_sedes()
        elif opcion == "2":
            crear_sede()
        elif opcion == "3":
            ver_sede()
        elif opcion == "4":
            editar_sede()
        elif opcion == "5":
            eliminar_sede()
        elif opcion == "0":
            return
        else:
            print("Opcion invalida.")
            pausar()


# --- CUENTAS ---
def mostrar_cuenta(cuenta) -> None:
    print("-" * 50)
    print(cuenta)
    print("-" * 50)


def listar_cuentas() -> None:
    limpiar_pantalla()
    titulo("LISTAR CUENTAS")
    cuentas = cuenta_crud.listar()
    if not cuentas:
        print("No hay cuentas registradas.")
        pausar()
        return
    for indice, cuenta in enumerate(cuentas, start=1):
        print(f"{indice}. {cuenta.numero_cuenta} | {cuenta.estado} | {cuenta.saldo}")
        mostrar_cuenta(cuenta)
    pausar()


def seleccionar_cuenta():
    cuentas = cuenta_crud.listar()
    if not cuentas:
        print("No hay cuentas registradas.")
        return None
    print("\nCuentas disponibles:")
    for indice, cuenta in enumerate(cuentas, start=1):
        print(f"{indice}. {cuenta.numero_cuenta} ({cuenta.estado})")
    opcion = leer_texto("Seleccione el numero de la cuenta")
    if not opcion.isdigit():
        print("Opcion invalida.")
        return None
    indice = int(opcion) - 1
    if indice < 0 or indice >= len(cuentas):
        print("Opcion invalida.")
        return None
    return cuentas[indice]


def crear_cuenta() -> None:
    limpiar_pantalla()
    titulo("CREAR CUENTA")
    if sesion is None:
        print("Debe iniciar sesion para crear una cuenta.")
        pausar()
        return
    numero_cuenta = leer_texto("Numero de cuenta")
    saldo = leer_float("Saldo inicial", obligatorio=False)
    estado = leer_texto("Estado [Activa]", obligatorio=False) or "Activa"
    cuenta = cuenta_crud.crear(
        numero_cuenta=numero_cuenta,
        id_usuario=sesion.id_usuario,
        id_usuario_creacion=sesion.id_usuario,
        saldo=0.0 if saldo is None else saldo,
        estado=estado,
    )
    if cuenta is None:
        print("\nNo se pudo crear la cuenta. Verifique que el numero no este repetido.")
        pausar()
        return
    print("\nCuenta creada correctamente.")
    mostrar_cuenta(cuenta)
    pausar()


def ver_cuenta() -> None:
    limpiar_pantalla()
    titulo("VER CUENTA")
    seleccion = seleccionar_cuenta()
    if seleccion is None:
        pausar()
        return
    cuenta = cuenta_crud.obtener(seleccion.id_cuenta)
    if cuenta is None:
        print("No se encontro la cuenta.")
        pausar()
        return
    print("\nDetalle de la cuenta:")
    mostrar_cuenta(cuenta)
    pausar()


def editar_cuenta() -> None:
    limpiar_pantalla()
    titulo("EDITAR CUENTA")
    if sesion is None:
        print("Debe iniciar sesion para editar una cuenta.")
        pausar()
        return
    seleccion = seleccionar_cuenta()
    if seleccion is None:
        pausar()
        return
    cuenta = cuenta_crud.obtener(seleccion.id_cuenta)
    if cuenta is None:
        print("No se encontro la cuenta.")
        pausar()
        return
    print("\nDeje el campo vacio para conservar el valor actual.\n")
    numero_cuenta = leer_texto(
        f"Numero de cuenta [{cuenta.numero_cuenta}]", obligatorio=False
    )
    saldo = leer_float(f"Saldo [{cuenta.saldo}]", obligatorio=False)
    estado = leer_texto(f"Estado [{cuenta.estado}]", obligatorio=False)
    actualizado = cuenta_crud.actualizar(
        id_cuenta=cuenta.id_cuenta,
        id_usuario_edicion=sesion.id_usuario,
        numero_cuenta=numero_cuenta or None,
        saldo=saldo,
        estado=estado or None,
    )
    if actualizado is None:
        print("No se pudo actualizar la cuenta.")
        pausar()
        return
    print("\nCuenta actualizada correctamente.")
    mostrar_cuenta(actualizado)
    pausar()


def eliminar_cuenta() -> None:
    limpiar_pantalla()
    titulo("ELIMINAR CUENTA")
    seleccion = seleccionar_cuenta()
    if seleccion is None:
        pausar()
        return
    confirmacion = leer_texto(
        f"¿Eliminar la cuenta '{seleccion.numero_cuenta}'? (s/n)"
    ).lower()
    if confirmacion != "s":
        print("Operacion cancelada.")
        pausar()
        return
    if not cuenta_crud.eliminar(seleccion.id_cuenta):
        print("No se pudo eliminar la cuenta.")
        pausar()
        return
    print("Cuenta eliminada correctamente.")
    pausar()


def menu_cuentas() -> None:
    while True:
        limpiar_pantalla()
        titulo("CRUD CUENTAS")
        print("1. Listar cuentas")
        print("2. Crear cuenta")
        print("3. Ver cuenta")
        print("4. Editar cuenta")
        print("5. Eliminar cuenta")
        print("0. Volver")

        opcion = leer_texto("\nSeleccione una opcion")
        if opcion == "1":
            listar_cuentas()
        elif opcion == "2":
            crear_cuenta()
        elif opcion == "3":
            ver_cuenta()
        elif opcion == "4":
            editar_cuenta()
        elif opcion == "5":
            eliminar_cuenta()
        elif opcion == "0":
            return
        else:
            print("Opcion invalida.")
            pausar()


# --- CUOTAS ---
def menu_cuotas() -> None:
    while True:
        limpiar_pantalla()
        titulo("CRUD CUOTAS")
        print("1. Listar cuotas")
        print("0. Volver")
        opcion = leer_texto("\nSeleccione una opcion")
        if opcion == "1":
            limpiar_pantalla()
            titulo("LISTAR CUOTAS")
            cuotas = cuota_crud.listar() if hasattr(cuota_crud, 'listar') else []
            if not cuotas:
                print("No hay cuotas registradas.")
            else:
                for c in cuotas:
                    print(c)
            pausar()
        elif opcion == "0":
            return


# --- SUCURSALES ---
def menu_sucursales() -> None:
    while True:
        limpiar_pantalla()
        titulo("CRUD SUCURSALES")
        print("1. Listar sucursales")
        print("0. Volver")
        opcion = leer_texto("\nSeleccione una opcion")
        if opcion == "1":
            limpiar_pantalla()
            titulo("LISTAR SUCURSALES")
            sucursales = sucursal_crud.listar() if hasattr(sucursal_crud, 'listar') else []
            if not sucursales:
                print("No hay sucursales registradas.")
            else:
                for s in sucursales:
                    print(s)
            pausar()
        elif opcion == "0":
            return


# --- EMPLEADOS ---
def menu_empleados() -> None:
    while True:
        limpiar_pantalla()
        titulo("CRUD EMPLEADOS")
        print("1. Listar empleados")
        print("0. Volver")
        opcion = leer_texto("\nSeleccione una opcion")
        if opcion == "1":
            limpiar_pantalla()
            titulo("LISTAR EMPLEADOS")
            empleados = empleado_crud.listar() if hasattr(empleado_crud, 'listar') else []
            if not empleados:
                print("No hay empleados registrados.")
            else:
                for e in empleados:
                    print(e)
            pausar()
        elif opcion == "0":
            return


# --- BENEFICIARIOS ---
def menu_beneficiarios() -> None:
    while True:
        limpiar_pantalla()
        titulo("CRUD BENEFICIARIOS")
        print("1. Listar beneficiarios")
        print("0. Volver")
        opcion = leer_texto("\nSeleccione una opcion")
        if opcion == "1":
            limpiar_pantalla()
            titulo("LISTAR BENEFICIARIOS")
            beneficiarios = beneficiario_crud.listar() if hasattr(beneficiario_crud, 'listar') else []
            if not beneficiarios:
                print("No hay beneficiarios registrados.")
            else:
                for b in beneficiarios:
                    print(b)
            pausar()
        elif opcion == "0":
            return


def menu_entidades() -> None:
    global sesion
    while sesion is not None:
        limpiar_pantalla()
        titulo("ENTIDADES")
        print(f"Sesion: {sesion.nombre_usuario}")
        print("\n1. Sedes")
        print("2. Cuotas")
        print("3. Sucursales")
        print("4. Empleados")
        print("5. Beneficiarios")
        print("6. Cuentas")
        print("0. Cerrar sesion")

        opcion = leer_texto("\nSeleccione una opcion")
        if opcion == "1":
            menu_sedes()
        elif opcion == "2":
            menu_cuotas()
        elif opcion == "3":
            menu_sucursales()
        elif opcion == "4":
            menu_empleados()
        elif opcion == "5":
            menu_beneficiarios()
        elif opcion == "6":
            menu_cuentas()
        elif opcion == "0":
            sesion = None
            return
        else:
            print("Opcion invalida.")
            pausar()


def menu_principal() -> None:
    global sesion
    while True:
        sesion = None
        limpiar_pantalla()
        titulo("SISTEMA DE GESTION")
        print("1. Iniciar sesion")
        print("2. Crear usuario")
        print("0. Salir")

        opcion = leer_texto("\nSeleccione una opcion")
        if opcion == "1":
            iniciar_sesion()
        elif opcion == "2":
            crear_usuario()
        elif opcion == "0":
            print("\nHasta luego.")
            return
        else:
            print("Opcion invalida.")
            pausar()


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma finalizado.")
