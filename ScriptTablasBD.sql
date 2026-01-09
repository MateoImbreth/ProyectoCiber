-- =====================================================================
-- Script para la creación de las tablas Usuarios y Detalle_Usuarios
-- =====================================================================

-- Se recomienda ejecutar estas sentencias dentro de una transacción
-- para asegurar que ambas tablas se creen correctamente.
BEGIN;

-- -----------------------------------------------------
-- Tabla: usuarios
-- -----------------------------------------------------
-- Esta tabla almacena la información principal y pública del usuario.
-- Se crea primero porque 'detalle_usuarios' depende de ella.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    -- SERIAL es un tipo de dato autoincremental en PostgreSQL (INTEGER),
    -- perfecto para una llave primaria.
    id_usuario SERIAL PRIMARY KEY,

    -- VARCHAR(50) corresponde a str con max_length=50.
    -- NOT NULL porque el campo no es opcional en el modelo.
    nick_name VARCHAR(50) NOT NULL,

    -- El tipo DATE en PostgreSQL corresponde directamente al 'date' de Python.
    -- NOT NULL porque el campo no es opcional.
    fecha DATE NOT NULL,

    -- VARCHAR(255) es una longitud por defecto razonable para un nombre.
    -- NULL es permitido porque el campo es 'Optional' en el modelo.
    nombre VARCHAR(255) NULL
);

-- -----------------------------------------------------
-- Tabla: detalle_usuarios
-- -----------------------------------------------------
-- Esta tabla almacena detalles sensibles y de configuración de la cuenta.
-- Tiene una relación de uno a uno (o uno a muchos si se quisiera) con 'usuarios'.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS detalle_usuarios (
    id_detalle_usuarios SERIAL PRIMARY KEY,

    -- Llave foránea que referencia a la tabla 'usuarios'.
    -- Debe ser del mismo tipo que 'usuarios.id_usuario' (INTEGER).
    -- NOT NULL para asegurar que todo detalle siempre pertenezca a un usuario.
    id_usuario INTEGER NOT NULL,

    -- VARCHAR(255) es una buena elección para almacenar contraseñas hasheadas.
    contrasena VARCHAR(255) NOT NULL,

    -- TEXT es ideal para tokens (como JWT) que pueden tener una longitud variable y larga.
    -- NULL es permitido porque el campo es 'Optional'.
    token TEXT NULL,

    -- INTEGER para el grupo del usuario.
    grupo INTEGER NOT NULL,

    -- VARCHAR(255) para el email. Se añade una restricción UNIQUE
    -- para asegurar que no haya dos usuarios con el mismo email.
    email VARCHAR(255) NOT NULL UNIQUE,

    -- El tipo BOOLEAN en PostgreSQL corresponde a 'bool' de Python.
    estado_cuenta BOOLEAN NOT NULL,

    -- Definición de la llave foránea (Foreign Key).
    -- Se nombra la restricción (CONSTRAINT) para poder identificarla fácilmente.
    CONSTRAINT fk_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios (id_usuario)
        -- ON DELETE CASCADE asegura que si un usuario es eliminado,
        -- sus detalles asociados también se eliminen automáticamente.
        ON DELETE CASCADE
);


-- -----------------------------------------------------
-- Índice para la llave foránea
-- -----------------------------------------------------
-- Crear un índice en la columna de la llave foránea (id_usuario)
-- mejora significativamente el rendimiento de las consultas que
-- unen ambas tablas (JOINs) y de las operaciones de borrado en cascada.
-- -----------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_detalle_usuarios_id_usuario ON detalle_usuarios(id_usuario);

-- Finalizar la transacción
COMMIT;