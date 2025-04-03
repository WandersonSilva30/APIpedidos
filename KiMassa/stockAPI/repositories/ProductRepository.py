from repositories.BaseRepository import BaseRepository

class ProductRepository(BaseRepository):
    
    def __init__(self):
        super().__init__()

    def getAll(self):
        query = "SELECT * FROM products"
        return self.executeQuery(query)

    def create(self, productData):
        command = "INSERT INTO products (name, cost, price) VALUES (%s, %s, %s)"
        values = (productData['name'], productData['cost'], productData['price'])
        self.execute(command, values)

    def details(self, id: int):
        query = "SELECT * FROM products WHERE id = %s"
        return self.executeQuery(query, (id,))

    def update(self, id: int, productData):
        command = """
        UPDATE products 
        SET name = %s, cost = %s, price = %s 
        WHERE id = %s
        """
        values = (productData['name'], productData['cost'], productData['price'], id)
        self.execute(command, values)

    def delete(self, id: int):
        command = "DELETE FROM products WHERE id = %s"
        self.execute(command, (id,))

