// Recupera o carrinho
let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

// Salva no localStorage
function salvarCarrinho() {
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
}

// Atualiza lista principal
function atualizarCarrinho() {

    const ulItens = document.getElementById('itens-carrinho');
    const totalElem = document.getElementById('total');

    if (!ulItens) return;

    ulItens.innerHTML = '';

    let total = 0;

    carrinho.forEach((item, index) => {

        total += Number(item.preco);

        ulItens.innerHTML += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <strong>${item.nome}</strong><br>
                    <small>R$ ${Number(item.preco).toFixed(2)}</small>
                </div>

                <button
                    class="btn btn-sm btn-danger"
                    onclick="removerDoCarrinho(${index})">
                    ❌
                </button>
            </li>
        `;
    });

    if (totalElem) {
        totalElem.textContent = `Total: R$ ${total.toFixed(2)}`;
    }

    atualizarResumoCarrinho();
}

// Atualiza resumo lateral
function atualizarResumoCarrinho() {

    const resumoUl = document.getElementById('resumo-itens');
    const resumoTotal = document.getElementById('resumo-total');

    if (!resumoUl) return;

    resumoUl.innerHTML = '';

    let total = 0;

    carrinho.forEach(item => {

        total += Number(item.preco);

        resumoUl.innerHTML += `
            <li class="list-group-item">
                ${item.nome}
                <span class="float-end">
                    R$ ${Number(item.preco).toFixed(2)}
                </span>
            </li>
        `;
    });

    if (resumoTotal) {
        resumoTotal.textContent = `R$ ${total.toFixed(2)}`;
    }
}

// Remove item
function removerDoCarrinho(index) {

    carrinho.splice(index, 1);

    salvarCarrinho();

    atualizarCarrinho();

    atualizarBadge();
}

// Atualiza badge da navbar
function atualizarBadge() {

    const badge =
        document.getElementById('carrinhoBadge');

    if (badge) {
        badge.textContent = carrinho.length;
    }
}

// Finalizar compra
function finalizarCompra() {

    if (carrinho.length === 0) {

        if (typeof Swal !== "undefined") {

            Swal.fire({
                icon: 'warning',
                title: 'Carrinho vazio',
                text: 'Adicione produtos antes de finalizar.'
            });

        } else {

            alert('Seu carrinho está vazio.');

        }

        return;
    }

    const total = carrinho
        .reduce((acc, item) => acc + Number(item.preco), 0);

    if (typeof Swal !== "undefined") {

        Swal.fire({
            icon: 'success',
            title: 'Compra finalizada!',
            text: `Total: R$ ${total.toFixed(2)}`
        });

    } else {

        alert(`Compra finalizada! Total: R$ ${total.toFixed(2)}`);

    }

    carrinho = [];

    salvarCarrinho();

    atualizarCarrinho();

    atualizarBadge();
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {

    atualizarCarrinho();

    atualizarBadge();

    const btn =
        document.getElementById('finalizar-compra');

    if (btn) {

        btn.addEventListener(
            'click',
            finalizarCompra
        );

    }

});