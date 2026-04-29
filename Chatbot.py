# chatbot

import psycopg

conn = psycopg.connect(
    host="localhost",
    port="5432",
    dbname="test_shop",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

print("Chatbot E-commerce")
print("Escribe: producto, pedido, comprar o salir")

while True:
    opcion = input("/Hola: ").strip().lower()
    
    if opcion == "salir":
        print("Adios")
        break

    ## CONSULTA PRODUCTO
    elif opcion == "producto":
        nombre = input("Ingresa el nombre del producto: ").strip()
        
        cursor.execute(
            """
            SELECT 
                p.id,
                p.nombre,
                c.nombre AS categoria,
                m.nombre AS marca,
                p.precio,
                p.stock
            FROM producto p
            JOIN categoria c ON p.categoria_id = c.id
            JOIN marca m ON p.marca_id = m.id
            WHERE p.nombre ILIKE %s
            AND p.activo = TRUE
            """,
            ("%" + nombre + "%",)
        )
        
        datos = cursor.fetchall()
        
        if datos:
            for x in datos:
                print(
                    "ID:", x[0],
                    "| Nombre:", x[1],
                    "| Categoria:", x[2],
                    "| Marca:", x[3],
                    "| Precio:", x[4],
                    "| Stock:", x[5]
                )
        else:
            print("No se encontro informacion")

    ## CONSULTA PEDIDO
    elif opcion == "pedido":
        pedido_id = input("ID del pedido: ").strip()
        
        # 1. Encabezado del pedido
        cursor.execute(
            """
            SELECT 
                p.id,
                c.nombre,
                p.fecha,
                p.total
            FROM pedido p
            JOIN cliente c ON p.cliente_id = c.id
            WHERE p.id = %s
            """,
            (pedido_id,)
        )
        
        pedido = cursor.fetchone()
        
        if pedido:
            print("\n=== PEDIDO ===")
            print("ID:", pedido[0])
            print("Cliente:", pedido[1])
            print("Fecha:", pedido[2])
            print("Total:", pedido[3])

            # 2. Detalle del pedido
            cursor.execute(
                """
                SELECT 
                    pr.nombre,
                    d.cantidad,
                    d.precio_unitario
                FROM detalle_pedido d
                JOIN producto pr ON d.producto_id = pr.id
                WHERE d.pedido_id = %s
                """,
                (pedido_id,)
            )

            detalles = cursor.fetchall()

            print("\n--- Detalles ---")
            for d in detalles:
                print(
                    "Producto:", d[0],
                    "| Cantidad:", d[1],
                    "| Precio Unitario:", d[2]
                )
        else:
            print("No se encontro el pedido")

    elif opcion == "comprar":
        print("Estamos trabajando para que puedas comprar desde el chatbot...")
    else:
        print("Opcion no valida")

cursor.close()
conn.close()