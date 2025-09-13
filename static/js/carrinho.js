// Recupera o carrinho do localStorage
let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

function atualizarCarrinho() {
    const ul = document.getElementById("itens-carrinho");
    const totalElem = document.getElementById("total");
    ul.innerHTML = "";
    let total = 0;

    carrinho.forEach((item, index) => {
        ul.innerHTML += `
            <li>
                ${item.nome} - R$${item.preco.toFixed(2)} 
                <button onclick="removerDoCarrinho(${index})">❌</button>
            </li>`;
        total += item.preco;
    });

    totalElem.textContent = `Total: R$${total.toFixed(2)}`;
}

// Função para remover um item
function removerDoCarrinho(index) {
    carrinho.splice(index, 1);
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
    atualizarCarrinho();
}

// Finalizar compra (apenas alerta por enquanto)
document.getElementById("finalizar-compra").onclick = () => {
    if(carrinho.length === 0) {
        Swal.fire({
            icon: 'warning',
            title: 'Carrinho vazio!',
            text: 'Adicione produtos antes de finalizar a compra.'
        });
        return;
    }

    Swal.fire({
        icon: 'success',
        title: 'Compra finalizada!',
        text: 'Total: R$' + carrinho.reduce((a,b) => a + b.preco, 0).toFixed(2)
    });

    carrinho = [];
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
    atualizarCarrinho();
};

// Atualiza a lista quando carrega a página
atualizarCarrinho();

// Atualiza itens do carrinho e total
function atualizarCarrinho() {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    const ulItens = document.getElementById('itens-carrinho');
    const totalElem = document.getElementById('total');

    ulItens.innerHTML = '';
    let total = 0;

    carrinho.forEach(item => {
        ulItens.innerHTML += `<li>${item.nome} - R$${Number(item.preco).toFixed(2)}</li>`;
        total += Number(item.preco);
    });

    totalElem.textContent = `Total: R$${total.toFixed(2)}`;
    atualizarResumoCarrinho();
}

// Atualiza menu lateral
function atualizarResumoCarrinho() {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    const resumoUl = document.getElementById('resumo-itens');
    const resumoTotal = document.getElementById('resumo-total');

    resumoUl.innerHTML = '';
    let total = 0;

    carrinho.forEach(item => {
        resumoUl.innerHTML += `<li>${item.nome} - R$${Number(item.preco).toFixed(2)}</li>`;
        total += Number(item.preco);
    });

    resumoTotal.textContent = `Total: R$${total.toFixed(2)}`;
}

// Finalizar compra
document.getElementById('finalizar-compra').addEventListener('click', () => {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    if(carrinho.length === 0){
        alert("Seu carrinho está vazio!");
        return;
    }
    alert("Compra finalizada! Total: R$" + carrinho.reduce((a,b) => a + Number(b.preco), 0).toFixed(2));
    localStorage.setItem('carrinho', JSON.stringify([]));
    atualizarCarrinho();
});

// Atualiza tudo ao carregar
document.addEventListener('DOMContentLoaded', atualizarCarrinho);