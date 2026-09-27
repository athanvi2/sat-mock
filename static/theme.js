/* Theme: Auto (follow the device), Light, or Dark. The choice is stored per device. The <head> of base.html applies it
   before first paint (no flash); this file wires the buttons and tells charts and calculators when it changes. */
(function () {
  'use strict';
  var KEY = 'theme', ORDER = ['auto', 'light', 'dark'], LABEL = {auto: 'Theme: Auto', light: 'Theme: Light', dark: 'Theme: Dark'};
  function get() { try { return localStorage.getItem(KEY) || 'auto'; } catch (e) { return 'auto'; } }
  function isDark() {
    var t = document.documentElement.getAttribute('data-theme');
    if (t) return t === 'dark';
    return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  }
  function apply(mode) {
    if (mode === 'auto') document.documentElement.removeAttribute('data-theme');
    else document.documentElement.setAttribute('data-theme', mode);
    try { if (mode === 'auto') localStorage.removeItem(KEY); else localStorage.setItem(KEY, mode); } catch (e) { /* private mode */ }
    Array.prototype.forEach.call(document.querySelectorAll('.themebtn'), function (b) {
      b.textContent = LABEL[mode]; b.setAttribute('aria-label', LABEL[mode] + '. Change theme');
    });
    document.dispatchEvent(new CustomEvent('themechange', {detail: {dark: isDark()}}));
  }
  window.Theme = {isDark: isDark};
  document.addEventListener('DOMContentLoaded', function () {
    apply(get());
    Array.prototype.forEach.call(document.querySelectorAll('.themebtn'), function (b) {
      b.addEventListener('click', function () { apply(ORDER[(ORDER.indexOf(get()) + 1) % ORDER.length]); });
    });
    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var onOS = function () { if (get() === 'auto') apply('auto'); };
      if (mq.addEventListener) mq.addEventListener('change', onOS); else if (mq.addListener) mq.addListener(onOS);
    }
  });
})();
