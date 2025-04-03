from flask import Flask, request, jsonify
from repositories.BaseRepository import BaseRepository
from repositories.ProductRepository import ProductRepository
import pandas as pd
from twilio.rest import Client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = BaseRepository()
productRepo = ProductRepository()

# Configuração do Twilio
ACCOUNT_SID = "SEU_ACCOUNT_SID"
AUTH_TOKEN = "SEU_AUTH_TOKEN"
TWILIO_NUMBER = "SEU_NUMERO_TWILIO"
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Preços dos produtos
PRECOS = {
    "M": 16.00,
    "G": 18.00,
    "Quadrada": 21.00
}

# Caminho do arquivo Excel
EXCEL_FILE = "pedidos.xlsx"

def salvar_pedido_excel(nome, telefone, tamanho, quantidade, pagamento):
    """Salva o pedido em um arquivo Excel."""
    valor = PRECOS.get(tamanho, 0) * quantidade
    novo_pedido = pd.DataFrame([{ 
        "Nome": nome, 
        "Telefone": telefone, 
        "Tamanho": tamanho, 
        "Quantidade": quantidade, 
        "Valor": valor,
        "Pagamento": pagamento
    }])
    
    try:
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, novo_pedido], ignore_index=True)
    except FileNotFoundError:
        df = novo_pedido
    
    df.to_excel(EXCEL_FILE, index=False)

def salvar_pedido_banco(nome, telefone, tamanho, quantidade, pagamento):
    """Salva o pedido no banco de dados."""
    valor = PRECOS.get(tamanho, 0) * quantidade
    productRepo.create({"name": f"{nome} ({pagamento})", "cost": 0, "price": valor})

def enviar_mensagem_whatsapp(telefone, mensagem):
    """Envia mensagem de confirmação pelo WhatsApp via Twilio."""
    try:
        message = client.messages.create(
            from_=f"whatsapp:{TWILIO_NUMBER}",
            body=mensagem,
            to=f"whatsapp:{telefone}"
        )
        return message.sid
    except Exception as e:
        print(f"Erro ao enviar mensagem via WhatsApp: {str(e)}")
        return None

@app.route("/pedido", methods=["POST"])
def receber_pedido():
    """Recebe um pedido e o processa."""
    try:
        data = request.json
        nome = data.get("nome")
        telefone = data.get("telefone")
        tamanho = data.get("tamanho")
        quantidade = data.get("quantidade", 1)
        pagamento = data.get("pagamento")

        # Validação de entrada
        if not nome or not telefone or tamanho not in PRECOS or not isinstance(quantidade, int) or quantidade <= 0:
            return jsonify({"erro": "Dados inválidos. Verifique nome, telefone, tamanho e quantidade."}), 400
        
        if pagamento not in ["Pix", "Dinheiro"]:
            return jsonify({"erro": "Forma de pagamento inválida. Escolha entre 'Pix' ou 'Dinheiro'."}), 400

        # Salva pedido no Excel e no banco de dados
        salvar_pedido_excel(nome, telefone, tamanho, quantidade, pagamento)
        salvar_pedido_banco(nome, telefone, tamanho, quantidade, pagamento)

        # Envia mensagem de confirmação
        mensagem = f"Olá {nome}, seu pedido de {quantidade}x {tamanho} foi recebido! O valor total é R${PRECOS[tamanho] * quantidade:.2f}. Forma de pagamento: {pagamento}. Obrigado!"
        mensagem_id = enviar_mensagem_whatsapp(telefone, mensagem)

        # Retorna resposta
        response = {"mensagem": "Pedido recebido e confirmado via WhatsApp"}
        if mensagem_id:
            response["whatsapp_id"] = mensagem_id
        else:
            response["aviso"] = "Não foi possível enviar a mensagem de confirmação."

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)

