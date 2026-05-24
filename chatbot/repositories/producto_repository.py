class ProductoRepository:

    def __init__(self, connection):
        self.connection = connection
    
    def buscar_por_nombre(self, nombre):
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
                LIMIT 15
            """,("%" + nombre + "%",)
            )

            return cursor.fetchall()
    
    def buscar_por_categoria(self, categoria):
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
                WHERE c.nombre ILIKE %s
                AND p.activo = TRUE
                LIMIT 15
            """,("%" + categoria + "%",)
            )
            return cursor.fetchall()
      