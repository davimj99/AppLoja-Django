/* ============================================================
   navbar.js — Busca e badge do carrinho (TechNova)
   ============================================================ */

(function () {
  const inputNavbar   = document.getElementById('busca-navbar');
  const dropdown      = document.getElementById('searchDropdown');
  const badge         = document.getElementById('carrinhoBadge');
  const todosProdutos = document.querySelectorAll('.produto');

  /* ── Helpers ── */
  function nomeProduto(el)      { return el.querySelector('h3')?.textContent || ''; }
  function imgProduto(el)       { return el.querySelector('img')?.src || ''; }
  function categoriaProduto(el) { return el.dataset.categoria || ''; }

  function slugify(str) {
    return str
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^\w-]/g, '');
  }

  function highlight(texto, termo) {
    const re = new RegExp(
      `(${termo.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi'
    );
    return texto.replace(re, '<mark>$1</mark>');
  }

  /* ── Dropdown de busca ── */
  function renderDropdown(termo) {
    dropdown.innerHTML = '';

    if (!termo) {
      dropdown.classList.remove('aberto');
      return;
    }

    const resultados = [...todosProdutos].filter(p =>
      nomeProduto(p).toLowerCase().includes(termo) ||
      categoriaProduto(p).includes(termo)
    );

    if (resultados.length === 0) {
      dropdown.innerHTML = '<div class="search-empty">Nenhum produto encontrado</div>';
      dropdown.classList.add('aberto');
      return;
    }

    resultados.slice(0, 7).forEach(p => {
      const nome = nomeProduto(p);
      const img  = imgProduto(p);
      const slug = slugify(categoriaProduto(p));

      const item = document.createElement('a');
      item.href      = '#' + slug;
      item.className = 'search-item';
      item.innerHTML = `
        ${img
          ? `<img src="${img}" alt="${nome}">`
          : '<span class="search-no-img">📦</span>'
        }
        <div class="search-info">
          <span class="search-nome">${highlight(nome, termo)}</span>
          <span class="search-cat">${categoriaProduto(p)}</span>
        </div>`;

      item.addEventListener('click', () => {
        fecharDropdown();
        /* Destaca o card encontrado */
        p.classList.add('destaque');
        setTimeout(() => p.classList.remove('destaque'), 1800);
      });

      dropdown.appendChild(item);
    });

    dropdown.classList.add('aberto');
  }

  function fecharDropdown() {
    dropdown.classList.remove('aberto');
    inputNavbar.value = '';
  }

  /* Eventos do input */
  if (inputNavbar) {
    inputNavbar.addEventListener('input', () => {
      renderDropdown(inputNavbar.value.trim().toLowerCase());
    });

    inputNavbar.addEventListener('keydown', e => {
      if (e.key === 'Escape') fecharDropdown();
    });
  }

  /* Fecha ao clicar fora */
  document.addEventListener('click', e => {
    if (!e.target.closest('.nav-search-wrap')) {
      dropdown.classList.remove('aberto');
    }
  });

  /* ── Badge do carrinho ── */
  function atualizarBadge() {
    const carrinho = JSON.parse(localStorage.getItem('carrinho') || '[]');
    const total = carrinho.reduce((soma, item) => soma + (item.qtd || 1), 0);
    if (!badge) return;
    badge.textContent    = total;
    badge.style.display  = total > 0 ? 'flex' : 'none';
  }

  atualizarBadge();

  /* Intercepta adicionarAoCarrinho para atualizar o badge automaticamente */
  const _original = window.adicionarAoCarrinho;
  window.adicionarAoCarrinho = function (nome, preco) {
    if (typeof _original === 'function') _original(nome, preco);
    atualizarBadge();
  };
})();