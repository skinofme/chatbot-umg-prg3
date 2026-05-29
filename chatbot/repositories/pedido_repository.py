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
    
    def crear_pedido_con_detalles(self, cliente_id, producto_id, cantidad):
        """
        Crea un nuevo pedido con detalles y actualiza el stock del producto.
        Retorna dict con detalles del pedido o None si hay error.
        """
        try:
            with self.connection.cursor() as cursor:
                # 1. Validar que el producto existe y obtener su información
                cursor.execute(
                    """
                    SELECT id, nombre, precio, stock
                    FROM producto
                    WHERE id = %s AND activo = TRUE
                    """, (producto_id,)
                )
                producto = cursor.fetchone()
                
                if not producto:
                    return {"error": "Producto no encontrado o está inactivo"}
                
                prod_id, prod_nombre, precio_unitario, stock_actual = producto
                
                # 2. Validar que hay stock suficiente
                if stock_actual < cantidad:
                    return {"error": f"Stock insuficiente. Disponible: {stock_actual}, Solicitado: {cantidad}"}
                
                # 3. Calcular total
                total = float(precio_unitario) * cantidad
                
                # 4. Crear el pedido
                cursor.execute(
                    """
                    INSERT INTO pedido (cliente_id, fecha, total)
                    VALUES (%s, NOW(), %s)
                    RETURNING id, fecha
                    """, (cliente_id, total)
                )
                pedido_info = cursor.fetchone()
                pedido_id, fecha_pedido = pedido_info
                
                # 5. Crear el detalle del pedido
                cursor.execute(
                    """
                    INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """, (pedido_id, producto_id, cantidad, precio_unitario)
                )
                
                # 6. Actualizar el stock del producto
                cursor.execute(
                    """
                    UPDATE producto
                    SET stock = stock - %s
                    WHERE id = %s
                    """, (cantidad, producto_id)
                )
                
                # 7. Confirmar cambios
                self.connection.commit()
                
                # 8. Obtener nombre del cliente
                cursor.execute(
                    "SELECT nombre FROM cliente WHERE id = %s",
                    (cliente_id,)
                )
                cliente_info = cursor.fetchone()
                cliente_nombre = cliente_info[0] if cliente_info else "Cliente"
                
                # 9. Retornar información del pedido creado
                return {
                    "pedido_id": pedido_id,
                    "cliente_nombre": cliente_nombre,
                    "producto_nombre": prod_nombre,
                    "cantidad": cantidad,
                    "precio_unitario": float(precio_unitario),
                    "total": total,
                    "fecha": fecha_pedido
                }
        
        except Exception as e:
            self.connection.rollback()
            return {"error": f"Error al crear el pedido: {str(e)}"}