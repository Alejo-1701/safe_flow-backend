# Safe Flow Backend

API REST para la gestión de accessos, parqueaderos, residentes y novedades de conjuntos residenciales.

## Stack

- Python 3.13
- Django 5.2 y Django REST Framework 3.18
- drf-spectacular para el esquema OpenAPI y Swagger
- PostgreSQL en Neon mediante `psycopg` 3
- Gunicorn para producción

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

En Windows, activá el entorno con `.venv\Scripts\activate` y copiá la plantilla con `copy .env.example .env`.

## Variables de entorno

Copiá `.env.example` a `.env` y completá los valores. El archivo `.env` está ignorado por Git.

| Variable | Uso |
| --- | --- |
| `DATABASE_URL` | Cadena de conexión a Neon. Obligatoria. |
| `SECRET_KEY` | Clave de Django. Obligatoria cuando `DEBUG=False`. |
| `DEBUG` | `True` solo en desarrollo; por defecto es `False`. |
| `ALLOWED_HOSTS` | Lista separada por comas. Obligatoria cuando `DEBUG=False`. |
| `CORS_ALLOW_ALL_ORIGINS` | Por defecto `False`. Habilitar solo en desarrollo. |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos separados por comas. |

Cuando `DEBUG=False` se activan redirección HTTPS, cookies seguras, HSTS y `SECURE_PROXY_SSL_HEADER` para despliegues detrás de proxy.

## Arranque local

```bash
python manage.py runserver
```

La documentación interactiva queda en `/api/docs/` y el esquema OpenAPI en `/api/schema/`.

## Pruebas

```bash
python manage.py test --settings=config.settings_test --testrunner=config.test_runner.SeedRunner --verbosity 2
```

La suite usa SQLite en memoria: `config/test_schema.py` crea y siembra las 23 tablas porque los modelos son `managed=False`. No conecta con Neon ni genera migraciones.

## Endpoints

Escritura completa (GET, POST, PUT, PATCH, DELETE) solo en estos recursos:

| Prefijo | Recursos |
| --- | --- |
| `/api/comun/` | `notificaciones`, `notificacion-estados` |
| `/api/usuarios/` | `perfiles` |
| `/api/personas/` | `roles`, `empresas`, `personas`, `telefonos`, `correos`, `administradores`, `guardias`, `residentes` |

Solo lectura (GET) en el resto:

| Prefijo | Recursos |
| --- | --- |
| `/api/` | `vehiculos` |
| `/api/infraestructura/` | `apartamentos`, `parqueaderos`, `asambleas` |
| `/api/accesos/` | `turnos`, `registros-acceso` |
| `/api/visitas/` | `autorizaciones` |
| `/api/financiero/` | `tarifas`, `pagos`, `recaudos` |
| `/api/novedades/` | `incidentes`, `solicitudes` |

Los listados admiten filtros por query params en vehículos, apartamentos, parqueaderos, turnos, registros de acceso y autorizaciones de visita.

### Acciones de solo lectura

| Ruta | Resultado |
| --- | --- |
| `/api/comun/notificaciones/no-leidas/` | Notificaciones sin leer |
| `/api/comun/notificacion-estados/por-notificacion/{id}/` | Historial de una notificación |
| `/api/usuarios/perfiles/activos/` | Perfiles activos, sin contraseña |
| `/api/personas/personas/por-rol/{id}/` | Personas de un rol |
| `/api/personas/personas/por-empresa/{nit}/` | Personas de una empresa |
| `/api/personas/telefonos/por-persona/{doc}/` | Teléfonos de una persona |
| `/api/personas/correos/por-persona/{doc}/` | Correos de una persona |

El detalle de teléfonos y correos usa la documentación en la URL y admite `?telefono=` o `?email=` para elegir el registro cuando hay varios.

## Decisiones

- Las tablas ya existen en Neon: los modelos usan `managed=False`, `db_table` exacto y foreign keys con `DO_NOTHING`. No se ejecutan migraciones propias.
- La contraseña de `Perfil` se valida, se hashea con `make_password` y se expone como `write_only`.
- Los permisos son `AllowAny` por decisión del equipo; no hay JWT ni control por roles.
- Cada router define un `root_view_name` propio para evitar nombres duplicados.
- `/admin/` no está expuesto: Neon no contiene las tablas de `django.contrib`.
- Frontend y documentación de arquitectura quedan fuera de este repositorio.

## Despliegue

El `Procfile` inicia la aplicación con Gunicorn. La plataforma debe proveer `PORT` y las variables de entorno indicadas.

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Los archivos estáticos de Swagger requieren servir `STATIC_ROOT` con el servidor o CDN de la plataforma.

## Pendientes

- Paginación global: hoy las listas devuelven arreglos completos.
