from database.connection import Base, engine
from entities.cuenta import Cuenta
from entities.Tarjeta import Tarjeta
from entities.usuario import Usuario
from entities.cuota import Cuota
from entities.sucursal import Sucursal
from entities.empleado import Empleado

Base.metadata.create_all(bind=engine)
print("Las tablas ya estan creadas correctamente.")
