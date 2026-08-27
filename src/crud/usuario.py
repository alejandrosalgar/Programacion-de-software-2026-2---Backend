from uuid import UUID

from entities.usuario import Usuario

usuarios: list[Usuario] = []


def _buscar_por_id(id_usuario: UUID) -> Usuario | None:
    for usuario in usuarios:
        if usuario.id_usuario == id_usuario:
            return usuario
    return None


def _buscar_por_nombre(nombre_usuario: str) -> Usuario | None:
    nombre = nombre_usuario.strip().lower()
    for usuario in usuarios:
        if usuario.nombre_usuario.lower() == nombre:
            return usuario
    return None


def crear(
    primer_nombre: str,
    segundo_nombre: str,
    primer_apellido: str,
    segundo_apellido: str,
    nombre_usuario: str,
    clave: str,
) -> Usuario | None:
    if _buscar_por_nombre(nombre_usuario):
        return None

    usuario = Usuario(
        primer_nombre=primer_nombre,
        segundo_nombre=segundo_nombre,
        primer_apellido=primer_apellido,
        segundo_apellido=segundo_apellido,
        nombre_usuario=nombre_usuario,
        clave=clave,
    )
    usuarios.append(usuario)
    return usuario


def eliminar(id_usuario: UUID) -> bool:
    usuario = _buscar_por_id(id_usuario)
    if usuario is None:
        return False
    usuarios.remove(usuario)
    return True


def actualizar(
    id_usuario: UUID,
    primer_nombre: str | None = None,
    segundo_nombre: str | None = None,
    primer_apellido: str | None = None,
    segundo_apellido: str | None = None,
    nombre_usuario: str | None = None,
    clave: str | None = None,
) -> Usuario | None:
    usuario = _buscar_por_id(id_usuario)
    if usuario is None:
        return None

    if nombre_usuario:
        existente = _buscar_por_nombre(nombre_usuario)
        if existente is not None and existente.id_usuario != id_usuario:
            return None

    if primer_nombre:
        usuario.primer_nombre = primer_nombre.strip()
    if segundo_nombre is not None:
        usuario.segundo_nombre = segundo_nombre.strip()
    if primer_apellido:
        usuario.primer_apellido = primer_apellido.strip()
    if segundo_apellido is not None:
        usuario.segundo_apellido = segundo_apellido.strip()
    if nombre_usuario:
        usuario.nombre_usuario = nombre_usuario.strip()
    if clave:
        usuario.clave = clave

    return usuario


def obtener(nombre_usuario: str, clave: str) -> Usuario | None:
    usuario = _buscar_por_nombre(nombre_usuario)
    if usuario is None or usuario.clave != clave:
        return None
    return usuario


def listar() -> list[Usuario]:
    return list(usuarios)
