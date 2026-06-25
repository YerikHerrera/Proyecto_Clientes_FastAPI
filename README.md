# Proyecto Clientes - FastAPI

Aplicación backend desarrollada con **FastAPI** y **SQLModel** para la gestión de **Clientes**, **Facturas** y **Transacciones**, construida como ejercicio práctico del programa Tecnólogo en Análisis y Desarrollo de Software (SENA). El proyecto evoluciona desde una versión inicial sin estructura de carpetas (todo el código en un solo archivo) hasta una arquitectura organizada por módulos con persistencia real en base de datos.

## Tabla de contenido

- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Estructura actual del proyecto](#estructura-actual-del-proyecto)
- [Relación de la base de datos](#relación-de-la-base-de-datos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Evolución del proyecto por commit](#evolución-del-proyecto-por-commit)
- [Cómo navegar entre los commits](#cómo-navegar-entre-los-commits)
- [Pendientes antes de la sustentación](#pendientes-antes-de-la-sustentación)
- [Autor](#autor)

## Tecnologías utilizadas

| Tecnología                    | Uso                                                          |
|-------------------------------|--------------------------------------------------------------|
| Python 3.14                   | Lenguaje base                                                |
| FastAPI (`fastapi[standard]`) | Framework para construir la API REST                         |
| SQLModel                      | ORM (combina SQLAlchemy + Pydantic) para modelos y consultas |
| SQLite                        | Motor de base de datos (`bd_clientes.sqlite3`)               |
| Uvicorn / FastAPI CLI         | Servidor ASGI para correr la aplicación en desarrollo        |

## Estructura actual del proyecto

```
Proyecto_Clientes_FastAPI/
├── app/
│   ├── main.py                 # Punto de entrada, registro de routers y ciclo de vida de la app
│   ├── conexion_bd.py          # Motor de BD, creación de tablas y sesión (inyección de dependencias)
│   ├── listas.py               # Listas en memoria (usadas en versiones tempranas, hoy en desuso)
│   ├── modelos/
│   │   ├── clientes.py         # Modelo Cliente + esquemas Crear/Editar/Leer
│   │   ├── facturas.py         # Modelo Factura + esquemas y campo calculado vr_total
│   │   └── transacciones.py    # Modelo Transaccion + esquemas Crear/Editar/Leer
│   └── enrutadores/
│       ├── clientes.py         # Endpoints del módulo Clientes
│       ├── facturas.py         # Endpoints del módulo Facturas
│       └── transacciones.py    # Endpoints del módulo Transacciones
├── bd_clientes.sqlite3         # Base de datos SQLite (se genera/actualiza automáticamente)
├── requirements.txt            # Dependencias del proyecto
└── .gitignore
```

Esta estructura por carpetas (`modelos/` y `enrutadores/` separados dentro de un paquete `app/`) **no existió desde el inicio**: fue el resultado de una reorganización a mitad del desarrollo. Ver la sección [Evolución del proyecto por commit](#evolución-del-proyecto-por-commit) para el detalle.

## Relación de la base de datos

El modelo de datos tiene una relación jerárquica 1 → N entre los tres módulos:

```
Cliente (1) ───────< Factura (N) ───────< Transaccion (N)
   id                  id                    id
   nombre               fecha                cantidad
   email                cliente_id (FK)       vr_unitario
   descripcion          vr_total (calculado)  descripcion
                                               factura_id (FK)
```

- **Cliente → Factura**: un cliente puede tener muchas facturas (`Factura.cliente_id` referencia a `Cliente.id`).
- **Factura → Transacción**: una factura puede tener muchas transacciones/ítems (`Transaccion.factura_id` referencia a `Factura.id`).
- **`vr_total`** de la factura **no se guarda como columna en la BD**: es un `computed_field` que recorre las transacciones asociadas y suma `cantidad * vr_unitario`.
- Las relaciones se modelan con `Relationship` de SQLModel y `back_populates`, generando una **relación virtual bidireccional** (se puede navegar de cliente → facturas → transacciones, y también desde una transacción de vuelta a su factura).

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/YerikHerrera/Proyecto_Clientes_FastAPI.git
cd Proyecto_Clientes_FastAPI

# 2. Crear y activar entorno virtual
python -m venv .ent_vir
# Windows
.ent_vir\Scripts\activate
# Linux / Mac
source .ent_vir/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
fastapi dev app/main.py
# alternativa equivalente:
# uvicorn app.main:app --reload
```

La base de datos SQLite (`bd_clientes.sqlite3`) y sus tablas se crean automáticamente al iniciar la aplicación (evento `lifespan` en `conexion_bd.py`).

Una vez corriendo, la documentación interactiva está disponible en:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

## Evolución del proyecto por commit

El proyecto se desarrolló en **19 commits**, agrupados en tres etapas que reflejan los criterios de evaluación de la sustentación.

### Etapa 1 — Inicio del proyecto sin estructura

Todo el código vive en la raíz del repositorio (`main.py` suelto, sin paquete `app/`).

| Commit    | Fecha      | Descripción                                                             |
|-----------|------------|-------------------------------------------------------------------------|
| `079aeb0` | 2026-06-15 | Primer commit, proyecto clientes inicial                                |
| `edbdb7c` | 2026-06-15 | Modelo `Cliente` y dos primeros endpoints: listar todos y crear cliente |

### Etapa 2 — Funcionamiento primario sin estructura

Sigue todo en la raíz, pero ya hay un CRUD básico funcionando **en memoria** (listas Python) para los tres módulos, sin persistencia en base de datos.

| Commit    | Fecha      | Descripción                                                            |
|-----------|------------|------------------------------------------------------------------------|
| `4297cc4` | 2026-06-15 | Separación de modelos y generación de ID al crear                      |
| `c20716c` | 2026-06-15 | Endpoint de editar cliente + creación de `transacciones.py`            |
| `abd126a` | 2026-06-15 | Creación de todos los endpoints (sin lógica, como esqueleto)           |
| `9d5f6d6` | 2026-06-15 | Endpoint de listar una factura + manejo de excepciones                 |
| `5c44e9c` | 2026-06-15 | Endpoint de crear factura + modelo `Factura`                           |
| `4592949` | 2026-06-15 | Cálculo del valor total de la factura + endpoint crear transacción     |
| `1a9fefb` | 2026-06-15 | `fix:` corrección de errores en modelos, imports y lógica de endpoints |

### Etapa 3 — Funcionamiento con estructura

Se reorganiza el proyecto en un paquete `app/` con `modelos/` y `enrutadores/` separados, y se introduce **persistencia real en base de datos** con SQLModel + SQLite.

| Commit    | Fecha      | Descripción                                                                       |
|-----------|------------|-----------------------------------------------------------------------------------|
| `9a5952a` | 2026-06-15 | Organización del proyecto en carpetas (creación del paquete `app/`)               |
| `f898895` | 2026-06-15 | Extracción de los endpoints de `main.py` a sus respectivos enrutadores            |
| `88d691e` | 2026-06-15 | Instalación de FastAPI y SQLModel; conexión a BD; crear/listar clientes en SQLite |
| `6b16105` | 2026-06-21 | CRUD completo de Clientes contra base de datos                                    |
| `0386eca` | 2026-06-21 | Creación de tablas `Factura` y `Transaccion` y sus relaciones                     |
| `2d0aac5` | 2026-06-22 | Enrutador de facturas: listar y crear con persistencia en BD                      |
| `1c8f54f` | 2026-06-22 | Modelo y enrutador de transacciones: crear y listar                               |
| `35d4e14` | 2026-06-22 | `style:` configuración de paths en `settings.json` (limpieza de Pylance)          |
| `82bbc50` | 2026-06-24 | Modelos de cliente/factura + relación virtual bidireccional cliente↔factura       |
| `d1ee586` | 2026-06-24 | Finalización de la relación virtual factura↔transacciones (commit más reciente)   |

## Cómo navegar entre los commits

Para revisar el proyecto exactamente como estaba en cualquier punto de su evolución:

```bash
# Ver el historial completo en orden cronológico
git log --oneline --reverse

# Moverse a un commit específico (HEAD queda "desconectado", solo para revisión)
git checkout <hash_del_commit>
# ejemplo: git checkout 9a5952a

# Volver a la rama principal
git checkout master

# Comparar dos commits para ver qué cambió entre ellos
git diff 1a9fefb 9a5952a

# Ver qué archivos cambiaron en un commit puntual
git show --stat <hash_del_commit>
```

> Recomendación para la sustentación: usar `git checkout <hash>` para mostrar en vivo la "Etapa 1" (commit `079aeb0`), luego la "Etapa 2" (por ejemplo `1a9fefb`) y finalmente `master`/`d1ee586` para la "Etapa 3", evidenciando el antes/después de estructura y de persistencia en BD.

## Pendientes antes de la sustentación

Según los criterios de evaluación, el CRUD debe estar **completo** para clientes, facturas y transacciones. Hoy en día quedan abiertos:

1. **Facturas**: implementar la lógica real de `PATCH /facturas/{id_factura}` y `DELETE /facturas/{id_factura}` (actualmente son funciones vacías).
2. **Facturas**: corregir `GET /facturas/{factura_id}` — todavía recorre la lista en memoria `lista_facturas` (siempre vacía) en lugar de consultar la base de datos con `Sesion_dependencia`, igual que ya se hace en `listar_clientes`/`listar_cliente`.
3. **Transacciones**: implementar `GET /transacciones/{id_transaccion}`, `PATCH /transacciones/{id_transaccion}` y `DELETE /transacciones/{id_transaccion}` (actualmente son funciones vacías).
4. **Consistencia de rutas**: unificar `DELETE /cliente/{cliente_id}` (singular) con el resto de rutas de clientes que usan `/clientes` (plural).
5. **Limpieza**: una vez todos los módulos usen la base de datos, `app/listas.py` queda en desuso y puede eliminarse.

## Autor

**Yerik Julián Castañeda Herrera**
Tecnólogo en Análisis y Desarrollo de Software – SENA
Repositorio: [Proyecto_Clientes_FastAPI](https://github.com/YerikHerrera/Proyecto_Clientes_FastAPI)