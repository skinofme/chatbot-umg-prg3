class PedidoRepository:

    def __init__(self, connection):
        self.connection = connection

    def buscar_pedido_por_id(self, pedido_id):
        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT ped.id, cli.nombre, ped.fecha, ped.total
                FROM pedido ped
                JOIN cliente cli ON ped.cliente_id = cli.id
                WHERE ped.id = %s
                """,(pedido_id,)
            )
            return cursor.fetchone()
        
    def buscar_detalles_por_pedido_id(self, pedido_id):
        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT prod.nombre, det.cantidad, det.precio_unitario
                FROM detalle_pedido det 
                JOIN producto prod ON prod.id = det.producto_id
                WHERE det.pedido_id = %s
                """,(pedido_id,)
            )
            return cursor.fetchall()