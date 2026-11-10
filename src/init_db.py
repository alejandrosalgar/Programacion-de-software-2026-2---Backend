from database.connection import Base, engine
from entities.Accion import Accion
from entities.TipoCuenta import TipoCuenta
from entities.Tarjeta import Tarjeta
from entities.cuenta import Cuenta
from entities.cuota import Cuota
from entities.empleado import Empleado
from entities.sede import Sede
from entities.sucursal import Sucursal
from entities.usuario import Usuario

if __name__ == "__main__":
    from database.seed import seed

    resultado = seed()
    print("Tablas listas y datos semilla completados:")
    for entidad, total in resultado.items():
        print(f"  {entidad}: {total}")
