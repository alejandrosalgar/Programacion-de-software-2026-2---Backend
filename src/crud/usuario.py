from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.usuario import Usuario


class UsuarioCRUD:
    """
    Módulo CRUD para la entidad Usuario.
    Permite gestionar los usuarios del sistema y autenticarlos.

    Notas:
        - Se valida que no se repita el nombre de usuario (comparación
          insensible a mayúsculas/minúsculas, igual que la versión anterior).
    """

    def __init__(self, db):
        self.db = db

    @staticmethod
    def crear_usuario(db: Session, usuario: Usuario):
        if not usuario.nombre_usuario or not usuario.nombre_usuario.strip():
            raise ValueError("El nombre de usuario no puede estar vacío")

        existente = (
            db.query(Usuario)
            .filter(
                func.lower(Usuario.nombre_usuario)
                == usuario.nombre_usuario.strip().lower()
            )
            .first()
        )
        if existente:
            raise ValueError("Ya existe un usuario con ese nombre de usuario")

        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def obtener_usuario(db: Session, id_usuario: UUID):
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario

    @staticmethod
    def obtener_usuario_por_nombre(db: Session, nombre_usuario: str):
        usuario = (
            db.query(Usuario)
            .filter(
                func.lower(Usuario.nombre_usuario) == nombre_usuario.strip().lower()
            )
            .first()
        )
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario

    @staticmethod
    def obtener_usuarios(db: Session):
        return db.query(Usuario).all()

    @staticmethod
    def actualizar_usuario(db: Session, id_usuario: UUID, **kwargs):
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            raise ValueError("Usuario no encontrado")

        if "nombre_usuario" in kwargs and kwargs["nombre_usuario"] is not None:
            nuevo_nombre = kwargs["nombre_usuario"]
            duplicado = (
                db.query(Usuario)
                .filter(
                    func.lower(Usuario.nombre_usuario) == nuevo_nombre.strip().lower(),
                    Usuario.id_usuario != id_usuario,
                )
                .first()
            )
            if duplicado:
                raise ValueError("Ya existe otro usuario con ese nombre de usuario")

        for campo, valor in kwargs.items():
            if valor is None:
                continue
            if not hasattr(usuario, campo):
                raise ValueError(f"El campo '{campo}' no existe en Usuario")
            setattr(usuario, campo, valor.strip() if isinstance(valor, str) else valor)

        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def eliminar_usuario(db: Session, id_usuario: UUID) -> bool:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            raise ValueError("Usuario no encontrado")

        db.delete(usuario)
        db.commit()
        return True

    @staticmethod
    def autenticar(db: Session, nombre_usuario: str, clave: str):
        """Verifica credenciales para inicio de sesión. Retorna None si no coinciden."""
        usuario = (
            db.query(Usuario)
            .filter(
                func.lower(Usuario.nombre_usuario) == nombre_usuario.strip().lower()
            )
            .first()
        )
        if usuario is None or usuario.clave != clave:
            return None
        return usuario
