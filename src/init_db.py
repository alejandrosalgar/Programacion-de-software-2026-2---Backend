from database.connection import Base, engine
from entities.usuario import Usuario

Base.metadata.create_all(bind=engine)
