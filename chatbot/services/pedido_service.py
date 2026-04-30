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