from uuid import UUID
from entities.Tarjeta import Tarjeta


class TarjetaCRUD:
    """
    Módulo CRUD para la entidad Tarjeta.
    Permite gestionar las tarjetas asociadas a las cuentas.

    Funciones principales:
        - crear_tarjeta(datos: dict, tarjeta: Tarjeta) -> Tarjeta
        - obtener_tarjeta(datos: dict, id_tarjeta: UUID) -> Tarjeta
        - obtener_tarjetas(datos: dict) -> list
        - actualizar_tarjeta(...) -> Tarjeta
        - eliminar_tarjeta(datos: dict, id_tarjeta: UUID) -> bool

    Notas:
        - Se valida que no se repita el número de tarjeta.
        - "datos" es un diccionario en memoria
          (id_tarjeta -> Tarjeta).
    """

    def __init__(self, datos):
        self.datos = datos

    @staticmethod
    def crear_tarjeta(datos: dict, tarjeta: Tarjeta):
        if not tarjeta.numero_tarjeta or not tarjeta.numero_tarjeta.strip():
            raise ValueError("El número de tarjeta no puede estar vacío")

        existente = next(
            (t for t in datos.values() if t.numero_tarjeta == tarjeta.numero_tarjeta),
            None,
        )

        if existente:
            raise ValueError("La tarjeta ya existe")

        datos[tarjeta.id_tarjeta] = tarjeta

        return tarjeta

    @staticmethod
    def obtener_tarjeta(datos: dict, id_tarjeta: UUID):
        tarjeta = datos.get(id_tarjeta)

        if not tarjeta:
            raise ValueError("Tarjeta no encontrada")

        return tarjeta

    @staticmethod
    def obtener_tarjetas(datos: dict):
        return list(datos.values())

    @staticmethod
    def actualizar_tarjeta(
        datos: dict,
        id_tarjeta: UUID,
        id_cuenta: UUID,
        numero_tarjeta: str,
        tipo_tarjeta: str,
        fecha_emision,
        fecha_vencimiento,
        cvv: str,
        limite_credito: float,
        id_usuario_edicion: UUID,
    ):
        tarjeta = datos.get(id_tarjeta)

        if not tarjeta:
            raise ValueError("Tarjeta no encontrada")

        if not numero_tarjeta or not numero_tarjeta.strip():
            raise ValueError("El número de tarjeta no puede estar vacío")

        # Verificar que no exista otra tarjeta con el mismo número
        existente = next(
            (
                t
                for t in datos.values()
                if t.id_tarjeta != id_tarjeta and t.numero_tarjeta == numero_tarjeta
            ),
            None,
        )

        if existente:
            raise ValueError("Ya existe otra tarjeta con ese número")

        tarjeta.set_id_cuenta(id_cuenta)
        tarjeta.set_numero_tarjeta(numero_tarjeta)
        tarjeta.set_tipo_tarjeta(tipo_tarjeta)
        tarjeta.set_fecha_emision(fecha_emision)
        tarjeta.set_fecha_vencimiento(fecha_vencimiento)
        tarjeta.set_cvv(cvv)
        tarjeta.set_limite_credito(limite_credito)

        tarjeta.registrar_edicion(id_usuario_edicion)

        return tarjeta

    @staticmethod
    def eliminar_tarjeta(datos: dict, id_tarjeta: UUID) -> bool:
        tarjeta = datos.get(id_tarjeta)

        if not tarjeta:
            raise ValueError("Tarjeta no encontrada")

        del datos[id_tarjeta]

        return True
