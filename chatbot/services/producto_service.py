from repositories.producto_repository import ProductoRepository
class ProductoService:

    def __init__(self, conn):
        self.repository = ProductoRepository(conn)

    def buscar_productos(self, nombre):
        return self.repository.buscar_producto(nombre)