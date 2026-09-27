/* Exam / practice runner. State lives in RUN (from the server) and is saved with small POSTs after each change. */
(function () {
  'use strict';
  var R = window.RUN, items = R.items, cur = 0, enter = Date.now(), elim = false, hlOn = false, finishing = false;
  var $ = function (id) { return document.getElementById(id); };
  var LETTERS = ['A', 'B', 'C', 'D'];
  var hl = {}; // saved highlighted HTML of the left pane, per item

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function typeset(el) {
    if (window.renderMathInElement) renderMathInElement(el, {delimiters: [{left: '\\(', right: '\\)', display: false}, {left: '\\[', right: '\\]', display: true}], throwOnError: false});
  }

  /* ---------- figures */
  function figure(f) {
    if (!f || f.type !== 'scatter') return '';
    var W = 380, H = 270, L = 42, B = 34, T = 12, Rr = 14, pw = W - L - Rr, ph = H - B - T;
    var sx = function (x) { return L + (x - f.xmin) / (f.xmax - f.xmin) * pw; };
    var sy = function (y) { return T + ph - (y - f.ymin) / (f.ymax - f.ymin) * ph; };
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" style="max-width:420px;font-family:sans-serif" role="img" aria-label="Scatterplot with line of best fit">';
    for (var x = f.xmin; x <= f.xmax; x += f.xstep) {
      s += '<line x1="' + sx(x) + '" x2="' + sx(x) + '" y1="' + T + '" y2="' + (T + ph) + '" stroke="#DDE2E8"/>';
      s += '<text x="' + sx(x) + '" y="' + (H - B + 14) + '" font-size="10" text-anchor="middle">' + x + '</text>';
    }
    for (var y = f.ymin; y <= f.ymax; y += f.ystep) {
      s += '<line x1="' + L + '" x2="' + (L + pw) + '" y1="' + sy(y) + '" y2="' + sy(y) + '" stroke="#DDE2E8"/>';
      s += '<text x="' + (L - 6) + '" y="' + (sy(y) + 3) + '" font-size="10" text-anchor="end">' + y + '</text>';
    }
    s += '<rect x="' + L + '" y="' + T + '" width="' + pw + '" height="' + ph + '" fill="none" stroke="#18212E" stroke-width="1.5"/>';
    if (f.line) s += '<line x1="' + sx(f.line[0][0]) + '" y1="' + sy(f.line[0][1]) + '" x2="' + sx(f.line[1][0]) + '" y2="' + sy(f.line[1][1]) + '" stroke="#1F4FA3" stroke-width="2"/>';
    f.points.forEach(function (p) { s += '<circle cx="' + sx(p[0]) + '" cy="' + sy(p[1]) + '" r="3.6" fill="#18212E"/>'; });
    s += '<text x="' + (L + pw / 2) + '" y="' + (H - 4) + '" font-size="11" text-anchor="middle">' + (f.xlabel || 'x') + '</text>';
    s += '<text x="11" y="' + (T + ph / 2) + '" font-size="11" text-anchor="middle" transform="rotate(-90 11 ' + (T + ph / 2) + ')">' + (f.ylabel || 'y') + '</text></svg>';
    return '<div style="margin:.8rem 0">' + s + '</div>';
  }

  /* ---------- rendering */
  function isAnswered(it) { return it.answer !== '' && it.answer != null; }

  function render() {
    var it = items[cur], q = it.q, left = $('left'), right = $('right'), pages = $('pages');
    var rw = R.section === 'rw';
    var head = '<div class="qhead"><span class="qn">' + (cur + 1) + '</span>' +
      '<button type="button" class="flagbtn" id="flag" aria-pressed="' + it.flagged + '">' + (it.flagged ? 'Flagged for review' : 'Flag for review') + '</button>' +
      '<button type="button" class="tool' + (elim ? ' on' : '') + '" id="elim" aria-pressed="' + elim + '" title="Cross out answer choices">Cross out choices</button></div>';
    var leftHtml;
    if (hl[it.id]) leftHtml = hl[it.id];
    else if (rw) leftHtml = '<div class="passage">' + (q.passage || '') + '</div>';
    else leftHtml = '<div class="stem" style="font-weight:400">' + q.q + '</div>' + figure(q.figure);
    // Reading & Writing: passage on the left, stem + choices on the right. Math: question on the left, answer on the right.
    if (rw) {
      if (!q.passage) { pages.className = 'pages single'; left.style.display = 'none'; }
      else { pages.className = 'pages'; left.style.display = ''; }
      left.innerHTML = leftHtml;
    } else { pages.className = 'pages'; left.style.display = ''; left.innerHTML = leftHtml; }
    var body = head + (rw ? '<p class="stem">' + q.q + '</p>' : '');
    if (q.type === 'mc') {
      body += '<div class="opts' + (elim ? ' elim' : '') + '" role="radiogroup">';
      q.choices.forEach(function (c, i) {
        var L = LETTERS[i], sel = it.answer === L, struck = it.struck.indexOf(L) >= 0, cls = 'opt' + (sel ? ' sel' : '') + (struck ? ' struck' : '');
        if (it.fb) { if (L === it.fb.key) cls += ' right'; else if (sel) cls += ' wrong'; }
        body += '<button type="button" class="' + cls + '" data-l="' + L + '" role="radio" aria-checked="' + sel + '"><span class="bub">' + L + '</span><span class="txt">' + c + '</span>' +
          '<span class="x" data-x="' + L + '">' + (struck ? 'Undo' : 'Cross out') + '</span></button>';
      });
      body += '</div>';
    } else {
      body += '<div class="sprbox"><label for="spr" style="font-weight:600">Your answer</label><br><input id="spr" type="text" inputmode="text" autocomplete="off" value="' + esc(it.answer || '') + '" ' + (it.fb ? 'disabled' : '') + '>' +
        '<div class="prev" id="sprprev"></div><p class="hint">Enter a whole number, decimal, or fraction such as 3/4. Negative numbers use a minus sign.</p></div>';
    }
    if (R.feedback) {
      if (!it.fb) body += '<p><button type="button" class="btn" id="check"' + (isAnswered(it) ? '' : ' disabled') + '>Check answer</button></p>';
      else body += '<div class="feedback"><div class="verdict ' + (it.fb.correct ? 'ok' : 'no') + '">' + (it.fb.correct ? 'Correct' : 'Not quite') +
        (q.type === 'spr' && !it.fb.correct ? '. Correct answer: ' + esc(it.fb.key) : '') + '</div>' + it.fb.expl + '</div>';
    }
    right.innerHTML = body;
    typeset(left); typeset(right);
    $('qcur').textContent = cur + 1;
    $('back').disabled = cur === 0;
    $('next').textContent = cur === items.length - 1 ? 'Review' : 'Next';
    enter = Date.now();
    bind(it);
    left.scrollTop = 0; right.scrollTop = 0;
  }

  function bind(it) {
    $('flag').onclick = function () { it.flagged = !it.flagged; save(it); render(); };
    $('elim').onclick = function () { elim = !elim; render(); };
    var opts = document.querySelectorAll('.opt');
    Array.prototype.forEach.call(opts, function (b) {
      b.onclick = function (e) {
        if (it.fb) return;
        var L = b.getAttribute('data-l');
        if (e.target.closest('.x')) {
          var k = it.struck.indexOf(L);
          if (k >= 0) it.struck.splice(k, 1); else { it.struck.push(L); if (it.answer === L) it.answer = ''; }
          save(it); render(); return;
        }
        it.answer = (it.answer === L) ? '' : L;
        var k2 = it.struck.indexOf(L); if (k2 >= 0) it.struck.splice(k2, 1);
        save(it); render();
      };
    });
    var spr = $('spr');
    if (spr) {
      var prev = function () {
        var v = spr.value.trim(), out = '';
        if (v) { var n = parse(v); out = n === null ? 'Not a valid answer yet' : 'Reads as ' + n; }
        $('sprprev').textContent = out;
      };
      spr.oninput = function () { it.answer = spr.value.trim(); prev(); var c = $('check'); if (c) c.disabled = !isAnswered(it); clearTimeout(spr._t); spr._t = setTimeout(function () { save(it); }, 500); };
      spr.onblur = function () { save(it); };
      prev();
    }
    var chk = $('check');
    if (chk) chk.onclick = function () {
      var d = Date.now() - enter; enter = Date.now();
      post(R.urls.check, {item_id: it.id, answer: it.answer, time_ms: d}).then(function (j) {
        if (!j) return; it.fb = {correct: j.correct, key: j.key, expl: j.expl}; it.checked = true; render();
      });
    };
    typeset($('right'));
  }

  function parse(v) {
    v = v.replace(/,/g, '').replace(/\s/g, '');
    if (/^-?\d+\/-?\d+$/.test(v)) { var p = v.split('/'); if (+p[1] === 0) return null; return +(p[0] / p[1]).toFixed(5) * 1; }
    if (/^-?(\d+\.?\d*|\.\d+)$/.test(v)) return +v;
    return null;
  }

  /* ---------- server calls */
  function post(url, body) {
    return fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})
      .then(function (r) { if (r.status === 409) { window.location.reload(); return null; } return r.json(); }).catch(function () { return null; });
  }
  function save(it) {
    var d = Date.now() - enter; enter = Date.now();
    it.time_ms = (it.time_ms || 0) + d;
    return post(R.urls.save, {item_id: it.id, answer: it.answer, flagged: it.flagged, struck: it.struck, time_ms: d});
  }
  function goto(n) { save(items[cur]); cur = Math.max(0, Math.min(items.length - 1, n)); render(); }

  /* ---------- navigator + review */
  function stateClass(it, i) { return 'bubble ' + (isAnswered(it) ? 'done' : 'todo') + (it.flagged ? ' flag' : '') + (i === cur ? ' here' : ''); }
  function buildGrid(el, closeFn) {
    el.innerHTML = '';
    items.forEach(function (it, i) {
      var b = document.createElement('button'); b.type = 'button'; b.className = stateClass(it, i); b.textContent = i + 1;
      b.setAttribute('aria-label', 'Question ' + (i + 1) + (isAnswered(it) ? ', answered' : ', not answered') + (it.flagged ? ', flagged' : ''));
      b.onclick = function () { closeFn(); goto(i); };
      el.appendChild(b);
    });
  }
  function toggleNav(force) {
    var p = $('navpop'), open = force !== undefined ? force : p.hidden;
    if (open) {
      p.innerHTML = '<div class="legend"><span>Filled: answered</span><span>Dashed: not answered</span><span>Red corner: flagged</span></div><div class="bubblegrid" id="navgrid"></div>' +
        '<p style="margin:.8rem 0 0;text-align:right"><button type="button" class="btn ghost" id="gorev">Go to review page</button></p>';
      buildGrid($('navgrid'), function () { toggleNav(false); });
      $('gorev').onclick = function () { toggleNav(false); openReview(); };
    }
    p.hidden = !open; $('qnav').setAttribute('aria-expanded', open);
  }
  function openReview() {
    save(items[cur]);
    var un = items.filter(function (i) { return !isAnswered(i); }).length, fl = items.filter(function (i) { return i.flagged; }).length;
    $('revsum').textContent = (un ? un + ' unanswered. ' : 'Every question has an answer. ') + (fl ? fl + ' flagged for review.' : '');
    buildGrid($('revgrid'), function () { $('review').hidden = true; });
    $('review').hidden = false;
  }

  /* ---------- finish */
  function finish() {
    if (finishing) return; finishing = true;
    var chain = save(items[cur]);
    Promise.resolve(chain).then(function () { return post(R.urls.finish, {module_id: R.moduleId}); }).then(function (j) { window.location = j && j.next ? j.next : window.location.href; });
  }

  /* ---------- timer */
  var t0 = performance.now(), hidden = false;
  function tick() {
    var el = (performance.now() - t0) / 1000, txt;
    if (R.limit) {
      var left = Math.max(0, R.remaining - el);
      txt = fmt(left);
      $('timer').classList.toggle('warn', left <= R.warn);
      var w = $('warn'); if (left <= R.warn && left > 0) { w.hidden = false; w.textContent = Math.ceil(left / 60) + ' minute' + (Math.ceil(left / 60) === 1 ? '' : 's') + ' or less remaining in this module.'; } else if (left <= 0) { w.hidden = false; w.textContent = 'Time is up. Submitting your answers.'; }
      if (left <= 0) { $('clock').textContent = '0:00'; finish(); return; }
    } else txt = fmt(el);
    if (!hidden) $('clock').textContent = txt;
  }
  function fmt(s) { s = Math.floor(s); var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60; return (h ? h + ':' + ('0' + m).slice(-2) : m) + ':' + ('0' + x).slice(-2); }

  /* ---------- highlight tool */
  function saveHL() { hl[items[cur].id] = $('left').innerHTML; }
  document.addEventListener('mouseup', function (e) {
    if (!hlOn) return;
    var left = $('left'), sel = window.getSelection();
    if (e.target.tagName === 'MARK' && left.contains(e.target)) { var m = e.target, par = m.parentNode; while (m.firstChild) par.insertBefore(m.firstChild, m); par.removeChild(m); saveHL(); return; }
    if (!sel || sel.isCollapsed || !left.contains(sel.anchorNode) || !left.contains(sel.focusNode)) return;
    try {
      var rg = sel.getRangeAt(0), mk = document.createElement('mark'); mk.appendChild(rg.extractContents()); rg.insertNode(mk); sel.removeAllRanges(); saveHL();
    } catch (err) { /* selection crossed an element boundary the browser cannot wrap */ }
  });

  /* ---------- floating panels */
  function drag(panel) {
    var h = panel.querySelector('header'), sx, sy, ox, oy, on = false;
    h.addEventListener('mousedown', function (e) { on = true; sx = e.clientX; sy = e.clientY; var r = panel.getBoundingClientRect(); ox = r.left; oy = r.top; panel.style.right = 'auto'; panel.style.bottom = 'auto'; panel.style.left = ox + 'px'; panel.style.top = oy + 'px'; e.preventDefault(); });
    document.addEventListener('mousemove', function (e) { if (on) { panel.style.left = (ox + e.clientX - sx) + 'px'; panel.style.top = (oy + e.clientY - sy) + 'px'; } });
    document.addEventListener('mouseup', function () { on = false; });
  }
  var calcReady = false;
  function calcMount() {
    if (calcReady) return; calcReady = true;
    var host = $('calcbody');
    if (window.Desmos && Desmos.GraphingCalculator) {
      host.style.height = '100%';
      var c = Desmos.GraphingCalculator(host, {keypad: true, expressions: true, settingsMenu: false, zoomButtons: true, expressionsTopbar: true});
      window._desmos = c; setTimeout(function () { c.resize(); }, 50);
      new ResizeObserver(function () { c.resize(); }).observe($('calc'));
    } else if (window.BuiltinCalc) { BuiltinCalc.mount(host); }
    else host.textContent = 'Calculator did not load.';
  }
  function toggle(id, btn, on) {
    var p = $(id), open = on !== undefined ? on : p.style.display !== 'flex';
    p.style.display = open ? 'flex' : 'none'; btn.setAttribute('aria-pressed', open);
    return open;
  }

  /* ---------- wire up */
  window.addEventListener('DOMContentLoaded', function () {
    $('back').onclick = function () { goto(cur - 1); };
    $('next').onclick = function () { if (cur === items.length - 1) openReview(); else goto(cur + 1); };
    $('qnav').onclick = function () { toggleNav(); };
    $('rev-back').onclick = function () { $('review').hidden = true; };
    $('rev-submit').onclick = function () { $('review').hidden = true; finish(); };
    $('hideclock').onclick = function () { hidden = !hidden; $('clock').textContent = hidden ? '' : $('clock').textContent; $('hideclock').textContent = hidden ? 'Show' : 'Hide'; if (!hidden) tick(); };
    $('t-hl').onclick = function () { hlOn = !hlOn; $('t-hl').setAttribute('aria-pressed', hlOn); document.body.style.cursor = ''; };
    var tc = $('t-calc'), tr = $('t-ref');
    if (tc) { $('calc-x').onclick = function () { toggle('calc', tc, false); }; tc.onclick = function () { var o = toggle('calc', tc); if (o) calcMount(); }; drag($('calc')); }
    if (tr) { $('ref-x').onclick = function () { toggle('refsheet', tr, false); }; tr.onclick = function () { toggle('refsheet', tr); }; drag($('refsheet')); }
    document.addEventListener('keydown', function (e) {
      if (e.target.tagName === 'INPUT') return;
      if (e.key === 'ArrowRight') $('next').click(); else if (e.key === 'ArrowLeft' && cur > 0) $('back').click();
    });
    render(); tick(); setInterval(tick, 500);
  });
})();
