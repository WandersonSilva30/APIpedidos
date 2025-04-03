from workers.ProductWorker import ProductWorker
from flask import request, jsonify

class ProductController:
    def __init__(self):
        self.productWorker = ProductWorker()

    def getAll(self):
        """Retorna todos os produtos."""
        try:
            products = self.productWorker.getAll()
            return jsonify(products), 200
        except Exception as e:
            return jsonify({"error": f"Erro ao buscar produtos: {str(e)}"}), 500

    def create(self):
        """Cria um novo produto."""
        try:
            productData = request.get_json()
            if not productData or not all(k in productData for k in ["name", "cost", "price"]):
                return jsonify({"error": "Dados inválidos. Os campos 'name', 'cost' e 'price' são obrigatórios."}), 400
            
            self.productWorker.create(productData)
            return jsonify({"message": "Produto criado com sucesso"}), 201
        except Exception as e:
            return jsonify({"error": f"Erro ao criar produto: {str(e)}"}), 500

    def details(self, id: int):
        """Retorna detalhes de um produto pelo ID."""
        try:
            product = self.productWorker.details(id)
            if not product:
                return jsonify({"error": "Produto não encontrado"}), 404
            return jsonify(product), 200
        except Exception as e:
            return jsonify({"error": f"Erro ao buscar produto: {str(e)}"}), 500

    def update(self, id: int):
        """Atualiza um produto pelo ID."""
        try:
            productData = request.get_json()
            if not productData:
                return jsonify({"error": "Dados inválidos"}), 400
            
            updated = self.productWorker.update(id, productData)
            if not updated:
                return jsonify({"error": "Produto não encontrado"}), 404

            return jsonify({"message": "Produto atualizado com sucesso"}), 200
        except Exception as e:
            return jsonify({"error": f"Erro ao atualizar produto: {str(e)}"}), 500

    def delete(self, id: int):
        """Exclui um produto pelo ID."""
        try:
            deleted = self.productWorker.delete(id)
            if not deleted:
                return jsonify({"error": "Produto não encontrado"}), 404

            return jsonify({"message": "Produto excluído com sucesso"}), 200
        except Exception as e:
            return jsonify({"error": f"Erro ao excluir produto: {str(e)}"}), 500
