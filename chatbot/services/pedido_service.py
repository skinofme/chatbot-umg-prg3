from repositories.pedido_repository import PedidoRepository

class PedidoService:

    def __init__(self, conn):
        self.repository = PedidoRepository(conn)

    def buscar_pedido_completo(self, pedido_id):
        pedido = self.repository.buscar_pedido_por_id(pedido_id)
        
        if not pedido: return None
        
        detalles = self.repository.buscar_detalles_por_pedido_id(pedido_id)

        return {
            "pedido": pedido,
            "detalles": detalles
        }
    
    def crear_compra(self, producto_id, cantidad, cliente_id=1):
        """
        Crea una nueva compra (pedido) para un cliente.
        Retorna mensaje formateado con confirmación o error.
        """
        try:
            # Validar que producto_id sea numérico
            producto_id = int(producto_id)
        except (ValueError, TypeError):
            return "Error: El ID del producto debe ser un número entero."
        
        try:
            # Validar que cantidad sea numérica y positiva
            cantidad = int(cantidad)
            if cantidad <= 0:
                return "Error: La cantidad debe ser un número mayor a 0."
        except (ValueError, TypeError):
            return "Error: La cantidad debe ser un número entero."
        
        # Crear el pedido
        resultado = self.repository.crear_pedido_con_detalles(cliente_id, producto_id, cantidad)
        
        # Manejar errores
        if "error" in resultado:
            return f"❌ {resultado['error']}"
        
        # Formatear respuesta exitosa
        pedido_id = resultado["pedido_id"]
        cliente_nombre = resultado["cliente_nombre"]
        producto_nombre = resultado["producto_nombre"]
        precio_unitario = resultado["precio_unitario"]
        total = resultado["total"]
        fecha = resultado["fecha"]
        
        respuesta = f"""✅ ¡COMPRA EXITOSA!
__________________________
Pedido #{pedido_id}
Cliente: {cliente_nombre}
Fecha: {fecha}

DETALLES:
Producto: {producto_nombre}
Cantidad: {cantidad} unidad(es)
Precio Unitario: Q {precio_unitario:,.2f}
TOTAL: Q {total:,.2f}
__________________________

💡 Puedes consultar tu pedido escribiendo: pedido {pedido_id}"""
        
        return respuesta