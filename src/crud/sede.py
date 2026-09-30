from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.sede import Sede


class SedeCRUD:
    """
    Módulo CRUD para la entidad Sede.
    Permite gestionar las sedes físicas registradas en el sistema.
    """

    def __init__(self, db):
        self.db = db

    @staticmethod
    def crear_sede(db: Session, sede: Sede):
        if not sede.nombre or not sede.nombre.strip():
            raise ValueError("El nombre de la sede no puede estar vacío")

        existente = db.query(Sede).filter(Sede.nombre == sede.nombre).first()
        if existente:
            raise ValueError("Ya existe una sede con ese nombre")

        db.add(sede)
        db.commit()
        db.refresh(sede)
        return sede

    @staticmethod
    def obtener_sede(db: Session, id_sede: UUID):
        sede = db.query(Sede).filter(Sede.id_sede == id_sede).first()
        if not sede:
            raise ValueError("Sede no encontrada")
        return sede

    @staticmethod
    def obtener_sedes(db: Session):
        return db.query(Sede).all()

    @staticmethod
    def actualizar_sede(
        db: Session, id_sede: UUID, id_usuario_edicion: UUID = None, **kwargs
    ):
        sede = db.query(Sede).filter(Sede.id_sede == id_sede).first()
        if not sede:
            raise ValueError("Sede no encontrada")

        # kwargs esperados: nombre, direccion, ciudad, telefono
        for campo, valor in kwargs.items():
            if valor is None:
                continue
            if not hasattr(sede, campo):
                raise ValueError(f"El campo '{campo}' no existe en Sede")
            setattr(sede, campo, valor)

        if id_usuario_edicion is not None:
            sede.registrar_edicion(id_usuario_edicion)

        db.commit()
        db.refresh(sede)
        return sede

    @staticmethod
    def eliminar_sede(db: Session, id_sede: UUID) -> bool:
        sede = db.query(Sede).filter(Sede.id_sede == id_sede).first()
        if not sede:
            raise ValueError("Sede no encontrada")

        db.delete(sede)
        db.commit()
        return True
