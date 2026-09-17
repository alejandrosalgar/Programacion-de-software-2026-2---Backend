from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.TipoCuenta import TipoCuenta


class TipoCuentaCRUD:
    """
    Módulo CRUD para la entidad TipoCuenta.
    Permite gestionar los tipos de cuenta que existen en el sistema
    (ahorros, corriente, nómina, etc.).

    Funciones principales:
        - crear_tipo_cuenta(db: Session, tipo: TipoCuenta) -> TipoCuenta
        - obtener_tipo_cuenta(db: Session, id_tipo_cuenta: UUID) -> TipoCuenta
        - obtener_tipos_cuenta(db: Session) -> List[TipoCuenta]
        - actualizar_tipo_cuenta(db: Session, id_tipo_cuenta: UUID, **kwargs) -> TipoCuenta
        - eliminar_tipo_cuenta(db: Session, id_tipo_cuenta: UUID) -> bool

    Notas:
        - Se valida que no se repitan tipos de cuenta con el mismo nombre.
    """

    def __init__(self, db):
        self.db = db

    @staticmethod
    def crear_tipo_cuenta(db: Session, tipo: TipoCuenta):
        if not tipo.nombre or not tipo.nombre.strip():
            raise ValueError("El nombre del tipo de cuenta no puede estar vacío")

        existente = (
            db.query(TipoCuenta).filter(TipoCuenta.nombre == tipo.nombre).first()
        )
        if existente:
            raise ValueError("El tipo de cuenta ya existe")

        db.add(tipo)
        db.commit()
        db.refresh(tipo)
        return tipo

    @staticmethod
    def obtener_tipo_cuenta(db: Session, id_tipo_cuenta: UUID):
        tipo = (
            db.query(TipoCuenta)
            .filter(TipoCuenta.id_tipo_cuenta == id_tipo_cuenta)
            .first()
        )
        if not tipo:
            raise ValueError("Tipo de cuenta no encontrado")
        return tipo

    @staticmethod
    def obtener_tipos_cuenta(db: Session):
        return db.query(TipoCuenta).all()

    @staticmethod
    def actualizar_tipo_cuenta(
        db: Session, id_tipo_cuenta: UUID, id_usuario_edicion: UUID = None, **kwargs
    ):
        tipo = (
            db.query(TipoCuenta)
            .filter(TipoCuenta.id_tipo_cuenta == id_tipo_cuenta)
            .first()
        )
        if not tipo:
            raise ValueError("Tipo de cuenta no encontrado")

        # kwargs esperados: nombre, descripcion, tasa_interes,
        # monto_minimo_apertura, requiere_mantenimiento, estado
        if "nombre" in kwargs and kwargs["nombre"] is not None:
            nuevo_nombre = kwargs["nombre"]
            if not nuevo_nombre.strip():
                raise ValueError("El nombre del tipo de cuenta no puede estar vacío")
            duplicado = (
                db.query(TipoCuenta)
                .filter(
                    TipoCuenta.nombre == nuevo_nombre,
                    TipoCuenta.id_tipo_cuenta != id_tipo_cuenta,
                )
                .first()
            )
            if duplicado:
                raise ValueError("Ya existe otro tipo de cuenta con ese nombre")

        for campo, valor in kwargs.items():
            if valor is None:
                continue
            if not hasattr(tipo, campo):
                raise ValueError(f"El campo '{campo}' no existe en TipoCuenta")
            setattr(tipo, campo, valor)

        if id_usuario_edicion is not None:
            tipo.registrar_edicion(id_usuario_edicion)

        db.commit()
        db.refresh(tipo)
        return tipo

    @staticmethod
    def eliminar_tipo_cuenta(db: Session, id_tipo_cuenta: UUID) -> bool:
        tipo = (
            db.query(TipoCuenta)
            .filter(TipoCuenta.id_tipo_cuenta == id_tipo_cuenta)
            .first()
        )
        if not tipo:
            raise ValueError("Tipo de cuenta no encontrado")

        db.delete(tipo)
        db.commit()
        return True
