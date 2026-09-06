from database.connection import Base, engine
from entities.cuenta import Cuenta
from entities.Tarjeta import Tarjeta
from entities.usuario import Usuario

Base.metadata.create_all(bind=engine)
