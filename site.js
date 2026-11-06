const search = document.querySelector('#book-search');
if (search) {
  document.querySelector('.search-bar').hidden = false;
  const rows = [...document.querySelectorAll('[data-book]')];
  const normalize = text => text.toLocaleLowerCase('pl').replaceAll('ł', 'l').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  search.addEventListener('input', () => {
    const query = normalize(search.value.trim());
    let count = 0;
    rows.forEach(row => { row.hidden = !normalize(row.dataset.book).includes(query); if (!row.hidden) count++; });
    document.querySelector('#book-count').textContent = `Wyniki: ${count} z ${rows.length}`;
    document.querySelector('#no-results').hidden = count !== 0;
  });
}

const menuToggle = document.querySelector('.menu-toggle');
const menu = document.querySelector('#main-menu');
if (menuToggle && menu) {
  menuToggle.hidden = false;
  document.documentElement.classList.add('has-menu-toggle');
  const closeMenu = () => { menuToggle.setAttribute('aria-expanded', 'false'); menu.classList.remove('is-open'); };
  menuToggle.addEventListener('click', () => {
    const open = menuToggle.getAttribute('aria-expanded') !== 'true';
    menuToggle.setAttribute('aria-expanded', String(open));
    menu.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.classList.contains('is-open')) { closeMenu(); menuToggle.focus(); }
  });
  menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
  matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);
}
