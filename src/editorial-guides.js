/* Progressive enhancement: all 500 ordinary links remain available without JS. */
(() => {
  const root = document.querySelector('.topic-discovery');
  if (!root) return;
  const cards = [...root.querySelectorAll('[data-topic-card]')];
  const search = root.querySelector('#guide-search');
  const group = root.querySelector('#guide-group');
  const count = root.querySelector('#guide-count');
  const more = root.querySelector('#guide-more');
  const normalize = value => value.toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i');
  const index = cards.map(card => ({card, text: normalize(card.textContent), group: card.dataset.guideGroup}));
  let limit = 24;
  function update() {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    const matches = index.filter(item => (!group.value || item.group === group.value) && words.every(word => item.text.includes(word)));
    const visible = new Set(matches.slice(0, limit).map(item => item.card));
    cards.forEach(card => { card.hidden = !visible.has(card); });
    count.textContent = `${matches.length} konu ve rehber · ${visible.size} tanesi gösteriliyor`;
    root.querySelector('#guide-empty').hidden = matches.length > 0;
    more.hidden = visible.size >= matches.length;
  }
  for (const input of [search, group]) input.addEventListener('input', () => { limit = 24; update(); });
  more.addEventListener('click', () => { limit += 24; update(); });
  root.querySelector('.editorial-controls').hidden = false;
  update();
})();
