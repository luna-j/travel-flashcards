(() => {
  const storageKey = 'language-flashcards-decks-v1';
  const $ = id => document.getElementById(id);
  let decks = [], archived = new Set(), toastTimer;
  function toast(message) { $('toast').textContent = message; $('toast').classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => $('toast').classList.remove('show'), 1800); }
  function setArchived(id, value) {
    const next = new Set(archived);
    value ? next.add(id) : next.delete(id);
    try { localStorage.setItem(storageKey, JSON.stringify({archived: [...next]})); }
    catch { toast('无法保存收纳状态，请检查浏览器存储设置。'); return; }
    archived = next;
    render();
    if (value) { $('shelfSummary').focus(); }
    else { document.querySelector(`[data-deck-id="${id}"] .deck-link`)?.focus(); }
    toast(value ? '已收纳，学习进度保留' : '已恢复到正在复习');
  }
  function element(tag, className, text) { const el = document.createElement(tag); if (className) el.className = className; if (text) el.textContent = text; return el; }
  function action(deck, restore) { const b = element('button', 'shelve-button', restore ? '恢复复习' : '收纳'); b.type = 'button'; b.setAttribute('aria-label', `${restore ? '恢复复习' : '收纳'}：${deck.title}`); b.onclick = () => setArchived(deck.id, !restore); return b; }
  function render() {
    $('activeDecks').replaceChildren(); $('archivedDecks').replaceChildren();
    for (const deck of decks) {
      if (archived.has(deck.id)) {
        const row = element('div', 'shelf-item'); const a = element('a', '', deck.title); a.href = deck.href; row.append(a, action(deck, true)); $('archivedDecks').append(row);
      } else {
        const card = element('article', `card ${deck.type}`); card.dataset.deckId = deck.id;
        const link = element('a', 'deck-link'); link.href = deck.href;
        link.append(element('span', 'tag', deck.tag), element('h2', '', deck.title), element('p', '', deck.description));
        const actions = element('div', 'deck-actions'); const open = element('a', 'arrow', deck.action); open.href = deck.href; open.style.textDecoration = 'none'; actions.append(open, action(deck, false)); card.append(link, actions); $('activeDecks').append(card);
      }
    }
    const count = decks.filter(d => archived.has(d.id)).length;
    $('activeCount').textContent = `${decks.length - count} 个卡组`;
    $('shelfSummary').textContent = `已收纳卡组（${count}）`;
    $('emptyActive').hidden = decks.length !== count; $('emptyShelf').hidden = count !== 0;
  }
  fetch('data/decks.json').then(r => { if (!r.ok) throw new Error('manifest'); return r.json(); }).then(data => {
    decks = data;
    try { const saved = JSON.parse(localStorage.getItem(storageKey) || '{}'); archived = new Set(Array.isArray(saved.archived) ? saved.archived.filter(id => decks.some(d => d.id === id)) : []); } catch {}
    render();
  }).catch(() => { $('activeDecks').append(element('p', 'empty', '卡组加载失败，请刷新后重试。')); });
})();
