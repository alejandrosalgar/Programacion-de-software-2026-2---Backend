from uuid import UUID
from entities.TipoCuenta import TipoCuenta


class TipoCuentaCRUD:
    """
    Módulo CRUD para la entidad TipoCuenta.
    Permite gestionar los tipos de cuenta que existen en el banco
    (ahorros, corriente, nómina, etc.).

    Funciones principales:
        - crear_tipo_cuenta(datos: dict, tipo: TipoCuenta) -> TipoCuenta
        - obtener_tipo_cuenta(datos: dict, id_tipo: UUID) -> TipoCuenta
        - obtener_tipos_cuenta(datos: dict) -> list
        - actualizar_tipo_cuenta(...) -> TipoCuenta
        - eliminar_tipo_cuenta(datos: dict, id_tipo: UUID) -> bool

    Notas:
        - Se valida que no se repitan tipos de cuenta con el mismo nombre.
        - "datos" es un diccionario en memoria
          (id_tipo_cuenta -> TipoCuenta).
    """

    def __init__(self, datos):
        self.datos = datos

    @staticmethod
    def crear_tipo_cuenta(datos: dict, tipo: TipoCuenta):
        if not tipo.nombre or not tipo.nombre.strip():
            raise ValueError("El nombre del tipo de cuenta no puede estar vacío")

        existente = next((t for t in datos.values() if t.nombre == tipo.nombre), None)

        if existente:
            raise ValueError("El tipo de cuenta ya existe")

        datos[tipo.id_tipo_cuenta] = tipo

        return tipo

    @staticmethod
    def obtener_tipo_cuenta(datos: dict, id_tipo: UUID):
        tipo = datos.get(id_tipo)

        if not tipo:
            raise ValueError("Tipo de cuenta no encontrado")

        return tipo

    @staticmethod
    def obtener_tipos_cuenta(datos: dict):
        return list(datos.values())

    @staticmethod
    def actualizar_tipo_cuenta(
        datos: dict,
        id_tipo: UUID,
        nombre: str,
        descripcion: str,
        tasa_interes: float,
        monto_minimo_apertura: float,
        requiere_mantenimiento: bool,
        id_usuario_edicion: UUID,
    ):
        tipo = datos.get(id_tipo)

        if not tipo:
            raise ValueError("Tipo de cuenta no encontrado")

        if not nombre or not nombre.strip():
            raise ValueError("El nombre del tipo de cuenta no puede estar vacío")

        # Verificar que no exista otro tipo de cuenta con el mismo nombre
        existente = next(
            (
                t
                for t in datos.values()
                if t.id_tipo_cuenta != id_tipo and t.nombre == nombre
            ),
            None,
        )

        if existente:
            raise ValueError("Ya existe otro tipo de cuenta con ese nombre")

        tipo.set_nombre(nombre)
        tipo.set_descripcion(descripcion)
        tipo.set_tasa_interes(tasa_interes)
        tipo.set_monto_minimo_apertura(monto_minimo_apertura)
        tipo.set_requiere_mantenimiento(requiere_mantenimiento)

        tipo.registrar_edicion(id_usuario_edicion)

        return tipo

    @staticmethod
    def eliminar_tipo_cuenta(datos: dict, id_tipo: UUID) -> bool:
        tipo = datos.get(id_tipo)

        if not tipo:
            raise ValueError("Tipo de cuenta no encontrado")

        del datos[id_tipo]

        return True
