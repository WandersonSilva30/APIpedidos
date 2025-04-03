from repositories.ProductRepository import ProductRepository

class ProductWorker():
    def __init__(self):
        self.productRepository = ProductRepository()

    def getAll(self):
        return self.productRepository.getAll()

    def create(self, productData):
        self.productRepository.create(productData)

    def details(self, id:int):
        return self.productRepository.details(id)

    def update(self, id:int, productData):
        self.productRepository.update(id, productData)

    def delete(self, id:int):
        self.productRepository.delete(id)
