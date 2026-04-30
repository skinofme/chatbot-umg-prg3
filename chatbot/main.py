# chatbot
import connection
from services.producto_service import ProductoService
from services.pedido_service import PedidoService 

conn = connection.get_connection()
prodService = ProductoService(conn)
pedService = PedidoService(conn)

print("Chatbot E-commerce")
print("""______________________________________________________________\n   Hola gracias por preferirnos, como puedo ayudarte?
   escribe alguna de estas palabras clave para que pueda ayudarte con tu consulta: producto, pedido, comprar o salir\n""")

while True:
    opcion = input("Opcion: ").strip().lower()
    
    if opcion == "salir":
        print("Vuelve pronto")
        break

    ## CONSULTA PRODUCTO
    elif opcion == "producto":
        nombre = input("Ingresa el nombre del producto que buscas: ").strip()
        
        productos = prodService.buscar_productos(nombre)
        
        if productos:
            for prod in productos:
                print(f"""
                    ID producto {prod[0]}
                    Nombre: {prod[1]}
                    Categoria: {prod[2]}
                    Marca: {prod[3]}
                    Precio: {prod[4]}
                    Stock: {prod[5]}
                """)
        else:
            print("Ups, parece que no tenemos el producto que buscas, prueba con otro")

    ## CONSULTA PEDIDO
    elif opcion == "pedido":

        pedido_id = int(input("Escribe el ID del pedido que quieres consultar: "))
        result = pedService.buscar_pedido_completo(pedido_id)
        
        if result:

            pedido = result["pedido"]
            detalles = result["detalles"]

            print(f"""
                Pedido #{pedido[0]}
                Cliente: {pedido[1]}
                Fecha: {pedido[2]}
                Total: Q {pedido[3]}
            """)
            for det in detalles:
                print(f"""
                Detalles:
                      
                Producto: {det[0]},
                Cantidad: {det[1]},
                Precio Unitario: Q {det[2]}
                """)
        else: print("No se encontro el pedido")

    elif opcion == "comprar":
        print("Estamos trabajando para que pronto puedas comprar desde aqui")

    else: print("Parece que eres pendejo, prueba escribir: producto, pedido, comprar o salir")

conn.close()