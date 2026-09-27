/* Hover and keyboard tooltips for the server-drawn SVG charts. Any element with data-tip shows its text next to the
   pointer (or next to the element when focused with the keyboard). Charts stay plain SVG so they also print. */
(function () {
  'use strict';
  var tip;
  function show(text, x, y) {
    if (!tip) { tip = document.createElement('div'); tip.className = 'charttip'; tip.setAttribute('role', 'status'); document.body.appendChild(tip); }
    tip.textContent = text; tip.hidden = false;
    var w = tip.offsetWidth, h = tip.offsetHeight;
    tip.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, x + 12)) + 'px';
    tip.style.top = Math.max(8, y - h - 12) + 'px';
  }
  function hide() { if (tip) tip.hidden = true; }
  document.addEventListener('pointerover', function (e) { var t = e.target.closest && e.target.closest('[data-tip]'); if (t) show(t.getAttribute('data-tip'), e.clientX, e.clientY); });
  document.addEventListener('pointermove', function (e) { var t = e.target.closest && e.target.closest('[data-tip]'); if (t) show(t.getAttribute('data-tip'), e.clientX, e.clientY); else hide(); });
  document.addEventListener('pointerout', function (e) { if (!e.relatedTarget || !e.relatedTarget.closest || !e.relatedTarget.closest('[data-tip]')) hide(); });
  document.addEventListener('focusin', function (e) {
    var t = e.target.closest && e.target.closest('[data-tip]');
    if (!t) return hide();
    var r = t.getBoundingClientRect(); show(t.getAttribute('data-tip'), r.left + r.width / 2, r.top);
  });
  document.addEventListener('focusout', hide);
  document.addEventListener('scroll', hide, true);
})();
