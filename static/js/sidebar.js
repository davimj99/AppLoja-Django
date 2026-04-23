/* ============================================================
   sidebar.js — Lógica do menu lateral (TechNova)
   ============================================================ */

(function () {
  const sidebar       = document.getElementById('sidebar');
  const toggleBtn     = document.getElementById('toggleSidebar');
  const navCats       = document.querySelectorAll('.nav-cat');
  const buscaSidebar  = document.getElementById('busca');
  const todosProdutos = document.querySelectorAll('.produto');

  /* ── Helpers ── */
  function nomeProduto(el)      { return el.querySelector('h3')?.textContent || ''; }
  function categoriaProduto(el) { return el.dataset.categoria || ''; }

  /* ── Abrir / fechar sidebar (mobile) ── */
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('aberta');
    });
  }

  /* Fecha ao clicar fora em mobile */
  document.addEventListener('click', e => {
    if (
      sidebar.classList.contains('aberta') &&
      !sidebar.contains(e.target) &&
      !toggleBtn.contains(e.target)
    ) {
      sidebar.classList.remove('aberta');
    }
  });

  /* ── Marca categoria ativa + fecha sidebar em mobile ── */
  navCats.forEach(link => {
    link.addEventListener('click', () => {
      navCats.forEach(l => l.classList.remove('ativo'));
      link.classList.add('ativo');
      sidebar.classList.remove('aberta');
    });
  });

  /* ── Busca na sidebar (filtra cards da página) ── */
  if (buscaSidebar) {
    buscaSidebar.addEventListener('input', function () {
      const termo = this.value.trim().toLowerCase();

      todosProdutos.forEach(p => {
        const visivel =
          nomeProduto(p).toLowerCase().includes(termo) ||
          categoriaProduto(p).includes(termo);
        p.style.display = visivel ? '' : 'none';
      });
    });
  }
})();