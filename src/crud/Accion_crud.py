from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.Accion import Accion


class AccionCRUD:
    """
    Módulo CRUD para la entidad Accion.
    Permite registrar y consultar los eventos de auditoría generados
    por las acciones de los usuarios en el sistema.

    Funciones principales:
        - crear_accion(db: Session, accion: Accion) -> Accion
        - obtener_accion(db: Session, id_accion: UUID) -> Accion
        - obtener_acciones(db: Session) -> List[Accion]
        - obtener_acciones_por_usuario(db: Session, id_usuario: UUID) -> List[Accion]
        - actualizar_accion(db: Session, id_accion: UUID, **kwargs) -> Accion
        - eliminar_accion(db: Session, id_accion: UUID) -> bool

    Notas:
        - Se valida que exista un tipo_accion definido.
        - Los registros de auditoría normalmente no se editan ni eliminan
          en un sistema real; se dejan estas operaciones por completitud
          del CRUD que exige el examen.
    """

    def __init__(self, db):
        self.db = db

    @staticmethod
    def crear_accion(db: Session, accion: Accion):
        if not accion.tipo_accion or not accion.tipo_accion.strip():
            raise ValueError("El tipo de acción no puede estar vacío")

        db.add(accion)
        db.commit()
        db.refresh(accion)
        return accion

    @staticmethod
    def obtener_accion(db: Session, id_accion: UUID):
        accion = db.query(Accion).filter(Accion.id_accion == id_accion).first()
        if not accion:
            raise ValueError("Acción no encontrada")
        return accion

    @staticmethod
    def obtener_acciones(db: Session):
        return db.query(Accion).all()

    @staticmethod
    def obtener_acciones_por_usuario(db: Session, id_usuario: UUID):
        return db.query(Accion).filter(Accion.id_usuario == id_usuario).all()

    @staticmethod
    def actualizar_accion(db: Session, id_accion: UUID, **kwargs):
        accion = db.query(Accion).filter(Accion.id_accion == id_accion).first()
        if not accion:
            raise ValueError("Acción no encontrada")

        # kwargs esperados: tipo_accion, descripcion, ip_origen, resultado
        for campo, valor in kwargs.items():
            if valor is None:
                continue
            if not hasattr(accion, campo):
                raise ValueError(f"El campo '{campo}' no existe en Accion")
            setattr(accion, campo, valor)

        db.commit()
        db.refresh(accion)
        return accion

    @staticmethod
    def eliminar_accion(db: Session, id_accion: UUID) -> bool:
        accion = db.query(Accion).filter(Accion.id_accion == id_accion).first()
        if not accion:
            raise ValueError("Acción no encontrada")

        db.delete(accion)
        db.commit()
        return True
