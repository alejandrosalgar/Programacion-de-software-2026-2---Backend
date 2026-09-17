from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.Tarjeta import Tarjeta


class TarjetaCRUD:
    """
    Módulo CRUD para la entidad Tarjeta.
    Permite gestionar las tarjetas (débito/crédito) asociadas a una cuenta.

    Funciones principales:
        - crear_tarjeta(db: Session, tarjeta: Tarjeta) -> Tarjeta
        - obtener_tarjeta(db: Session, id_tarjeta: UUID) -> Tarjeta
        - obtener_tarjetas(db: Session) -> List[Tarjeta]
        - obtener_tarjetas_por_cuenta(db: Session, id_cuenta: UUID) -> List[Tarjeta]
        - actualizar_tarjeta(db: Session, id_tarjeta: UUID, **kwargs) -> Tarjeta
        - eliminar_tarjeta(db: Session, id_tarjeta: UUID) -> bool

    Notas:
        - Se valida que no se repita el número de tarjeta.
        - Se aprovechan los métodos de negocio del modelo (bloquear,
          activar, esta_vencida, tiene_cupo_disponible).
    """

    def __init__(self, db):
        self.db = db

    @staticmethod
    def crear_tarjeta(db: Session, tarjeta: Tarjeta):
        if not tarjeta.numero_tarjeta or not tarjeta.numero_tarjeta.strip():
            raise ValueError("El número de la tarjeta no puede estar vacío")

        existente = (
            db.query(Tarjeta)
            .filter(Tarjeta.numero_tarjeta == tarjeta.numero_tarjeta)
            .first()
        )
        if existente:
            raise ValueError("La tarjeta ya existe")

        db.add(tarjeta)
        db.commit()
        db.refresh(tarjeta)
        return tarjeta

    @staticmethod
    def obtener_tarjeta(db: Session, id_tarjeta: UUID):
        tarjeta = db.query(Tarjeta).filter(Tarjeta.id_tarjeta == id_tarjeta).first()
        if not tarjeta:
            raise ValueError("Tarjeta no encontrada")
        return tarjeta

    @staticmethod
    def obtener_tarjetas(db: Session):
        return db.query(Tarjeta).all()

    @staticmethod
    def obtener_tarjetas_por_cuenta(db: Session, id_cuenta: UUID):
        return db.query(Tarjeta).filter(Tarjeta.id_cuenta == id_cuenta).all()

    @staticmethod
    def actualizar_tarjeta(
        db: Session, id_tarjeta: UUID, id_usuario_edicion: UUID = None, **kwargs
    ):
        tarjeta = db.query(Tarjeta).filter(Tarjeta.id_tarjeta == id_tarjeta).first()
        if not tarjeta:
            raise ValueError("Tarjeta no encontrada")

        # kwargs esperados: numero_tarjeta, tipo_tarjeta, fecha_vencimiento,
        # cvv, limite_credito, estado, id_cuenta
        for campo, valor in kwargs.items():
            if valor is None:
                continue
            if not hasattr(tarjeta, campo):
                raise ValueError(f"El campo '{campo}' no existe en Tarjeta")
            setattr(tarjeta, campo, valor)

        if id_usuario_edicion is not None:
            tarjeta.registrar_edicion(id_usuario_edicion)

        db.commit()
        db.refresh(tarjeta)
        return tarjeta

    @staticmethod
    def eliminar_tarjeta(db: Session, id_tarjeta: UUID) -> bool:
        tarjeta = db.query(Tarjeta).filter(Tarjeta.id_tarjeta == id_tarjeta).first()
        if not tarjeta:
            raise ValueError("Tarjeta no encontrada")

        db.delete(tarjeta)
        db.commit()
        return True
