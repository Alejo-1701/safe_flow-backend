# Safe Flow Backend

API REST para la gestión de accessos, parqueaderos, residentes y novedades de conjuntos residenciales.

## Stack

- Python 3.13
- Django 5.2 y Django REST Framework 3.18
- drf-spectacular para el esquema OpenAPI y Swagger
- djangorestframework-simplejwt para tokens JWT
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

`CORS_ALLOWED_ORIGINS` debe incluir el origen exacto del frontend con scheme, host y puerto, sin barra final. Los tokens JWT usan `SECRET_KEY`; no requieren otra variable.

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

Escritura completa (GET, POST, PUT, PATCH, DELETE):

| Prefijo | Recursos |
| --- | --- |
| `/api/comun/` | `notificaciones`, `notificacion-estados` |
| `/api/usuarios/` | `perfiles` |
| `/api/personas/` | `roles`, `empresas`, `personas`, `telefonos`, `correos`, `administradores`, `guardias`, `residentes` |
| `/api/infraestructura/` | `asambleas` |
| `/api/accesos/` | `turnos`, `registros-acceso` |
| `/api/visitas/` | `autorizaciones` |
| `/api/financiero/` | `tarifas`, `pagos`, `recaudos` |
| `/api/novedades/` | `incidentes`, `solicitudes` |

Solo lectura (GET):

| Prefijo | Recursos |
| --- | --- |
| `/api/` | `vehiculos` |
| `/api/infraestructura/` | `apartamentos`, `parqueaderos` |

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

### Acciones de escritura

| Ruta | Resultado |
| --- | --- |
| `POST /api/usuarios/login/` | Tokens `access` y `refresh` con datos básicos del perfil |
| `POST /api/accesos/registros-acceso/ingreso/` | Registra ingreso, reserva la primera celda disponible y la marca como `Ocupado` |
| `POST /api/financiero/pagos/arqueo-turno/` | Compara el recaudo físico con los pagos en efectivo y actualiza el estado del turno |
| `PATCH /api/novedades/solicitudes/{id}/cambiar-estado/` | Actualiza solo `estado_solicitud` |

El login acepta `num_documento` y `contrasenia`. Las acciones responden `400` ante payload inválido; el login responde `401` para credenciales incorrectas y `403` para perfil inactivo.

## Decisiones

- Las tablas ya existen en Neon: los modelos usan `managed=False`, `db_table` exacto y foreign keys con `DO_NOTHING`. No se ejecutan migraciones propias.
- La contraseña de `Perfil` se valida, se hashea con `make_password` y se expone como `write_only`.
- Los permisos globales siguen siendo `AllowAny`: el token JWT es opcional, se valida si se envía y todavía no restringe recursos por rol.
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
- Control de acceso por rol: el token JWT se emite, pero `AllowAny` todavía permite todos los recursos.
