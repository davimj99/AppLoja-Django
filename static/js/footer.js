/* ============================================================
   footer.js — Revela o footer ao chegar no final da página
   ============================================================ */

(function () {
  const footer = document.getElementById('siteFooter');
  if (!footer) return;

  function checarScroll() {
    // distância do topo + altura da janela >= altura total da página (com margem de 10px)
    const chegouAoFinal =
      window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 10;

    if (chegouAoFinal) {
      footer.classList.add('visivel');
    } else {
      footer.classList.remove('visivel');
    }
  }

  window.addEventListener('scroll', checarScroll, { passive: true });
  checarScroll(); // checar ao carregar caso a página já seja curta
})();