import uuid


class Usuario:
    def __init__(
        self,
        primer_nombre: str,
        segundo_nombre: str,
        primer_apellido: str,
        segundo_apellido: str,
        nombre_usuario: str,
        clave: str,
        id_usuario: uuid.UUID | None = None,
    ):
        self.id_usuario = id_usuario if id_usuario is not None else uuid.uuid4()
        self.primer_nombre = primer_nombre.strip()
        self.segundo_nombre = segundo_nombre.strip()
        self.primer_apellido = primer_apellido.strip()
        self.segundo_apellido = segundo_apellido.strip()
        self.nombre_usuario = nombre_usuario.strip()
        self.clave = clave

    def nombre_completo(self) -> str:
        partes = [
            self.primer_nombre,
            self.segundo_nombre,
            self.primer_apellido,
            self.segundo_apellido,
        ]
        return " ".join(parte for parte in partes if parte)

    def __str__(self) -> str:
        return (
            f"ID: {self.id_usuario}\n"
            f"Nombre: {self.nombre_completo()}\n"
            f"Usuario: {self.nombre_usuario}"
        )
