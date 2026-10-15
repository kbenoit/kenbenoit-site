// Filtering, sorting, hash sync and BibTeX export for /publication/. Items are server-rendered;
// this only hides, shows and reorders them.
(function () {
  var list = document.getElementById('cite-list');
  if (!list) return;
  var items = Array.prototype.slice.call(list.querySelectorAll('.pub-item'));
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab-btn'));
  var q = document.getElementById('f-q'), area = document.getElementById('f-area'), sort = document.getElementById('f-sort');
  var years = Array.prototype.slice.call(document.querySelectorAll('input[name=year]'));
  var countEl = document.getElementById('result-count'), empty = document.getElementById('no-results');
  document.querySelector('.pub-tabs').hidden = false;
  var panel = document.querySelector('.pub-filters'), tog = document.getElementById('f-toggle');
  panel.hidden = false; tog.hidden = false;
  tog.addEventListener('click', function () {
    var open = panel.classList.toggle('open'); tog.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  function readState() {
    var s = { tab: 'all', area: '', q: '', sort: 'new', year: [] };
    location.hash.replace(/^#/, '').split('&').forEach(function (p, i) {
      if (!p) return;
      var kv = p.split('=');
      if (kv.length === 1) { if (i === 0) s.tab = decodeURIComponent(kv[0]); return; }
      var v = decodeURIComponent(kv.slice(1).join('='));
      if (kv[0] === 'year') s.year = v.split(',').filter(Boolean); else if (kv[0] in s) s[kv[0]] = v;
    });
    if (!tabs.some(function (t) { return t.dataset.tab === s.tab; })) s.tab = 'all';
    return s;
  }
  function formState() {
    return { tab: (tabs.filter(function (t) { return t.classList.contains('active'); })[0] || tabs[0]).dataset.tab,
      area: area.value, q: q.value.trim(), sort: sort.value,
      year: years.filter(function (y) { return y.checked; }).map(function (y) { return y.value; }) };
  }
  function hashOf(s) {
    var h = s.tab;
    if (s.area) h += '&area=' + encodeURIComponent(s.area);
    if (s.year.length) h += '&year=' + s.year.join(',');
    if (s.q) h += '&q=' + encodeURIComponent(s.q);
    if (s.sort !== 'new') h += '&sort=' + s.sort;
    return h;
  }
  function matches(it, s, ignoreTab) {
    if (!ignoreTab && s.tab !== 'all' && it.dataset.tab !== s.tab) return false;
    if (s.area && (' ' + it.dataset.areas + ' ').indexOf(' ' + s.area + ' ') < 0) return false;
    if (s.year.length && s.year.indexOf(it.dataset.year) < 0) return false;
    if (s.q) { var hay = it.dataset.search; if (!s.q.toLowerCase().split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; })) return false; }
    return true;
  }
  var cmp = {
    new: function (a, b) { return b.dataset.year - a.dataset.year || a.dataset.order - b.dataset.order; },
    old: function (a, b) { return a.dataset.year - b.dataset.year || b.dataset.order - a.dataset.order; },
    az: function (a, b) { return key(a).localeCompare(key(b)); },
    za: function (a, b) { return key(b).localeCompare(key(a)); }
  };
  function key(it) { return it.dataset.title.replace(/^[^A-Za-z0-9]+/, '').toLowerCase(); }

  function apply(s, setControls) {
    if (setControls) {
      area.value = s.area; sort.value = s.sort; q.value = s.q;
      years.forEach(function (y) { y.checked = s.year.indexOf(y.value) >= 0; });
    }
    tabs.forEach(function (t) {
      var on = t.dataset.tab === s.tab;
      t.classList.toggle('active', on); t.setAttribute('aria-selected', on ? 'true' : 'false');
      var n = items.filter(function (it) { return (t.dataset.tab === 'all' || it.dataset.tab === t.dataset.tab) && matches(it, s, true); }).length;
      t.querySelector('.count').textContent = n;
    });
    items.sort(cmp[s.sort] || cmp.new).forEach(function (it) { list.appendChild(it); });
    var shown = 0;
    items.forEach(function (it) { var ok = matches(it, s); it.hidden = !ok; if (ok) shown++; });
    countEl.textContent = shown + ' of ' + items.length + ' results';
    empty.hidden = shown !== 0;
  }
  function push() {
    var s = formState(), h = '#' + hashOf(s);
    if (h !== location.hash) location.hash = h; else apply(s);
  }

  tabs.forEach(function (t) { t.addEventListener('click', function () {
    tabs.forEach(function (x) { x.classList.toggle('active', x === t); }); push(); }); });
  [area, sort].forEach(function (el) { el.addEventListener('change', push); });
  years.forEach(function (y) { y.addEventListener('change', push); });
  var timer;
  q.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () { var s = formState(); history.replaceState(null, '', '#' + hashOf(s)); apply(s); }, 150);
  });
  document.getElementById('f-reset').addEventListener('click', function () {
    var tab = formState().tab; location.hash = '#' + tab; if (location.hash === '#' + tab) apply(readState(), true);
  });
  window.addEventListener('hashchange', function () { apply(readState(), true); });

  // BibTeX for the visible results
  function bibEscape(s) { return s.replace(/([&%$#_])/g, '\\$1'); }
  function bibtex(it) {
    var d = it.dataset, pub = d.pub || '', type = d.type, f = [], kind = 'misc';
    f.push(['author', d.authors], ['title', '{' + d.title + '}'], ['year', d.year]);
    if (type === 'journal_article') {
      kind = 'article';
      var m = pub.match(/^(.*?),\s*(\d+)(?:\((\w+)\))?:\s*([\d–-]+)/);
      if (m) { f.push(['journal', m[1]], ['volume', m[2]]); if (m[3]) f.push(['number', m[3]]); f.push(['pages', m[4].replace(/[–-]/, '--')]); }
      else if (pub) f.push(['journal', pub.split(',')[0]]);
    } else if (type === 'book') { kind = 'book'; if (pub) f.push(['publisher', pub]); }
    else if (type === 'book_chapter') { kind = 'incollection'; if (pub) f.push(['note', pub]); }
    else if (pub) f.push(['howpublished', pub]);
    if (d.doi) f.push(['doi', d.doi]);
    return '@' + kind + '{' + d.key + ',\n' + f.map(function (p) {
      var v = p[1]; v = p[0] === 'year' || p[0] === 'pages' ? v : bibEscape(v);
      return '  ' + p[0] + ' = {' + (p[1].charAt(0) === '{' ? v : v) + '}'; }).join(',\n') + '\n}';
  }
  document.getElementById('f-bib').addEventListener('click', function () {
    var vis = items.filter(function (it) { return !it.hidden; });
    var blob = new Blob([vis.map(bibtex).join('\n\n') + '\n'], { type: 'application/x-bibtex' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'benoit-publications.bib';
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  });

  apply(readState(), true);
})();
