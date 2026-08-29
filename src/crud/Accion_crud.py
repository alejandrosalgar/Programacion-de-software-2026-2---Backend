from uuid import UUID
from entities.Accion import Accion


class AccionCRUD:
    """
    Módulo CRUD para la entidad Accion.
    Permite gestionar las acciones realizadas por los usuarios.

    Funciones principales:
        - crear_accion(datos: dict, accion: Accion) -> Accion
        - obtener_accion(datos: dict, id_accion: UUID) -> Accion
        - obtener_acciones(datos: dict) -> list
        - actualizar_accion(...) -> Accion
        - eliminar_accion(datos: dict, id_accion: UUID) -> bool

    Notas:
        - "datos" es un diccionario en memoria
          (id_accion -> Accion).
    """

    def __init__(self, datos):
        self.datos = datos

    @staticmethod
    def crear_accion(datos: dict, accion: Accion):
        if not accion.tipo_accion or not accion.tipo_accion.strip():
            raise ValueError("El tipo de acción no puede estar vacío")

        if not accion.descripcion or not accion.descripcion.strip():
            raise ValueError("La descripción de la acción no puede estar vacía")

        datos[accion.id_accion] = accion

        return accion

    @staticmethod
    def obtener_accion(datos: dict, id_accion: UUID):
        accion = datos.get(id_accion)

        if not accion:
            raise ValueError("Acción no encontrada")

        return accion

    @staticmethod
    def obtener_acciones(datos: dict):
        return list(datos.values())

    @staticmethod
    def actualizar_accion(
        datos: dict,
        id_accion: UUID,
        tipo_accion: str,
        descripcion: str,
        ip_origen: str,
        resultado: str,
    ):
        accion = datos.get(id_accion)

        if not accion:
            raise ValueError("Acción no encontrada")

        if not tipo_accion or not tipo_accion.strip():
            raise ValueError("El tipo de acción no puede estar vacío")

        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción de la acción no puede estar vacía")

        accion.tipo_accion = tipo_accion
        accion.descripcion = descripcion
        accion.ip_origen = ip_origen
        accion.resultado = resultado

        return accion

    @staticmethod
    def eliminar_accion(datos: dict, id_accion: UUID) -> bool:
        accion = datos.get(id_accion)

        if not accion:
            raise ValueError("Acción no encontrada")

        del datos[id_accion]

        return True
