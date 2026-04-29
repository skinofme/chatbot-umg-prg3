-- CATEGORIAS

    INSERT INTO categoria (nombre)
    VALUES 
    ('Tecnología'),
    ('Comida'),
    ('Ropa');


-- MARCAS

    INSERT INTO marca (nombre)
    VALUES
    ('Apple'),
    ('Samsung'),
    ('Nike'),
    ('Adidas'),
    ('Sony'),
    ('LG'),
    ('Zara'),
    ('Nestlé');


-- PRODUCTOS

    INSERT INTO producto (nombre, categoria_id, marca_id, precio, stock, descripcion)
    SELECT
        'Producto ' || gs,

        ((gs - 1) % 3) + 1,

        ((gs - 1) % 8) + 1,

        CASE
            WHEN ((gs - 1) % 3) + 1 = 1 THEN (500 + random() * 4500)
            WHEN ((gs - 1) % 3) + 1 = 2 THEN (10 + random() * 90)
            ELSE (100 + random() * 400)
        END::NUMERIC(10,2),

        (random() * 100)::INT,

        'Descripción del producto ' || gs

    FROM generate_series(1, 10000) AS gs;


-- CLIENTES

    INSERT INTO cliente (nombre)
    SELECT
        'Cliente ' || gs
    FROM generate_series(1, 10000) AS gs;


-- PEDIDOS

    INSERT INTO pedido (cliente_id, fecha)
    SELECT
        ((gs - 1) % 10000) + 1,
        CURRENT_TIMESTAMP - (gs || ' minutes')::INTERVAL
    FROM generate_series(1, 10000) AS gs;


-- DETALLE PEDIDOS

    INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario)
    SELECT
        p.id,

        ((p.id * 7 + linea * 3) % 10000) + 1,

        (random() * 3 + 1)::INT,

        pr.precio

    FROM pedido p
    CROSS JOIN generate_series(1, 2) AS linea
    JOIN producto pr 
        ON pr.id = ((p.id * 7 + linea * 3) % 10000) + 1;



-- ACTUALIZAR TOTALES

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

