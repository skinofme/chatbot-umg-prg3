-- =========================================================
-- SEED PROFESIONAL E-COMMERCE
-- PostgreSQL
-- =========================================================

-- =========================================================
-- CATEGORIAS
-- =========================================================

INSERT INTO categoria (nombre)
VALUES
('Smartphones'),
('Laptops'),
('Audio'),
('Televisores'),
('Ropa Deportiva'),
('Calzado'),
('Snacks'),
('Bebidas');



-- =========================================================
-- MARCAS
-- =========================================================

INSERT INTO marca (nombre)
VALUES
('Apple'),
('Samsung'),
('Sony'),
('LG'),
('Nike'),
('Adidas'),
('Puma'),
('Nestlé'),
('Coca-Cola'),
('Lenovo'),
('HP'),
('Dell');



-- =========================================================
-- PRODUCTOS
-- 5000 productos realistas
-- =========================================================

INSERT INTO producto
(nombre, categoria_id, marca_id, precio, stock, descripcion, activo)

SELECT

    CASE categoria_id

        WHEN 1 THEN
            (ARRAY[
                'iPhone 15',
                'Galaxy S24',
                'Xiaomi Redmi Note',
                'Pixel 8',
                'Moto Edge'
            ])[floor(random() * 5 + 1)]

        WHEN 2 THEN
            (ARRAY[
                'MacBook Air',
                'ThinkPad X1',
                'HP Pavilion',
                'Dell XPS',
                'Lenovo Legion'
            ])[floor(random() * 5 + 1)]

        WHEN 3 THEN
            (ARRAY[
                'AirPods Pro',
                'Sony WH-1000XM5',
                'Galaxy Buds',
                'JBL Charge',
                'LG Sound Bar'
            ])[floor(random() * 5 + 1)]

        WHEN 4 THEN
            (ARRAY[
                'LG OLED 55',
                'Samsung Crystal UHD',
                'Sony Bravia',
                'LG NanoCell',
                'Samsung QLED'
            ])[floor(random() * 5 + 1)]

        WHEN 5 THEN
            (ARRAY[
                'Camiseta Dry Fit',
                'Short Deportivo',
                'Sudadera Running',
                'Pants Training',
                'Chaqueta Sport'
            ])[floor(random() * 5 + 1)]

        WHEN 6 THEN
            (ARRAY[
                'Nike Air Max',
                'Adidas Ultraboost',
                'Puma RS-X',
                'Nike Revolution',
                'Adidas Campus'
            ])[floor(random() * 5 + 1)]

        WHEN 7 THEN
            (ARRAY[
                'Doritos',
                'Cheetos',
                'KitKat',
                'Chocobreak',
                'Galletas Oreo'
            ])[floor(random() * 5 + 1)]

        ELSE
            (ARRAY[
                'Coca-Cola 2L',
                'Pepsi 1L',
                'Agua Pura',
                'Té Frío',
                'Jugo Natural'
            ])[floor(random() * 5 + 1)]

    END

    || ' '
    || gs,

    categoria_id,

    CASE categoria_id
        WHEN 1 THEN (ARRAY[1,2])[floor(random()*2+1)]
        WHEN 2 THEN (ARRAY[1,10,11,12])[floor(random()*4+1)]
        WHEN 3 THEN (ARRAY[1,2,3,4])[floor(random()*4+1)]
        WHEN 4 THEN (ARRAY[2,3,4])[floor(random()*3+1)]
        WHEN 5 THEN (ARRAY[5,6,7])[floor(random()*3+1)]
        WHEN 6 THEN (ARRAY[5,6,7])[floor(random()*3+1)]
        WHEN 7 THEN 8
        ELSE 9
    END,

    CASE categoria_id
        WHEN 1 THEN (7000 + random()*8000)
        WHEN 2 THEN (5000 + random()*12000)
        WHEN 3 THEN (300 + random()*2500)
        WHEN 4 THEN (2500 + random()*10000)
        WHEN 5 THEN (100 + random()*400)
        WHEN 6 THEN (300 + random()*1200)
        WHEN 7 THEN (5 + random()*30)
        ELSE (3 + random()*20)
    END::NUMERIC(10,2),

    (random()*150)::INT,

    'Producto categoría ' || categoria_id,

    random() > 0.08

FROM (
    SELECT
        gs,
        ((gs - 1) % 8) + 1 AS categoria_id
    FROM generate_series(1, 5000) gs
) t;



-- =========================================================
-- CLIENTES
-- 3000 clientes
-- =========================================================

INSERT INTO cliente (nombre)

SELECT

    (ARRAY[
        'Juan Pérez',
        'María López',
        'Carlos Ramírez',
        'Ana García',
        'Luis Hernández',
        'Sofía Morales',
        'Pedro Castillo',
        'Andrea Méndez',
        'José González',
        'Fernanda Ruiz'
    ])[floor(random()*10+1)]

    || ' '

    || gs

FROM generate_series(1, 3000) gs;



-- =========================================================
-- PEDIDOS
-- 10000 pedidos distribuidos en el año
-- =========================================================

INSERT INTO pedido (cliente_id, fecha, total)

SELECT

    (random()*2999 + 1)::INT,

    CURRENT_TIMESTAMP
    - (random() * INTERVAL '365 days'),

    0

FROM generate_series(1, 10000);



-- =========================================================
-- DETALLE PEDIDOS
-- Cada pedido tendrá entre 1 y 5 productos
-- =========================================================

INSERT INTO detalle_pedido
(pedido_id, producto_id, cantidad, precio_unitario)

SELECT

    p.id,

    pr.id,

    (random()*4 + 1)::INT,

    pr.precio

FROM pedido p

JOIN LATERAL (

    SELECT
        id,
        precio

    FROM producto

    WHERE activo = TRUE

    ORDER BY random()

    LIMIT (random()*4 + 1)::INT

) pr ON TRUE;



-- =========================================================
-- ACTUALIZAR TOTALES
-- =========================================================

UPDATE pedido p

SET total = sub.total

FROM (

    SELECT
        pedido_id,
        SUM(cantidad * precio_unitario) AS total

    FROM detalle_pedido

    GROUP BY pedido_id

) sub

WHERE p.id = sub.pedido_id;



-- =========================================================
-- ÍNDICES EXTRA
-- =========================================================

CREATE INDEX idx_pedido_cliente
ON pedido(cliente_id);

CREATE INDEX idx_pedido_fecha
ON pedido(fecha);

CREATE INDEX idx_detalle_pedido
ON detalle_pedido(pedido_id);

CREATE INDEX idx_detalle_producto
ON detalle_pedido(producto_id);



-- =========================================================
-- CONSULTAS DE PRUEBA
-- =========================================================

-- Total productos
SELECT COUNT(*) FROM producto;

-- Total clientes
SELECT COUNT(*) FROM cliente;

-- Total pedidos
SELECT COUNT(*) FROM pedido;

-- Total detalles
SELECT COUNT(*) FROM detalle_pedido;

-- Top productos más caros
SELECT nombre, precio
FROM producto
ORDER BY precio DESC
LIMIT 10;

-- Pedidos más altos
SELECT id, total
FROM pedido
ORDER BY total DESC
LIMIT 10;