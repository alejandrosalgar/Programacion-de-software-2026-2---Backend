# Programacion de software 2026-2 — API REST

Proyecto de programacion de software ITM.

Hoy el backend se usa por **consola**: `main.py` pide datos con `input` y muestra resultados con `print`. El siguiente paso es exponer el mismo CRUD como **API REST** con **FastAPI**, para que un frontend (u otra aplicacion) hable con el sistema por HTTP.

Esta guia explica, desde cero:

- que es una API y para que sirve
- por que REST
- que es FastAPI y como funciona
- como se organizara la carpeta `api` en este proyecto
- como quedara `main.py` (solo la app, CORS y Uvicorn)

**Este archivo es la guia.** Aun no se reescribe el codigo: primero se entiende, despues se implementa.

La consola actual sigue funcionando:

```bash
python src/main.py
```

Cuando exista la API, el arranque sera:

```bash
uvicorn src.main:app --reload
```

---

## 1. Donde estamos

```
src/
  main.py            # menus de consola (input / print)
  entities/          # modelos ORM (Usuario, Cuenta, Tarjeta, ...)
  crud/              # crear, eliminar, actualizar, obtener, listar
  database/          # conexion a Neon + seeder
  init_db.py         # crea las tablas
```

Flujo actual:

```
persona  -->  main.py (consola)  -->  crud  -->  entities / SQLAlchemy  -->  PostgreSQL (Neon)
```

- `main.py` es la **interfaz**. Solo pide y muestra.
- `entities` define los objetos y las tablas.
- `crud` es el contrato de negocio: cinco operaciones por entidad.
- La base ya existe (Neon). El seeder carga usuarios, cuentas y tarjetas de prueba.

El contrato del CRUD **no deberia cambiar**. Lo que cambia es **quien llama** al CRUD:

| Ahora | Despues |
| --- | --- |
| Una persona en la terminal | Un cliente HTTP (frontend, Postman, celular) |
| `input` / `print` | JSON de ida y vuelta |
| Un solo usuario a la vez | Varias peticiones al mismo tiempo |
| El programa se cierra y listo | Un servidor que se queda escuchando |

```
cliente HTTP  -->  FastAPI (main + api/)  -->  crud  -->  ORM  -->  Neon
```

`entities` y `database` se quedan. `crud` se queda. Lo que se reemplaza es la consola.

---

## 2. Que es una API

**API** significa *Application Programming Interface* (interfaz de programacion de aplicaciones).

Es un **contrato** entre dos programas: uno pide algo y el otro responde, con reglas claras.

En la vida diaria ya se usan APIs, aunque no se vean:

- una app del clima pide el pronostico a un servidor
- el frontend de un banco pide el saldo de una cuenta
- Postman prueba un `GET /usuarios` contra nuestro backend

Sin API, el unico camino es la consola. Nadie mas puede usar el CRUD.

Con API, el backend ofrece operaciones como:

- "crea este usuario"
- "listame las cuentas"
- "elimina esta tarjeta"

El cliente no entra a Python, no importa SQLAlchemy ni Neon. Solo habla el contrato: **URL + metodo HTTP + JSON**.

Analogia con este proyecto:

| Consola | API |
| --- | --- |
| Elegir `2. Crear usuario` | `POST /usuarios` |
| Escribir primer nombre, clave... | Enviar un JSON con esos campos |
| Ver el usuario impreso | Recibir el usuario en JSON |
| Elegir `1. Listar` | `GET /usuarios` |

La API no es una base de datos. Es la **puerta** para usar el backend.

---

## 3. Por que una API en este proyecto

1. **Separar interfaz y negocio.** El CRUD ya existe. La consola es una interfaz. La API es otra. El banco no se reescribe: se expone.
2. **El frontend no corre en la misma terminal.** React, Vue o un HTML van a estar en otro origen (otro puerto). Necesitan HTTP.
3. **Varios clientes, un backend.** Consola, web, movil o pruebas: todos piden lo mismo (`listar cuentas`).
4. **Datos reales.** Neon ya guarda usuarios, cuentas y tarjetas. La API es la forma de leerlos y escribirlos desde fuera.
5. **Es el estandar de un backend.** Un sistema de software se entrega como servicio HTTP, no como menu de `input`.

La consola sirvio para construir entidades y CRUD. La API es el mismo sistema, listo para hablar con el resto del mundo.

---

## 4. Que es REST (y por que REST)

**REST** significa *Representational State Transfer*.

Es un estilo para disenar APIs sobre **HTTP**. La idea central:

- cada cosa del negocio es un **recurso** (usuario, cuenta, tarjeta)
- el recurso tiene una **URL**
- las acciones se expresan con **verbos HTTP**, no con nombres raros de funcion

No se hace `GET /obtenerUsuario` ni `GET /crearCuenta`. Se hace:

```
GET    /usuarios
POST   /usuarios
GET    /usuarios/{id}
PUT    /usuarios/{id}
DELETE /usuarios/{id}
```

### Recursos de este proyecto

| Entidad | Recurso | Idea |
| --- | --- | --- |
| `Usuario` | `/usuarios` | Personas que inician sesion |
| `Cuenta` | `/cuentas` | Cuentas bancarias de un usuario |
| `Tarjeta` | `/tarjetas` | Tarjetas asociadas a una cuenta |

### CRUD = verbos HTTP

El CRUD que ya tenemos se mapea asi:

| CRUD | HTTP | Ejemplo | Que hace |
| --- | --- | --- | --- |
| `listar()` | `GET` | `GET /usuarios` | Traer la coleccion |
| `obtener(...)` | `GET` | `GET /usuarios/{id}` | Traer uno |
| `crear(...)` | `POST` | `POST /usuarios` | Crear |
| `actualizar(...)` | `PUT` | `PUT /usuarios/{id}` | Reemplazar / actualizar |
| `eliminar(...)` | `DELETE` | `DELETE /usuarios/{id}` | Borrar |

`GET` no deberia cambiar datos. `POST`, `PUT` y `DELETE` si.

### JSON

El cuerpo de las peticiones y respuestas va en **JSON** (texto estructurado). Ejemplo de crear usuario:

```json
{
  "primer_nombre": "Ana",
  "segundo_nombre": "Maria",
  "primer_apellido": "Restrepo",
  "segundo_apellido": "Lopez",
  "nombre_usuario": "ana.restrepo",
  "clave": "123456"
}
```

Respuesta (sin devolver la clave, en un diseno cuidadoso):

```json
{
  "id_usuario": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "primer_nombre": "Ana",
  "nombre_usuario": "ana.restrepo"
}
```

### Codigos de estado

HTTP responde con un numero. No basta con el JSON:

| Codigo | Significado | Cuando en este proyecto |
| --- | --- | --- |
| `200` | OK | Listar o actualizar bien |
| `201` | Created | `POST` que si creo |
| `204` | No Content | `DELETE` exitoso, sin cuerpo |
| `400` | Bad Request | Datos invalidos (numero de cuenta vacio) |
| `404` | Not Found | Esa cuenta o tarjeta no existe |
| `409` | Conflict | `nombre_usuario` o `numero_cuenta` repetido |
| `422` | Unprocessable Entity | FastAPI: el JSON no cumple el esquema |
| `500` | Error del servidor | Falla inesperada ( Neon caido, etc.) |

REST no es una libreria. Es la forma de pensar las URLs, los verbos y los recursos. FastAPI es la herramienta que lo implementa en Python.

---

## 5. Que es FastAPI

[FastAPI](https://fastapi.tiangolo.com/) es un framework web para construir APIs en Python.

Se elige para este curso porque:

1. **Usa type hints.** `nombre_usuario: str` ya lo escribimos en el CRUD. FastAPI los aprovecha.
2. **Documentacion sola.** Al arrancar aparecen `/docs` (Swagger) y `/redoc`. Se prueban endpoints sin Postman, al inicio.
3. **Pydantic valida el JSON.** Si falta `clave` o `saldo` no es un numero, responde `422` antes de tocar el CRUD.
4. **Rapido de leer.** Un endpoint se parece a una funcion de Python.
5. **Ecosistema actual.** Es el estandar de facto para APIs nuevas en Python.

No reemplaza SQLAlchemy. FastAPI recibe HTTP; el CRUD y el ORM siguen haciendo persistencia.

```
HTTP  -->  FastAPI (rutas)  -->  crud  -->  SQLAlchemy  -->  Neon
              |
         Pydantic (validar JSON)
```

### Uvicorn

FastAPI no abre el puerto solo. Necesita un servidor **ASGI**.

[Uvicorn](https://www.uvicorn.org/) es ese servidor: toma la app FastAPI, escucha en un puerto (por defecto `8000`) y entrega cada peticion HTTP a las rutas.

```
navegador / Postman / frontend
        |
     Uvicorn   (escucha localhost:8000)
        |
     FastAPI   (el objeto `app`)
        |
     nuestras rutas en api/
```

Por eso, cuando se implemente, `main.py` no se ejecutara con `python src/main.py` como menu, sino:

```bash
uvicorn src.main:app --reload
```

- `src.main` = modulo `src/main.py`
- `app` = la variable FastAPI dentro de ese archivo
- `--reload` = al guardar codigo, el servidor se reinicia (desarrollo)

### Pydantic (esquemas)

Las entidades (`Usuario`, `Cuenta`, `Tarjeta`) son modelos de **base de datos**. No conviene mandarlas crudas por la red: traen relacion con SQLAlchemy, clave en texto plano, campos internos.

Un **esquema** Pydantic es el JSON que la API acepta o devuelve:

```python
from pydantic import BaseModel


class UsuarioPost(BaseModel):
    primer_nombre: str
    segundo_nombre: str = ""
    primer_apellido: str
    segundo_apellido: str = ""
    nombre_usuario: str
    clave: str


class UsuarioGet(BaseModel):
    id_usuario: UUID
    primer_nombre: str
    segundo_nombre: str
    primer_apellido: str
    segundo_apellido: str
    nombre_usuario: str
```

- `UsuarioCreate`: lo que llega en el `POST`
- `UsuarioRead`: lo que se responde (sin `clave`)

La entidad ORM se queda en `entities`. El esquema vive en la capa API.

---

## 6. Como funciona una peticion (de punta a punta)

Ejemplo: el frontend pide `GET /cuentas`.

1. El navegador (o Postman) manda HTTP a `http://127.0.0.1:8000/cuentas`.
2. **Uvicorn** recibe el TCP y se lo pasa a FastAPI.
3. FastAPI busca una ruta que coincida: `GET` + `/cuentas`.
4. Antes, **CORS** decide si ese origen tiene permiso (si la peticion viene de un navegador en otro puerto).
5. Si hay cuerpo JSON (en `POST`/`PUT`), **Pydantic** lo valida.
6. La funcion de la ruta llama a `cuenta_crud.listar()`.
7. El CRUD habla con SQLAlchemy / Neon y devuelve objetos `Cuenta`.
8. FastAPI convierte el resultado a JSON y responde `200`.

Si no hay ruta: `404`.
Si el JSON esta mal: `422`.
Si el CRUD no encuentra la fila: la ruta responde `404`.

Nada de esto usa `input` ni `print` de menús. El "menu" son las URLs.

---

## 7. CORS — por que aparece en `main.py`

**CORS** significa *Cross-Origin Resource Sharing* (compartir recursos entre origenes).

Un **origen** es la combinacion de protocolo + host + puerto:

- `http://localhost:8000` → la API
- `http://localhost:5173` → un frontend Vite/React, por ejemplo

El navegador bloquea, por seguridad, que una pagina en `5173` lea respuestas de `8000`, **salvo** que el servidor lo autorice con cabeceras CORS.

Sin CORS:

```
Frontend (puerto 5173)  --X-->  API (puerto 8000)
Error: blocked by CORS policy
```

Con CORS configurado en FastAPI:

```
Frontend (puerto 5173)  ----->  API (puerto 8000)  -->  JSON
```

En desarrollo se suele permitir el origen del frontend, o `*` para pruebas locales (no en produccion abierta).

FastAPI lo resuelve con `CORSMiddleware`. Quedara en `main.py`, junto a la creacion de `app`, porque es una regla **global** del servidor, no de una entidad.

CORS no autentica usuarios. Solo dice: "este origen del navegador puede hablarme". Login, tokens y roles son otro tema.

---

## 8. Como va a funcionar en ESTE proyecto

### 8.1 Lo que se conserva

- `src/entities/` — modelos
- `src/crud/` — operaciones
- `src/database/` — Neon, `get_session`, seeder
- `src/init_db.py` — crear tablas

### 8.2 Lo que se agrega: carpeta `api`

Ahi viven las **rutas HTTP**. Una idea de estructura:

```
src/
  main.py                 # solo FastAPI + CORS + incluir routers
  api/
    __init__.py
    schemas.py            # (o schemas/ ) modelos Pydantic
    usuarios.py           # router GET/POST/PUT/DELETE /usuarios
    cuentas.py            # router /cuentas
    tarjetas.py           # router /tarjetas
  entities/
  crud/
  database/
```

Cada archivo de `api/` es un **router**: agrupa las rutas de una entidad y llama a su CRUD.

El router no abre la sesion SQL a mano si el CRUD ya lo hace. El router:

1. recibe el JSON (esquema)
2. llama `usuario_crud.crear(...)`
3. traduce `None` o "no encontrado" a `HTTPException` (`404`, `409`, ...)
4. devuelve el esquema de respuesta

Asi `api/` no se mezcla con SQL. `crud/` no se mezcla con HTTP. `main.py` no conoce `Usuario` ni `Cuenta`.

### 8.3 Lo que se borra de `main.py`

Hoy `main.py` tiene menus, `limpiar_pantalla`, `getpass`, `crear_usuario`, `menu_sedes`, `menu_cuentas`, etc.

Eso **se elimina**. `main.py` deja de ser un programa interactivo.

Quedara, en esencia:

1. crear `app = FastAPI(...)`
2. agregar **CORS**
3. incluir los routers de `api/`
4. (opcional) un `GET /` de salud: `{"ok": true}`

Uvicorn carga ese `app`. No hay `if __name__ == "__main__": menu_principal()`.

Comparacion:

```
ANTES
  python src/main.py
  --> while True: mostrar menu, input, print

DESPUES
  uvicorn src.main:app --reload
  --> servidor HTTP en el puerto 8000
  --> /docs para probar
  --> /usuarios, /cuentas, /tarjetas
```

### 8.4 Diagrama de carpetas (despues)

```
cliente HTTP
    |
 uvicorn  -->  main.py (app + CORS)
                  |
                  +-- api/usuarios.py  -->  crud/usuario.py  -->  entities/usuario.py
                  +-- api/cuentas.py   -->  crud/cuenta.py   -->  entities/cuenta.py
                  +-- api/tarjetas.py  -->  crud/Tarjeta.py  -->  entities/Tarjeta.py
                                              |
                                         database/connection.py
                                              |
                                            Neon
```

---

## 9. Paso a paso: de la consola a la API

Igual que con el ORM: el codigo de abajo es **el destino**. Se implementa despues de entender esta guia.

### Paso 0 — CRUD estable y datos en Neon

Antes de HTTP:

- cada entidad con `crear`, `eliminar`, `actualizar`, `obtener`, `listar`
- tablas creadas (`init_db.py`)
- seeder ejecutado (`python src/database/seed.py`) para tener `ana.restrepo` y sus cuentas/tarjetas

La API no inventa datos: expone lo que el CRUD ya sabe hacer.

El CRUD, en el diseno final, debe usar `Session` contra Neon (como indica el `README.md` del ORM). Si el CRUD sigue en listas de RAM, la API arranca pero no vera el seeder.

### Paso 1 — Dependencias

En la raiz del repo:

```bash
pip install fastapi uvicorn
```

En `requirements.txt`:

```text
fastapi
uvicorn
```

`pydantic` llega como dependencia de FastAPI. SQLAlchemy, `psycopg2` y `python-dotenv` ya estan.

### Paso 2 — Esquemas Pydantic

Definir, por entidad, al menos:

- `*Create` — cuerpo del `POST`
- `*Update` — cuerpo del `PUT` (campos opcionales)
- `*Read` — respuesta (ids incluidos; sin secretos como `clave` o `cvv` si se decide ocultarlos)

Viven en `src/api/` (por ejemplo `schemas.py` o `api/schemas/usuario.py`). **No** se mezclan con `entities`.

### Paso 3 — Routers en `src/api/`

Cada modulo crea un `APIRouter` y declara las rutas.

Ejemplo de idea para usuarios (ilustrativo):

```python
from fastapi import APIRouter, HTTPException
from crud import usuario as usuario_crud

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/")
def listar_usuarios():
    return usuario_crud.listar()


@router.post("/", status_code=201)
def crear_usuario(datos: UsuarioCreate):
    usuario = usuario_crud.crear(...)
    if usuario is None:
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
    return usuario
```

Mismo patron para cuentas y tarjetas:

- `prefix="/cuentas"`, `prefix="/tarjetas"`
- `tags` para que `/docs` agrupe por entidad
- `HTTPException` cuando el CRUD devuelve `None` o lanza `ValueError`

`api/` importa `crud`. `api/` **no** importa menus. `crud` **no** importa FastAPI.

### Paso 4 — Reescribir `main.py`

Se borra el menu. Queda la aplicacion:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.usuarios import router as usuarios_router
from api.cuentas import router as cuentas_router
from api.tarjetas import router as tarjetas_router

app = FastAPI(
    title="API Banco — Programacion de software 2026-2",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo; luego el origen real del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)
app.include_router(cuentas_router)
app.include_router(tarjetas_router)


@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}
```

Eso es `main.py`: **app + CORS + routers**. Sin `input`. Sin `cls`. Sin `menu_principal`.

Uvicorn importa `app` desde este archivo.

### Paso 5 — CORS (detalle)

`CORSMiddleware` debe registrarse **antes** de usar la API desde el navegador.

| Parametro | Para que |
| --- | --- |
| `allow_origins` | Que paginas pueden llamar (ej. `http://localhost:5173` o `*` en local) |
| `allow_methods` | Verbos permitidos (`GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`) |
| `allow_headers` | Cabeceras que el frontend puede enviar (`Content-Type`, etc.) |
| `allow_credentials` | Cookies / autorizacion entre origenes |

El navegador manda primero un `OPTIONS` (preflight) en varios `POST`/`PUT`. FastAPI + este middleware responden ese `OPTIONS`. No hay que crear una ruta `OPTIONS` a mano.

### Paso 6 — Arrancar Uvicorn

Desde la raiz del repo (ajustando el modulo segun como quede el `PYTHONPATH`):

```bash
uvicorn src.main:app --reload
```

O, si se trabaja con `src` en el path:

```bash
cd src
uvicorn main:app --reload
```

Salida esperada: escuchando en `http://127.0.0.1:8000`.

### Paso 7 — Probar el circuito

1. Abrir `http://127.0.0.1:8000/docs`.
2. `GET /` debe devolver el mensaje de salud.
3. `GET /usuarios`, `GET /cuentas`, `GET /tarjetas` (con el seeder deberia haber filas).
4. `POST /usuarios` con un JSON nuevo; repetir el mismo `nombre_usuario` debe dar conflicto.
5. `PUT` y `DELETE` de un id existente.
6. Desde un frontend en otro puerto, confirmar que CORS no bloquee.

Si `/docs` abre y los `GET` responden JSON, la consola ya no es necesaria para usar el backend.

---

## 10. Endpoints previstos (mapa)

Recursos con los que ya hay modelo ORM y seeder: **usuarios, cuentas, tarjetas**.

### Usuarios — `/usuarios`

| Metodo | Ruta | CRUD |
| --- | --- | --- |
| `GET` | `/usuarios` | `listar` |
| `GET` | `/usuarios/{id_usuario}` | `obtener` por id |
| `POST` | `/usuarios` | `crear` |
| `PUT` | `/usuarios/{id_usuario}` | `actualizar` |
| `DELETE` | `/usuarios/{id_usuario}` | `eliminar` |
| `POST` | `/usuarios/login` | `obtener(nombre, clave)` |

Login puede ser un `POST` extra: no es CRUD puro, pero el menu de consola ya lo tenia. El cuerpo seria `nombre_usuario` + `clave`.

### Cuentas — `/cuentas`

| Metodo | Ruta | CRUD |
| --- | --- | --- |
| `GET` | `/cuentas` | `listar` |
| `GET` | `/cuentas/{id_cuenta}` | `obtener` |
| `POST` | `/cuentas` | `crear` |
| `PUT` | `/cuentas/{id_cuenta}` | `actualizar` |
| `DELETE` | `/cuentas/{id_cuenta}` | `eliminar` |

Una cuenta pertenece a un usuario (`id_usuario`). El JSON de alta incluye titular, numero y saldo.

### Tarjetas — `/tarjetas`

| Metodo | Ruta | CRUD |
| --- | --- | --- |
| `GET` | `/tarjetas` | `listar` / `obtener_tarjetas` |
| `GET` | `/tarjetas/{id_tarjeta}` | `obtener` |
| `POST` | `/tarjetas` | `crear` |
| `PUT` | `/tarjetas/{id_tarjeta}` | `actualizar` |
| `DELETE` | `/tarjetas/{id_tarjeta}` | `eliminar` |

Una tarjeta pertenece a una cuenta (`id_cuenta`). Sin cuenta, no hay tarjeta (FK).

Otras entidades (`Sede`, `Empleado`, ...) pueden sumarse despues con el mismo patron: un archivo en `api/` + el CRUD que ya existe.

---

## 11. Que hace cada pieza (resumen)

| Pieza | Para que sirve en este proyecto |
| --- | --- |
| API | Contrato HTTP para usar el backend sin consola |
| REST | URLs de recursos + verbos CRUD |
| FastAPI | Framework que declara rutas y valida JSON |
| Pydantic | Forma del JSON de entrada/salida |
| Uvicorn | Servidor que mantiene `app` escuchando |
| CORS | Permite que el frontend en otro puerto llame a la API |
| `src/api/` | Rutas por entidad; llama a `crud` |
| `src/main.py` | Solo `app`, middleware CORS e `include_router` |
| `crud` / `entities` / `database` | Se reutilizan; no se tiran |

---

## 12. Orden recomendado de implementacion

1. Entender esta guia (sin codigo todavia).
2. Instalar FastAPI y Uvicorn.
3. Dejar `main.py` con `app` vacia + CORS + `GET /` y arrancar Uvicorn. Ver `/docs`.
4. Esquemas Pydantic de `Usuario`.
5. Router `api/usuarios.py` y `include_router` en `main`.
6. Repetir con `cuentas` y `tarjetas`.
7. Probar CRUD completo en `/docs`.
8. Recien ahi conectar un frontend; CORS ya estara.

No hace falta reescribir entidades. El cambio vive en `api/` (nuevo) y en `main.py` (se vacia).

---

## Buenas practicas

- `api/` llama a `crud`. No copie SQL ni listas en las rutas.
- `main.py` no declara `POST /usuarios` ahi mismo cuando ya hay varios recursos: eso es trabajo de routers.
- No devolver `clave` ni `cvv` en los JSON de lectura, si se puede evitar.
- CORS con `allow_origins=["*"]` solo en desarrollo.
- `--reload` es de desarrollo; en un servidor real se arranca sin reload.
- Nunca pegar `DATABASE_URL` ni secretos en este README ni en el chat.
- Cerrar la `Session` del CRUD como ya indica el README del ORM.

---

## Referencias

- [FastAPI — Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI — CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [Uvicorn](https://www.uvicorn.org/)
- [MDN — REST](https://developer.mozilla.org/es/docs/Glossary/REST)
- [MDN — CORS](https://developer.mozilla.org/es/docs/Web/HTTP/Guides/CORS)
- [HTTP status codes](https://developer.mozilla.org/es/docs/Web/HTTP/Reference/Status)

La guia del ORM y Neon sigue en [`README.md`](README.md). Esta API se apoya en esa persistencia: primero tablas y CRUD, despues HTTP.
