CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de productos  
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    image_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de carritos
CREATE TABLE carts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_cart_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla de items del carrito
CREATE TABLE cart_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cart_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    added_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_item_cart FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    CONSTRAINT fk_item_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT unique_cart_product UNIQUE (cart_id, product_id) -- un producto solo una vez por carrito
);

-- =======================================
-- Índices adicionales
-- =======================================
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);

-- =======================================
-- Datos de prueba
-- =======================================
INSERT INTO users (username, email, password_hash) VALUES
('admin', 'admin@tienda.com', '$2b$12$yL1SOHWB6Dq4fWfpf73ZNepywLKsGcZmsWTFC0JpjQSVb4ooXCBn6'),
('juan', 'juan@correo.com', '$2b$12$lkMCIbGQBK.Euo.2b/mWPOJFd/xSwR8BNbZrI3RGcOh7aa2VNmHt6');

INSERT INTO products (name, description, price, stock, image_url) VALUES
('Laptop', 'Laptop de 15 pulgadas con 8GB RAM', 2500.00, 10, 'https://via.placeholder.com/150'),
('Mouse', 'Mouse inalámbrico', 50.00, 100, 'https://via.placeholder.com/150'),
('Teclado', 'Teclado mecánico retroiluminado', 120.00, 50, 'https://via.placeholder.com/150');
