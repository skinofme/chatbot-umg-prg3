from repositories.producto_repository import ProductoRepository
class ProductoService:

    def __init__(self, conn):
        self.repository = ProductoRepository(conn)

    def buscar_por_nombre(self, nombre):
        return self.repository.buscar_por_nombre(nombre)
    
    def buscar_por_categoria(self, categoria):
        return self.repository.buscar_por_categoria(categoria)