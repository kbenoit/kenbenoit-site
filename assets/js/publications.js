// Tabs, topic pills, search, expandable abstracts, hash sync and BibTeX export for /publication/.
// Every entry is server-rendered; this only hides, shows and wires up controls.
(function () {
  var list = document.getElementById('cite-list');
  if (!list) return;
  var items = Array.prototype.slice.call(list.querySelectorAll('.pub-item'));
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab-btn'));
  var pills = Array.prototype.slice.call(document.querySelectorAll('.pill'));
  var q = document.getElementById('f-q');
  var countEl = document.getElementById('result-count'), empty = document.getElementById('no-results');
  ['.pub-tabs', '.pills', '.pub-toolbar'].forEach(function (s) { document.querySelector(s).hidden = false; });

  // Expandable abstracts: the text is in the page; hide it and reveal the button once JS runs.
  items.forEach(function (it) {
    var btn = it.querySelector('[data-abs]'), panel = it.querySelector('[data-abs-panel]');
    if (!btn || !panel) return;
    btn.hidden = false; panel.hidden = true;
    btn.addEventListener('click', function () {
      var open = panel.hidden; panel.hidden = !open; btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  function readState() {
    var s = { tab: 'all', area: '', q: '' };
    location.hash.replace(/^#/, '').split('&').forEach(function (p, i) {
      if (!p) return;
      var kv = p.split('=');
      if (kv.length === 1) { if (i === 0) s.tab = decodeURIComponent(kv[0]); return; }
      if (kv[0] === 'area' || kv[0] === 'q') s[kv[0]] = decodeURIComponent(kv.slice(1).join('='));
    });
    if (!tabs.some(function (t) { return t.dataset.tab === s.tab; })) s.tab = 'all';
    if (!pills.some(function (p) { return p.dataset.area === s.area; })) s.area = '';
    return s;
  }
  function formState() {
    return { tab: tabs.filter(function (t) { return t.classList.contains('active'); })[0].dataset.tab,
      area: pills.filter(function (p) { return p.classList.contains('active'); })[0].dataset.area, q: q.value.trim() };
  }
  function hashOf(s) {
    var h = s.tab;
    if (s.area) h += '&area=' + encodeURIComponent(s.area);
    if (s.q) h += '&q=' + encodeURIComponent(s.q);
    return h;
  }
  function match(it, s, skip) {
    if (skip !== 'tab' && s.tab !== 'all' && it.dataset.tab !== s.tab) return false;
    if (skip !== 'area' && s.area && (' ' + it.dataset.areas + ' ').indexOf(' ' + s.area + ' ') < 0) return false;
    if (s.q) { var hay = it.dataset.search; if (!s.q.toLowerCase().split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; })) return false; }
    return true;
  }
  function apply(s, setControls) {
    if (setControls) q.value = s.q;
    tabs.forEach(function (t) {
      var on = t.dataset.tab === s.tab;
      t.classList.toggle('active', on); t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.querySelector('.count').textContent = items.filter(function (it) {
        return (t.dataset.tab === 'all' || it.dataset.tab === t.dataset.tab) && match(it, s, 'tab'); }).length;
    });
    pills.forEach(function (p) {
      var on = p.dataset.area === s.area;
      p.classList.toggle('active', on); p.setAttribute('aria-pressed', on ? 'true' : 'false');
      p.querySelector('.count').textContent = items.filter(function (it) {
        return (!p.dataset.area || (' ' + it.dataset.areas + ' ').indexOf(' ' + p.dataset.area + ' ') >= 0) && match(it, s, 'area'); }).length;
    });
    var shown = 0;
    items.forEach(function (it) { var ok = match(it, s); it.hidden = !ok; if (ok) shown++; });
    countEl.textContent = shown + ' of ' + items.length + ' results';
    empty.hidden = shown !== 0;
  }
  function push(s) { var h = '#' + hashOf(s); if (h !== location.hash) location.hash = h; else apply(s); }

  tabs.forEach(function (t) { t.addEventListener('click', function () {
    var s = formState(); s.tab = t.dataset.tab; push(s); }); });
  pills.forEach(function (p) { p.addEventListener('click', function () {
    var s = formState(); s.area = p.dataset.area; push(s); }); });
  var timer;
  q.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () { var s = formState(); history.replaceState(null, '', '#' + hashOf(s)); apply(s); }, 150);
  });
  window.addEventListener('hashchange', function () { apply(readState(), true); });

  // BibTeX for the visible results
  function esc(s) { return s.replace(/([&%$#_])/g, '\\$1'); }
  function bibtex(it) {
    var d = it.dataset, pub = d.pub || '', f = [['author', d.authors], ['title', '{' + d.title + '}'], ['year', d.year]], kind = 'misc';
    if (d.type === 'journal_article') {
      kind = 'article';
      f.push(['journal', d.venue || pub.split(',')[0]]);
      var m = pub.match(/(\d+)(?:\((\w+)[^)]*\))?:\s*([\w.]+[–-][\w.]+|\w+)\s*$/);
      if (m) { f.push(['volume', m[1]]); if (m[2]) f.push(['number', m[2]]); f.push(['pages', m[3].replace(/[–-]/, '--')]); }
    } else if (d.type === 'book') { kind = 'book'; if (pub) f.push(['publisher', pub]); }
    else if (d.type === 'book_chapter') { kind = 'incollection'; if (pub) f.push(['note', pub]); }
    else if (pub) f.push(['howpublished', pub]);
    if (d.doi) f.push(['doi', d.doi]);
    return '@' + kind + '{' + d.key + ',\n' + f.map(function (p) {
      return '  ' + p[0] + ' = {' + (p[0] === 'year' || p[0] === 'pages' ? p[1] : esc(p[1])) + '}'; }).join(',\n') + '\n}';
  }
  document.getElementById('f-bib').addEventListener('click', function () {
    var vis = items.filter(function (it) { return !it.hidden; });
    var blob = new Blob([vis.map(bibtex).join('\n\n') + '\n'], { type: 'application/x-bibtex' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'benoit-publications.bib';
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  });

  apply(readState(), true);
})();
