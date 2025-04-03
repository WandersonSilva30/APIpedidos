const API_URL = "http://127.0.0.1:5000";

async function placeOrder() {
    const nomeInput = document.getElementById('clientName');
    const telefoneInput = document.getElementById('clientPhone');
    const tamanhoInput = document.getElementById('productSize');
    const quantidadeInput = document.getElementById('productQuantity');
    const pagamentoInput = document.getElementById('paymentMethod');

    if (!nomeInput || !telefoneInput || !tamanhoInput || !quantidadeInput || !pagamentoInput) {
        console.error("Erro: Um dos elementos do formulário não foi encontrado!");
        return;
    }

    const nome = nomeInput.value;
    const telefone = telefoneInput.value;
    const tamanho = tamanhoInput.value;
    const quantidade = parseInt(quantidadeInput.value);
    const pagamento = pagamentoInput.value;

    if (!nome || !telefone || !tamanho || quantidade <= 0 || !pagamento) {
        alert("Por favor, preencha todos os campos corretamente!");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/pedido", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, telefone, tamanho, quantidade, pagamento })
    });

    const data = await response.json();
    document.getElementById('result').innerText = JSON.stringify(data);
}

