from database.connection import Base, engine
from entities.TipoCuenta import TipoCuenta
from entities.Tarjeta import Tarjeta
from entities.Accion import Accion

Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente en Neon")
