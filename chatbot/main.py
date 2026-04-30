# chatbot
import connection
from repositories.producto_repository import ProductoRepository
from repositories.pedido_repository import PedidoRepository

conn = connection.get_connection()
prodRepo = ProductoRepository(conn)
pedRepo = PedidoRepository(conn)

print("Chatbot E-commerce")
print("Escribe: producto, pedido, comprar o salir")

while True:
    opcion = input("Opcion: ").strip().lower()
    
    if opcion == "salir":
        print("Adios")
        break

    ## CONSULTA PRODUCTO
    elif opcion == "producto":
        nombre = input("Ingresa el nombre del producto: ").strip()
        
        datos = prodRepo.buscar_producto(nombre)
        
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
        pedido_id = int(input("ID del pedido: "))
        
        # 1. Encabezado del pedido
        pedido = pedRepo.buscar_pedido_por_id(pedido_id)
        
        if pedido:
            print("\n=== PEDIDO ===")
            print("ID:", pedido[0])
            print("Cliente:", pedido[1])
            print("Fecha:", pedido[2])
            print("Total:", pedido[3])

            # 2. Detalle del pedido
            detalles = pedRepo.buscar_detalles_por_pedido_id(pedido_id)

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

conn.close()