from database.connection import Base, engine
from entities.TipoCuenta import TipoCuenta
from entities.Tarjeta import Tarjeta
from entities.Accion import Accion
from entities.cuenta import Cuenta
from entities.usuario import Usuario
from entities.sede import Sede

Base.metadata.create_all(bind=engine)
