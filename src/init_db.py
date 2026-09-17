from database.connection import Base, engine
from entities.TipoCuenta import TipoCuenta
from entities.Tarjeta import Tarjeta
from entities.Accion import Accion
from entities.cuenta import Cuenta
from entities.usuario import Usuario
from entities.cuota import Cuota
from entities.sucursal import Sucursal
from entities.empleado import Empleado
from entities.sede import Sede

Base.metadata.create_all(bind=engine)
print("Las tablas ya estan creadas correctamente.")
