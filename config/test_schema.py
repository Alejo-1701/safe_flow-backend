ESQUEMA = """
CREATE TABLE roles (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_rol VARCHAR(15) NOT NULL UNIQUE
);
CREATE TABLE empresa_vigilancia (
    nit VARCHAR(20) PRIMARY KEY,
    nombre_empresa VARCHAR(100) NOT NULL,
    rep_legal VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    direccion VARCHAR(100) NOT NULL
);
CREATE TABLE personas (
    num_documento VARCHAR(10) PRIMARY KEY,
    tipo_documento VARCHAR(2) NOT NULL,
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50) NOT NULL,
    id_rol INTEGER NOT NULL REFERENCES roles(id_rol) ON DELETE RESTRICT,
    nit_empresa VARCHAR(20) REFERENCES empresa_vigilancia(nit) ON DELETE SET NULL
);
CREATE TABLE persona_telefonos (
    doc_persona VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE CASCADE,
    telefono VARCHAR(15) NOT NULL,
    PRIMARY KEY (doc_persona, telefono)
);
CREATE TABLE persona_correo (
    doc_persona VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE CASCADE,
    email VARCHAR(250) NOT NULL,
    PRIMARY KEY (doc_persona, email)
);
CREATE TABLE administrador (
    numero_documento VARCHAR(10) PRIMARY KEY REFERENCES personas(num_documento) ON DELETE CASCADE,
    rol VARCHAR(50) NOT NULL,
    inicio_gestion DATE NOT NULL,
    fin_gestion DATE
);
CREATE TABLE guardia_seguridad (
    numero_documento VARCHAR(10) PRIMARY KEY REFERENCES personas(num_documento) ON DELETE CASCADE,
    empresa VARCHAR(100) NOT NULL
);
CREATE TABLE apartamento (
    id_apartamento INTEGER PRIMARY KEY AUTOINCREMENT,
    torre VARCHAR(10) NOT NULL,
    numero_apto VARCHAR(10) NOT NULL,
    doc_propietario VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE RESTRICT
);
CREATE TABLE residente (
    numero_documento VARCHAR(10) PRIMARY KEY REFERENCES personas(num_documento) ON DELETE CASCADE,
    id_apartamento INTEGER NOT NULL REFERENCES apartamento(id_apartamento) ON DELETE RESTRICT
);
CREATE TABLE parqueadero (
    id_parqueadero VARCHAR(20) PRIMARY KEY,
    tipo_celda VARCHAR(20) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    id_apto_asignado INTEGER REFERENCES apartamento(id_apartamento) ON DELETE SET NULL
);
CREATE TABLE perfil (
    doc_persona VARCHAR(10) PRIMARY KEY REFERENCES personas(num_documento) ON DELETE CASCADE,
    contrasenia VARCHAR(255) NOT NULL,
    estado_perfil BOOLEAN DEFAULT 1
);
CREATE TABLE notificacion (
    id_notificacion INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo VARCHAR(30) NOT NULL,
    mensaje TEXT NOT NULL,
    leido BOOLEAN DEFAULT 0,
    numero_documento VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE CASCADE
);
CREATE TABLE notificacion_estados (
    id_estado_hist INTEGER PRIMARY KEY AUTOINCREMENT,
    id_notificacion INTEGER NOT NULL REFERENCES notificacion(id_notificacion) ON DELETE CASCADE,
    nuevo_estado VARCHAR(20) NOT NULL,
    duracion NUMERIC NOT NULL,
    fecha_cambio DATE NOT NULL,
    hora_cambio TIME NOT NULL
);
CREATE TABLE vehiculos (
    placa VARCHAR(10) PRIMARY KEY,
    numero_chasis VARCHAR(30) NOT NULL UNIQUE,
    tipo VARCHAR(20) NOT NULL,
    linea VARCHAR(50) NOT NULL,
    modelo INTEGER NOT NULL,
    cilindraje INTEGER NOT NULL,
    color VARCHAR(20) NOT NULL,
    servicio VARCHAR(20) NOT NULL,
    clase_vehiculo VARCHAR(20) NOT NULL,
    doc_propietario VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE RESTRICT
);
CREATE TABLE asamblea_copropietarios (
    id_asamblea INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_acta VARCHAR(20) NOT NULL,
    fecha_reunion DATE NOT NULL,
    art_referencia VARCHAR(30) NOT NULL,
    des_acuerdo TEXT NOT NULL
);
CREATE TABLE turno (
    id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_turno DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    recaudo_fisico NUMERIC NOT NULL,
    observaciones TEXT,
    num_documento_guardia VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE RESTRICT
);
CREATE TABLE registro_acceso (
    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
    placa VARCHAR(10) NOT NULL REFERENCES vehiculos(placa) ON DELETE RESTRICT,
    id_turno INTEGER NOT NULL REFERENCES turno(id_turno) ON DELETE RESTRICT,
    fecha_entrada DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    fecha_salida DATE,
    hora_salida TIME
);
CREATE TABLE autorizacion_visita (
    id_autorizacion INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_programada DATE NOT NULL,
    doc_residente VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE CASCADE,
    doc_visitante VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE CASCADE,
    placa_vehiculo VARCHAR(10) REFERENCES vehiculos(placa) ON DELETE SET NULL
);
CREATE TABLE tarifa (
    id_tarifa INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_vehiculo VARCHAR(20) NOT NULL,
    valor_minuto NUMERIC NOT NULL,
    id_asamblea INTEGER NOT NULL REFERENCES asamblea_copropietarios(id_asamblea) ON DELETE RESTRICT
);
CREATE TABLE pago (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    metodo_pago VARCHAR(20) NOT NULL,
    fecha_caja DATE NOT NULL,
    hora_caja TIME NOT NULL,
    monto_total NUMERIC NOT NULL,
    id_registro INTEGER NOT NULL REFERENCES registro_acceso(id_registro) ON DELETE RESTRICT,
    id_turno INTEGER NOT NULL REFERENCES turno(id_turno) ON DELETE RESTRICT
);
CREATE TABLE recaudo (
    numero_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pago INTEGER NOT NULL REFERENCES pago(id_pago) ON DELETE RESTRICT,
    id_tarifa INTEGER NOT NULL REFERENCES tarifa(id_tarifa) ON DELETE RESTRICT,
    id_confirmacion VARCHAR(50) NOT NULL,
    sub_total NUMERIC NOT NULL,
    total_pagado NUMERIC NOT NULL
);
CREATE TABLE incidentes (
    id_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_persona VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE CASCADE,
    descripcion TEXT NOT NULL,
    fecha_incidente DATE NOT NULL
);
CREATE TABLE solicitud (
    id_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_persona VARCHAR(10) NOT NULL REFERENCES personas(num_documento) ON DELETE CASCADE,
    descripcion TEXT NOT NULL,
    fecha_solicitud DATE NOT NULL,
    estado_solicitud VARCHAR(20) NOT NULL DEFAULT 'Pendiente'
);
"""

FILAS = [
    ("INSERT INTO roles VALUES (?, ?)", (1, "Administrador")),
    ("INSERT INTO roles VALUES (?, ?)", (2, "Guardia")),
    ("INSERT INTO roles VALUES (?, ?)", (3, "Residente")),
    (
        "INSERT INTO empresa_vigilancia VALUES (?, ?, ?, ?, ?, ?)",
        ("900123456", "Seguridad Integral SA", "Carlos Perez", "3001234567", "contacto@seguridad.com", "Calle 1 #2-3"),
    ),
    ("INSERT INTO personas VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ("1000000001", "CC", "Ana", None, "Lopez", "Gomez", 1, "900123456")),
    ("INSERT INTO personas VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ("1000000002", "CC", "Juan", "Diego", "Perez", "Diaz", 2, "900123456")),
    ("INSERT INTO personas VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ("1000000003", "TI", "Maria", None, "Ruiz", "Castro", 3, None)),
    ("INSERT INTO perfil VALUES (?, ?, ?)", ("1000000001", "hash-prueba-1", 1)),
    ("INSERT INTO perfil VALUES (?, ?, ?)", ("1000000002", "hash-prueba-2", 1)),
    ("INSERT INTO perfil VALUES (?, ?, ?)", ("1000000003", "hash-prueba-3", 0)),
    ("INSERT INTO persona_telefonos VALUES (?, ?)", ("1000000001", "3001112233")),
    ("INSERT INTO persona_telefonos VALUES (?, ?)", ("1000000002", "3004455667")),
    ("INSERT INTO persona_telefonos VALUES (?, ?)", ("1000000003", "3007788990")),
    ("INSERT INTO persona_correo VALUES (?, ?)", ("1000000001", "ana@example.com")),
    ("INSERT INTO persona_correo VALUES (?, ?)", ("1000000002", "juan@example.com")),
    ("INSERT INTO persona_correo VALUES (?, ?)", ("1000000003", "maria@example.com")),
    ("INSERT INTO administrador VALUES (?, ?, ?, ?)", ("1000000001", "Admin general", "2026-01-01", None)),
    ("INSERT INTO guardia_seguridad VALUES (?, ?)", ("1000000002", "Seguridad Integral SA")),
    ("INSERT INTO apartamento VALUES (?, ?, ?, ?)", (402, "A", "402", "1000000001")),
    ("INSERT INTO residente VALUES (?, ?)", ("1000000003", 402)),
    ("INSERT INTO parqueadero VALUES (?, ?, ?, ?)", ("P-001", "Carro", "Disponible", 402)),
    ("INSERT INTO parqueadero VALUES (?, ?, ?, ?)", ("P-002", "Moto", "Mantenimiento", None)),
    ("INSERT INTO notificacion VALUES (?, ?, ?, ?, ?)", (1, "Acceso", "Ingreso registrado", 0, "1000000003")),
    ("INSERT INTO notificacion_estados VALUES (?, ?, ?, ?, ?, ?)", (1, 1, "Pendiente", 3600000000, "2026-11-24", "08:30:00")),
    ("INSERT INTO vehiculos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("ABC123", "CHS-0001", "Carro", "Renault", 2022, 1600, "Blanco", "Particular", "Automovil", "1000000003")),
    ("INSERT INTO asamblea_copropietarios VALUES (?, ?, ?, ?, ?)", (1, "ACT-001", "2026-10-15", "Articulo 12", "Se aprueba la tarifa")),
    ("INSERT INTO turno VALUES (?, ?, ?, ?, ?, ?, ?)", (1, "2026-11-24", "08:00:00", "16:00:00", 150000.00, None, "1000000002")),
    ("INSERT INTO registro_acceso VALUES (?, ?, ?, ?, ?, ?, ?)", (1, "ABC123", 1, "2026-11-24", "09:15:00", "2026-11-24", "17:45:00")),
    ("INSERT INTO autorizacion_visita VALUES (?, ?, ?, ?, ?)", (1, "2026-11-26", "1000000003", "1000000001", "ABC123")),
    ("INSERT INTO tarifa VALUES (?, ?, ?, ?)", (1, "Carro", 1200.00, 1)),
    ("INSERT INTO pago VALUES (?, ?, ?, ?, ?, ?, ?)", (1, "Efectivo", "2026-11-24", "17:50:00", 10200.00, 1, 1)),
    ("INSERT INTO recaudo VALUES (?, ?, ?, ?, ?, ?)", (1, 1, 1, "CONF-0001", 10200.00, 10200.00)),
    ("INSERT INTO incidentes VALUES (?, ?, ?, ?)", (1, "1000000003", "Porton con falla intermitente", "2026-11-23")),
    ("INSERT INTO solicitud VALUES (?, ?, ?, ?, ?)", (1, "1000000003", "Reposicion de llavero", "2026-11-22", "Pendiente")),
]


def preparar(conexion):
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.executescript(ESQUEMA)
    for sentencia, parametros in FILAS:
        cursor.execute(sentencia, parametros)
    conexion.commit()
