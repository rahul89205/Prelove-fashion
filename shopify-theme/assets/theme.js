/* Thrice Loved – tiny progressive-enhancement script. The store works without it. */
(function () {
  // Product gallery: swap main image when a thumbnail is clicked
  document.querySelectorAll('[data-gallery]').forEach(function (gallery) {
    var main = gallery.querySelector('[data-gallery-main] img');
    var thumbs = gallery.querySelectorAll('[data-gallery-thumb]');
    if (!main) return;
    thumbs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        main.src = thumb.getAttribute('data-src');
        main.srcset = '';
        main.alt = thumb.getAttribute('data-alt') || '';
        thumbs.forEach(function (t) { t.removeAttribute('aria-current'); });
        thumb.setAttribute('aria-current', 'true');
      });
    });
  });

  // Auto-submit sort / filter forms when a control changes
  document.querySelectorAll('[data-autosubmit]').forEach(function (el) {
    el.addEventListener('change', function () {
      if (el.form) el.form.submit();
    });
  });

  // Close the mobile menu when a link is chosen
  document.querySelectorAll('.mobile-nav a').forEach(function (a) {
    a.addEventListener('click', function () {
      var d = a.closest('details');
      if (d) d.removeAttribute('open');
    });
  });

  // Close open filter dropdowns when clicking elsewhere
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.filter[open]').forEach(function (d) {
      if (!d.contains(e.target)) d.removeAttribute('open');
    });
  });
})();
