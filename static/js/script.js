// ========================================
// ALERTA PERSONALIZADO
// ========================================

function alertPersonalizado(mensagem) {
    // Remove alert existente
    const alertExistente = document.querySelector('.alert-overlay');
    if (alertExistente) alertExistente.remove();

    // Cria overlay do alert
    const alertOverlay = document.createElement('div');
    alertOverlay.className = 'alert-overlay';
    alertOverlay.innerHTML = `
        <div class="alert-box">
            <div class="alert-icon">💰</div>
            <div class="alert-message">${mensagem}</div>
            <button class="alert-btn">OK</button>
        </div>
    `;

    document.body.appendChild(alertOverlay);

    // Adiciona animação
    setTimeout(() => alertOverlay.classList.add('alert-show'), 10);

    // Fechar ao clicar no botão
    alertOverlay.querySelector('.alert-btn').addEventListener('click', () => {
        fecharAlert();
    });

    // Adiciona CSS se não existir
    if (!document.querySelector('#alert-style')) adicionarEstilosAlert();

    // Fecha automaticamente em 5s
    setTimeout(() => fecharAlert(), 5000);
}

function fecharAlert() {
    const alert = document.querySelector('.alert-overlay');
    if (alert) {
        alert.classList.add('alert-hide');
        setTimeout(() => alert.remove(), 300);
    }
}

function adicionarEstilosAlert() {
    const style = document.createElement('style');
    style.id = 'alert-style';
    style.textContent = `
        .alert-overlay {
            position: fixed;
            top:0; left:0;
            width:100%; height:100%;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(5px);
            display:flex; justify-content:center; align-items:center;
            z-index:10000;
            opacity:0;
            transition: all 0.3s ease;
        }
        .alert-overlay.alert-show { opacity:1; }
        .alert-overlay.alert-hide { opacity:0; transform: scale(0.9); }
        .alert-box {
            background: linear-gradient(135deg, rgba(10,10,10,0.95), rgba(26,26,26,0.95));
            border: 2px solid;
            border-image: linear-gradient(45deg,#00ffff,#ff0095,#00ff7f)1;
            border-radius:20px;
            padding:2rem;
            text-align:center;
            max-width:400px; width:90%;
            transform: scale(0.8) translateY(50px);
            transition: all 0.3s cubic-bezier(0.175,0.885,0.32,1.275);
            box-shadow: 0 25px 50px rgba(0,0,0,0.4),0 0 30px rgba(0,255,255,0.2);
        }
        .alert-show .alert-box { transform: scale(1) translateY(0); }
        .alert-icon { font-size:3rem; margin-bottom:1rem; filter: drop-shadow(0 0 15px rgba(0,255,255,0.5)); animation: alertPulse 2s ease-in-out infinite; }
        @keyframes alertPulse { 0%,100%{transform:scale(1);} 50%{transform:scale(1.1);} }
        .alert-message { color:#fff; font-size:1.2rem; font-weight:600; margin-bottom:1.5rem; line-height:1.4; background: linear-gradient(45deg,#00ffff,#ff0095); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow:0 0 20px rgba(0,255,255,0.3);}
        .alert-btn { background:linear-gradient(135deg,#00ffff,#ff0095); color:#000; border:none; padding:12px 30px; border-radius:25px; font-size:1rem; font-weight:700; cursor:pointer; transition:all 0.3s ease; text-transform:uppercase; letter-spacing:1px; min-width:100px; box-shadow:0 8px 20px rgba(0,255,255,0.3);}
        .alert-btn:hover { background:linear-gradient(135deg,#ff0095,#00ff7f); transform:translateY(-2px); box-shadow:0 12px 25px rgba(255,0,150,0.4);}
        .alert-btn:active { transform:translateY(0);}
        @media (max-width:480px){ .alert-box{padding:1.5rem; max-width:350px;} .alert-icon{font-size:2.5rem;} .alert-message{font-size:1.1rem;} .alert-btn{padding:10px 25px; font-size:0.9rem;} }
    `;
    document.head.appendChild(style);
}

// ========================================
// CONFERIR VALOR
// ========================================
function mostrarValor(nome, modelo, preco) {
    let mensagem = `${nome}`;
    if(modelo) mensagem += ` (${modelo})`;
    mensagem += ` custa R$ ${Number(preco).toFixed(2)}`;
    alertPersonalizado(mensagem);
}

// ========================================
// ADICIONAR AO CARRINHO
// ========================================
function adicionarAoCarrinho(produto, preco) {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    carrinho.push({ nome: produto, preco: Number(preco) });
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
    alertPersonalizado(produto + " adicionado ao carrinho!");
}