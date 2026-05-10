import connection
from services.producto_service import ProductoService
from services.pedido_service import PedidoService 

conn = connection.get_connection()
prodService = ProductoService(conn)
pedService = PedidoService(conn)


def procesar_input(opcion):
    opcion = opcion.strip().lower()

    if opcion == "salir":
        return "Vuelve pronto"

    elif opcion == "producto":
        return "__PEDIR_NOMBRE_PRODUCTO__"

    elif opcion.startswith("producto:"):
        nombre = opcion.split(":", 1)[1].strip()
        productos = prodService.buscar_productos(nombre)

        if productos:
            respuesta = ""
            for prod in productos:
                respuesta += f"""
                    ID producto {prod[0]}
                    Nombre: {prod[1]}
                    Categoria: {prod[2]}
                    Marca: {prod[3]}
                    Precio: {prod[4]}
                    Stock: {prod[5]}
                """
            return respuesta
        else:
            return "Ups, parece que no tenemos el producto que buscas, prueba con otro"

    elif opcion == "pedido":
        return "__PEDIR_ID_PEDIDO__"

    elif opcion.startswith("pedido:"):
        pedido_id = int(opcion.split(":", 1)[1].strip())
        result = pedService.buscar_pedido_completo(pedido_id)

        if result:
            pedido = result["pedido"]
            detalles = result["detalles"]

            respuesta = f"""
                Pedido #{pedido[0]}
                Cliente: {pedido[1]}
                Fecha: {pedido[2]}
                Total: Q {pedido[3]}
            """

            for det in detalles:
                respuesta += f"""
                Detalles:
                      
                Producto: {det[0]},
                Cantidad: {det[1]},
                Precio Unitario: Q {det[2]}
                """

            return respuesta
        else:
            return "No se encontro el pedido"

    elif opcion == "comprar":
        return "Estamos trabajando para que pronto puedas comprar desde aqui"

    else:
        return "No tenemos esa opción \nprueba escribir: producto, pedido, comprar o salir"