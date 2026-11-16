/* Better To Best Research Hub: shared behaviour (S41). Theme choice, mobile menu, mark note. */
(function () {
  var root = document.documentElement;
  var KEY = 'btb-theme';
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* private window: ignore */ } }
  var saved = stored();
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);

  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var tt = document.getElementById('themeToggle');
    function paint() {
      if (!tt) return;
      var dark = isDark();
      tt.textContent = dark ? 'Light' : 'Dark';
      tt.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    }
    if (tt) {
      tt.addEventListener('click', function () {
        var next = isDark() ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        save(next);
        paint();
      });
      paint();
    }

    var nt = document.getElementById('navToggle');
    var nav = document.getElementById('site-nav');
    if (nt && nav) {
      nt.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        nt.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    var mark = document.getElementById('btbMarkToggle');
    var note = document.getElementById('btbGeometryNote');
    if (mark && note) {
      mark.addEventListener('click', function () {
        var open = note.getAttribute('data-open') === 'true';
        note.setAttribute('data-open', open ? 'false' : 'true');
        mark.setAttribute('aria-expanded', open ? 'false' : 'true');
      });
    }
  });
})();
