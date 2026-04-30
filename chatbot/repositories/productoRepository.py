class ProductoRepository:

    def __init__(self, connection):
        self.connection = connection
    
    def buscar_producto(self, nombre):
        with self.connection.cursor() as cursor:
        
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
            """,("%" + nombre + "%",)
            )

            return cursor.fetchall()
      