# Programacion de software 2026-2 — Backend

Proyecto de programacion de software ITM.

Hoy el sistema guarda `Usuario` y `Sede` en listas de Python. Los datos se pierden al cerrar el programa. Esta guia explica, paso a paso, como pasar esa persistencia a un **ORM** con **SQLAlchemy** y una base **PostgreSQL** en **Neon**.

Ejecutar la consola actual:

```bash
python src/main.py
```

## 1. Donde estamos

```
src/
  main.py          # menus, input y print
  entities/        # clases Usuario y Sede
  crud/            # crear, eliminar, actualizar, obtener, listar
```

- `main.py` solo pide datos y muestra resultados.
- `entities` define los objetos de negocio.
- `crud` opera sobre listas en memoria (`usuarios = []`, `sedes = []`).

El contrato del CRUD no deberia cambiar: cinco operaciones por entidad. Lo que cambia es **donde** se guardan los datos.

| Ahora | Despues |
| --- | --- |
| Lista en RAM | Tablas en PostgreSQL (Neon) |
| Se pierde al salir | Persiste entre ejecuciones |
| Buscar con un `for` | Consultas via SQLAlchemy |

## 2. Que es un ORM

**ORM** significa *Object-Relational Mapping* (mapeo objeto-relacional).

Es una capa que traduce:

- una **clase** de Python (`Usuario`, `Sede`) en una **tabla**
- un **objeto** en una **fila**
- un **atributo** (`primer_nombre`) en una **columna**

Sin ORM, el CRUD tendria que armar SQL a mano:

```sql
INSERT INTO usuario (primer_nombre, nombre_usuario, clave)
VALUES ('Ana', 'ana', '123');
```

Con ORM se sigue trabajando con objetos:

```python
usuario = Usuario(primer_nombre="Ana", nombre_usuario="ana", clave="123")
session.add(usuario)
session.commit()
```

SQLAlchemy genera el SQL, abre la conexion y lee/escribe las filas.

```
main.py  -->  crud  -->  ORM (SQLAlchemy)  -->  PostgreSQL en Neon
              |              |
           entidades      tablas usuario / sede
```

## 3. Por que usar un ORM

1. **Menos SQL repetido.** El CRUD sigue siendo `crear`, `listar`, `obtener`, `actualizar`, `eliminar`.
2. **Menos errores.** Tipos, UUID, nulos y llaves foraneas se declaran en el modelo.
3. **El mismo codigo, otra base.** Cambiar de listas a Postgres (o de un motor a otro) no obliga a reescribir `main.py`.
4. **Relaciones explicitas.** `Sede.id_usuario_creacion` e `id_usuario_edicion` quedan como FK hacia `Usuario`.
5. **Datos reales.** Neon guarda la informacion en la nube; no se borra al cerrar la consola.

Un ORM no reemplaza entender SQL. Ayuda a no mezclar SQL dentro de la interfaz.

## 4. Por que SQLAlchemy

[SQLAlchemy](https://www.sqlalchemy.org/) es el ORM mas usado en Python.

Usaremos el estilo **2.0** (`DeclarativeBase`, `Mapped`, `mapped_column`):

- el modelo se parece a las clases actuales de `entities`
- el CRUD cambia listas por una `Session`
- se conecta a Postgres con una URL

Complementos:

| Paquete | Para que |
| --- | --- |
| `sqlalchemy` | ORM y motor de conexion |
| `psycopg2-binary` | Driver de PostgreSQL |
| `python-dotenv` | Leer la URL desde `.env` |

## 5. Que es Neon

[Neon](https://neon.tech) es PostgreSQL serverless en la nube: se crea un proyecto, se copia la cadena de conexion y se usa como base remota. Sirve para desarrollo y para este curso (plan gratuito).

La conexion exige SSL (`sslmode=require`). SQLAlchemy se encarga si la URL esta bien armada.

## Paso a paso: de listas a ORM + Neon

### Paso 0 — Dejar el CRUD estable

Antes de tocar la base, el CRUD de cada entidad debe quedar en cinco metodos:

- `crear`
- `eliminar`
- `actualizar`
- `obtener` (en usuario: nombre y clave; en sede: id)
- `listar`

`main.py` no deberia importar `entities`. Asi, al cambiar el almacenamiento, la consola casi no se mueve.

### Paso 1 — Crear el proyecto en Neon

1. Entrar a [https://console.neon.tech](https://console.neon.tech) y crear cuenta.
2. **Create project** (region cercana, por ejemplo `Ohio` o `Sao Paulo` si aparece).
3. Abrir el proyecto → **Dashboard** → **Connection string**.
4. Copiar la URL. Se ve parecida a:

```text
postgresql://usuario:clave@ep-xxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

Esa URL no se sube a Git. Ya esta ignorada en `.gitignore` (`.env`).

### Paso 2 — Dependencias

En la raiz del repo:

```bash
pip install sqlalchemy psycopg2-binary python-dotenv
```

Opcional, dejarlas fijas en `requirements.txt`:

```text
sqlalchemy
psycopg2-binary
python-dotenv
```

### Paso 3 — Variable de entorno

Crear `.env` en la raiz (no se versiona):

```env
DATABASE_URL=postgresql+psycopg2://usuario:clave@ep-xxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

El prefijo `postgresql+psycopg2://` le indica a SQLAlchemy que use el driver `psycopg2`. Si Neon entrega `postgresql://`, solo hay que insertar `+psycopg2` despues de `postgresql`.

### Paso 4 — Conexion unica (`database`)

Nueva carpeta, por ejemplo `src/database/connection.py`:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Falta DATABASE_URL en el archivo .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_session():
    return SessionLocal()
```

- `engine`: puente con Neon.
- `Session`: transaccion (un conjunto de lecturas/escrituras).
- `Base`: clase padre de los modelos ORM.

### Paso 5 — Convertir entities en modelos

Las clases de `entities` pasan a heredar de `Base` y declaran columnas. Ejemplo de `Usuario`:

```python
import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database.connection import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    primer_nombre: Mapped[str] = mapped_column(String(80))
    segundo_nombre: Mapped[str] = mapped_column(String(80), default="")
    primer_apellido: Mapped[str] = mapped_column(String(80))
    segundo_apellido: Mapped[str] = mapped_column(String(80), default="")
    nombre_usuario: Mapped[str] = mapped_column(String(80), unique=True)
    clave: Mapped[str] = mapped_column(String(255))
```

`Sede` sigue la misma idea, con FK:

```python
id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuario.id_usuario"))
id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
    ForeignKey("usuario.id_usuario"), nullable=True
)
fecha_creacion: Mapped[date] = mapped_column(default=date.today)
fecha_edicion: Mapped[date | None] = mapped_column(nullable=True)
```

Equivalencia con lo que ya existe:

| Atributo actual | Columna ORM |
| --- | --- |
| `id_usuario` / `id_sede` (UUID) | `primary_key=True` |
| `nombre_usuario` | `unique=True` |
| `id_usuario_creacion` | `ForeignKey("usuario.id_usuario")` |
| `id_usuario_edicion` (puede ser null) | `nullable=True` |
| `fecha_creacion` (hoy) | `default=date.today` |
| `fecha_edicion` (null) | `nullable=True` |

Los metodos `nombre_completo()` y `__str__()` pueden quedarse en la clase.

### Paso 6 — Crear las tablas en Neon

Una sola vez, al arrancar (o en un script `init_db.py`):

```python
from database.connection import Base, engine
from entities.usuario import Usuario
from entities.sede import Sede

Base.metadata.create_all(bind=engine)
```

SQLAlchemy crea `usuario` y `sede` si no existen. En Neon se pueden ver en **Tables**.

Mas adelante se pueden usar **migraciones** (Alembic). `create_all` alcanza para el primer paso.

### Paso 7 — Reescribir el CRUD (misma firma)

Se quitan las listas. Cada metodo abre una sesion, opera y hace `commit`.

Ejemplo de `crear` y `listar` en usuario:

```python
from database.connection import get_session
from entities.usuario import Usuario


def crear(...) -> Usuario | None:
    session = get_session()
    try:
        if session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first():
            return None
        usuario = Usuario(...)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
    finally:
        session.close()


def listar() -> list[Usuario]:
    session = get_session()
    try:
        return session.query(Usuario).all()
    finally:
        session.close()
```

`obtener` de login sigue recibiendo nombre y clave:

```python
def obtener(nombre_usuario: str, clave: str) -> Usuario | None:
    session = get_session()
    try:
        return (
            session.query(Usuario)
            .filter_by(nombre_usuario=nombre_usuario, clave=clave)
            .first()
        )
    finally:
        session.close()
```

En sede, `obtener(id_sede)` usa el UUID. `actualizar` y `eliminar` buscan por id, cambian campos o borran, y hacen `commit`.

`main.py` no cambia su flujo: sigue llamando `usuario_crud.crear`, `sede_crud.listar`, etc.

### Paso 8 — Probar el circuito

1. Confirmar que `.env` tiene `DATABASE_URL` con `postgresql+psycopg2://` y `sslmode=require`.
2. Crear tablas (`create_all`).
3. `python src/main.py`
4. Crear un usuario, iniciar sesion, crear una sede.
5. Cerrar el programa, volver a abrirlo: usuario y sede deben seguir ahi.
6. En Neon → **Tables**, revisar las filas.

## Orden recomendado de implementacion

1. Neon + `.env` (sin codigo todavia).
2. `database/connection.py` y un `print` de `engine.connect()` para validar la red.
3. Modelos `Usuario` y `Sede` + `create_all`.
4. CRUD de `usuario` contra la base.
5. CRUD de `sede` (FK incluidas).
6. Probar la consola de punta a punta.

No hace falta reescribir los menus. El cambio vive en `entities` (modelos) y `crud` (sesion en lugar de listas).

## Buenas practicas

- Nunca subir `.env` ni pegar la URL de Neon en el chat o en el README.
- Cerrar siempre la `Session` (`try` / `finally` o `with SessionLocal() as session:`).
- La clave del usuario, en un siguiente paso, deberia ir hasheada (no en texto plano).
- Si `create_all` no alcanza (cambiar columnas ya creadas), usar Alembic.

## Referencias

- [SQLAlchemy 2.0 — ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Neon — Connect from any application](https://neon.tech/docs/connect/connect-from-any-app)
- [Neon + SQLAlchemy](https://neon.tech/docs/guides/sqlalchemy)
