/* Offline graphing calculator used when Desmos cannot load. Expressions containing x are graphed as y = f(x);
   expressions without x are evaluated. Drag to pan, scroll to zoom. Key points (intersections and intercepts) are listed. */
(function () {
  'use strict';
  var COLORS = ['#c74440', '#2d70b3', '#388c46', '#6042a6', '#000000'];

  /* ---- parser: numbers, x, pi, e, + - * / ^, functions, implicit multiplication */
  var FUNCS = {sin: Math.sin, cos: Math.cos, tan: Math.tan, asin: Math.asin, acos: Math.acos, atan: Math.atan, sqrt: Math.sqrt, abs: Math.abs,
    ln: Math.log, log: function (v) { return Math.log(v) / Math.LN10; }, exp: Math.exp};

  function tokenize(src) {
    var s = src.toLowerCase().replace(/\u03c0/g, 'pi').replace(/\u00d7/g, '*').replace(/\u00f7/g, '/').replace(/\u2212/g, '-').replace(/\s+/g, ''), out = [], i = 0, m;
    while (i < s.length) {
      var rest = s.slice(i);
      if ((m = /^(\d+\.?\d*|\.\d+)/.exec(rest))) { out.push({t: 'n', v: parseFloat(m[1])}); i += m[1].length; }
      else if ((m = /^(asin|acos|atan|sqrt|sin|cos|tan|abs|ln|log|exp|pi|x|e)/.exec(rest))) { out.push({t: 'id', v: m[1]}); i += m[1].length; }
      else if ('+-*/^()'.indexOf(s[i]) >= 0) { out.push({t: 'op', v: s[i]}); i++; }
      else throw new Error('Unexpected "' + s[i] + '"');
    }
    return out;
  }
  function compile(src) {
    var tk = tokenize(src), p = 0;
    function peek() { return tk[p]; }
    function isStart(t) { return t && (t.t === 'n' || t.t === 'id' || (t.t === 'op' && t.v === '(')); }
    function expr() { var a = term(); while (peek() && peek().t === 'op' && (peek().v === '+' || peek().v === '-')) { var op = tk[p++].v, b = term(); a = bin(op, a, b); } return a; }
    function term() {
      var a = unary();
      for (;;) {
        var t = peek();
        if (t && t.t === 'op' && (t.v === '*' || t.v === '/')) { p++; a = bin(t.v, a, unary()); }
        else if (isStart(t)) a = bin('*', a, unary());
        else break;
      }
      return a;
    }
    function unary() { var t = peek(); if (t && t.t === 'op' && t.v === '-') { p++; var u = unary(); return function (x) { return -u(x); }; } if (t && t.t === 'op' && t.v === '+') { p++; return unary(); } return power(); }
    function power() { var a = primary(), t = peek(); if (t && t.t === 'op' && t.v === '^') { p++; var b = unary(); return function (x) { return Math.pow(a(x), b(x)); }; } return a; }
    function primary() {
      var t = tk[p++];
      if (!t) throw new Error('Unfinished expression');
      if (t.t === 'n') return function () { return t.v; };
      if (t.t === 'op' && t.v === '(') { var e = expr(); if (!peek() || peek().v !== ')') throw new Error('Missing )'); p++; return e; }
      if (t.t === 'id') {
        if (t.v === 'x') return function (x) { return x; };
        if (t.v === 'pi') return function () { return Math.PI; };
        if (t.v === 'e') return function () { return Math.E; };
        var f = FUNCS[t.v];
        var arg;
        if (peek() && peek().v === '(') { p++; arg = expr(); if (!peek() || peek().v !== ')') throw new Error('Missing )'); p++; }
        else arg = power();
        return function (x) { return f(arg(x)); };
      }
      throw new Error('Unexpected "' + t.v + '"');
    }
    function bin(op, a, b) {
      return op === '+' ? function (x) { return a(x) + b(x); } : op === '-' ? function (x) { return a(x) - b(x); } : op === '*' ? function (x) { return a(x) * b(x); } : function (x) { return a(x) / b(x); };
    }
    var f = expr();
    if (p < tk.length) throw new Error('Unexpected "' + tk[p].v + '"');
    return f;
  }

  function niceStep(span) { var raw = span / 8, pow = Math.pow(10, Math.floor(Math.log10(raw))), n = raw / pow; return (n < 1.5 ? 1 : n < 3.5 ? 2 : n < 7.5 ? 5 : 10) * pow; }
  function fmtn(v) { if (Math.abs(v) < 1e-9) return '0'; var r = Math.round(v * 1000) / 1000; return String(r); }

  function mount(host) {
    host.innerHTML = '<div class="bc"><div class="rows"></div><canvas></canvas><div class="bar"><button data-a="in">Zoom in</button><button data-a="out">Zoom out</button><button data-a="reset">Reset view</button><button data-a="add">Add row</button><span class="pts"></span></div></div>';
    var rowsEl = host.querySelector('.rows'), cv = host.querySelector('canvas'), ctx = cv.getContext('2d'), pts = host.querySelector('.pts');
    var view = {x0: -10, x1: 10, y0: -7.5, y1: 7.5}, rows = [], key = [];

    function addRow(val) {
      var i = rows.length, div = document.createElement('div'); div.className = 'row';
      div.innerHTML = '<i style="background:' + COLORS[i % COLORS.length] + '"></i><input type="text" spellcheck="false" placeholder="' + (i === 0 ? 'y = 2x + 1   or   3(4+5)' : '') + '" aria-label="Expression ' + (i + 1) + '"><span class="res"></span>';
      rowsEl.appendChild(div);
      var inp = div.querySelector('input'), res = div.querySelector('.res'), r = {inp: inp, res: res, f: null, color: COLORS[i % COLORS.length]};
      inp.value = val || '';
      inp.addEventListener('input', function () { parseRow(r); draw(); });
      rows.push(r);
    }
    function parseRow(r) {
      r.f = null; r.res.textContent = ''; r.res.className = 'res';
      var t = r.inp.value.trim();
      if (!t) return;
      t = t.replace(/^y\s*=/i, '').replace(/^f\(x\)\s*=/i, '');
      try {
        var f = compile(t), usesX = /x/i.test(t.replace(/exp|max/gi, ''));
        if (usesX) r.f = f; else { var v = f(0); r.res.textContent = '= ' + (isFinite(v) ? fmtn(v) : 'undefined'); }
      } catch (e) { r.res.textContent = e.message; r.res.className = 'res err'; }
    }
    function size() { var r = cv.getBoundingClientRect(); cv.width = Math.max(50, r.width); cv.height = Math.max(50, r.height); draw(); }
    var sx = function (x) { return (x - view.x0) / (view.x1 - view.x0) * cv.width; };
    var sy = function (y) { return cv.height - (y - view.y0) / (view.y1 - view.y0) * cv.height; };
    var ix = function (px) { return view.x0 + px / cv.width * (view.x1 - view.x0); };
    var iy = function (py) { return view.y0 + (cv.height - py) / cv.height * (view.y1 - view.y0); };

    function keyPoints() {
      key = [];
      var fs = rows.filter(function (r) { return r.f; }), N = 600, a = view.x0, b = view.x1;
      function root(g, lo, hi) { var glo = g(lo); for (var k = 0; k < 40; k++) { var m = (lo + hi) / 2, gm = g(m); if ((gm < 0) === (glo < 0)) { lo = m; glo = gm; } else hi = m; } return (lo + hi) / 2; }
      function scan(g, tag, f0) {
        var px = a, pg = g(a);
        for (var i = 1; i <= N; i++) {
          var x = a + (b - a) * i / N, gx = g(x);
          if (isFinite(pg) && isFinite(gx) && pg * gx < 0 && Math.abs(pg - gx) < (view.y1 - view.y0)) { var r = root(g, px, x); key.push({x: r, y: f0(r), tag: tag}); }
          px = x; pg = gx;
        }
      }
      fs.forEach(function (r) { scan(r.f, 'x-int', function () { return 0; }); var y0 = r.f(0); if (isFinite(y0) && view.x0 < 0 && view.x1 > 0) key.push({x: 0, y: y0, tag: 'y-int'}); });
      for (var i = 0; i < fs.length; i++) for (var j = i + 1; j < fs.length; j++) (function (f1, f2) { scan(function (x) { return f1(x) - f2(x); }, 'intersection', f1); })(fs[i].f, fs[j].f);
    }
    function draw() {
      var W = cv.width, H = cv.height;
      ctx.clearRect(0, 0, W, H);
      var step = niceStep(view.x1 - view.x0), stepy = niceStep(view.y1 - view.y0);
      ctx.font = '11px sans-serif'; ctx.lineWidth = 1;
      for (var gx = Math.ceil(view.x0 / step) * step; gx <= view.x1; gx += step) { ctx.strokeStyle = Math.abs(gx) < 1e-9 ? '#18212E' : '#e2e6ea'; ctx.beginPath(); ctx.moveTo(sx(gx), 0); ctx.lineTo(sx(gx), H); ctx.stroke(); ctx.fillStyle = '#56616F'; if (Math.abs(gx) > 1e-9) ctx.fillText(fmtn(gx), sx(gx) + 2, Math.min(H - 3, Math.max(11, sy(0) + 12))); }
      for (var gy = Math.ceil(view.y0 / stepy) * stepy; gy <= view.y1; gy += stepy) { ctx.strokeStyle = Math.abs(gy) < 1e-9 ? '#18212E' : '#e2e6ea'; ctx.beginPath(); ctx.moveTo(0, sy(gy)); ctx.lineTo(W, sy(gy)); ctx.stroke(); ctx.fillStyle = '#56616F'; if (Math.abs(gy) > 1e-9) ctx.fillText(fmtn(gy), Math.min(W - 30, Math.max(2, sx(0) + 4)), sy(gy) - 2); }
      rows.forEach(function (r) {
        if (!r.f) return;
        ctx.strokeStyle = r.color; ctx.lineWidth = 2.2; ctx.beginPath();
        var started = false, prevY = null;
        for (var px = 0; px <= W; px += 1) {
          var y = r.f(ix(px));
          if (!isFinite(y) || (prevY !== null && Math.abs(sy(y) - sy(prevY)) > H * 3)) { started = false; prevY = isFinite(y) ? y : null; continue; }
          if (!started) { ctx.moveTo(px, sy(y)); started = true; } else ctx.lineTo(px, sy(y));
          prevY = y;
        }
        ctx.stroke();
      });
      keyPoints();
      key.forEach(function (k) { ctx.fillStyle = '#18212E'; ctx.beginPath(); ctx.arc(sx(k.x), sy(k.y), 4, 0, 6.3); ctx.fill(); });
      var inter = key.filter(function (k) { return k.tag === 'intersection'; }).slice(0, 4).map(function (k) { return '(' + fmtn(k.x) + ', ' + fmtn(k.y) + ')'; });
      var xs = key.filter(function (k) { return k.tag === 'x-int'; }).slice(0, 4).map(function (k) { return fmtn(k.x); });
      pts.textContent = (inter.length ? 'Intersections: ' + inter.join('  ') + '   ' : '') + (xs.length ? 'x-intercepts: ' + xs.join(', ') : '');
    }
    // pan / zoom
    var drag = null;
    cv.addEventListener('pointerdown', function (e) { drag = {x: e.clientX, y: e.clientY, v: {x0: view.x0, x1: view.x1, y0: view.y0, y1: view.y1}}; cv.setPointerCapture(e.pointerId); cv.style.cursor = 'grabbing'; });
    cv.addEventListener('pointermove', function (e) {
      if (!drag) { var r = cv.getBoundingClientRect(), px = e.clientX - r.left, py = e.clientY - r.top, hit = null; key.forEach(function (k) { if (Math.abs(sx(k.x) - px) < 8 && Math.abs(sy(k.y) - py) < 8) hit = k; }); cv.title = hit ? hit.tag + ' (' + fmtn(hit.x) + ', ' + fmtn(hit.y) + ')' : ''; return; }
      var dx = (e.clientX - drag.x) / cv.width * (drag.v.x1 - drag.v.x0), dy = (e.clientY - drag.y) / cv.height * (drag.v.y1 - drag.v.y0);
      view = {x0: drag.v.x0 - dx, x1: drag.v.x1 - dx, y0: drag.v.y0 + dy, y1: drag.v.y1 + dy}; draw();
    });
    cv.addEventListener('pointerup', function () { drag = null; cv.style.cursor = 'grab'; });
    function zoom(f, cx, cy) { view = {x0: cx - (cx - view.x0) * f, x1: cx + (view.x1 - cx) * f, y0: cy - (cy - view.y0) * f, y1: cy + (view.y1 - cy) * f}; draw(); }
    cv.addEventListener('wheel', function (e) { e.preventDefault(); var r = cv.getBoundingClientRect(); zoom(e.deltaY > 0 ? 1.15 : 0.87, ix(e.clientX - r.left), iy(e.clientY - r.top)); }, {passive: false});
    host.querySelector('.bar').addEventListener('click', function (e) {
      var a = e.target.getAttribute('data-a'); if (!a) return;
      var cx = (view.x0 + view.x1) / 2, cy = (view.y0 + view.y1) / 2;
      if (a === 'in') zoom(0.7, cx, cy); else if (a === 'out') zoom(1.4, cx, cy); else if (a === 'reset') { view = {x0: -10, x1: 10, y0: -7.5 * cv.height / 300 * 0 - 7.5, y1: 7.5}; draw(); } else if (a === 'add') addRow('');
    });
    addRow(''); addRow(''); addRow('');
    new ResizeObserver(size).observe(cv); size();
  }
  window.BuiltinCalc = {mount: mount};
})();
