-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Configurar zona horaria
SET timezone = 'America/Bogota';

-- Crear la base de datos si no existe
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'tienda_db'
   ) THEN
      PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE tienda_db');
   END IF;
END
$$;

-- Crear usuario si no existe
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_roles WHERE rolname = 'tienda_user'
   ) THEN
      CREATE ROLE tienda_user LOGIN PASSWORD 'tienda_password';
   END IF;
END
$$;

-- Conceder privilegios al usuario sobre la base de datos
GRANT ALL PRIVILEGES ON DATABASE tienda_db TO tienda_user;
