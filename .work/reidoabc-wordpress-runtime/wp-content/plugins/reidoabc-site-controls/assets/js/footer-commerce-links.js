(function () {
  function onReady(callback) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', callback, { once: true });
      return;
    }
    callback();
  }

  function normalize(text) {
    return (text || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  }

  onReady(function () {
    if (!window.reiDoABCCommerceLinks || !window.reiDoABCCommerceLinks.html) {
      return;
    }

    if (document.querySelector('.reidoabc-commerce-links')) {
      return;
    }

    var headings = Array.prototype.slice.call(document.querySelectorAll('h1,h2,h3,h4,h5,h6'));
    var socialHeading = headings.find(function (heading) {
      return normalize(heading.textContent) === 'redes sociais';
    });

    if (!socialHeading) {
      return;
    }

    var container = socialHeading.closest('.wp-block-group, .widget, .footer-col, div') || socialHeading.parentElement;
    if (!container) {
      return;
    }

    container.insertAdjacentHTML('afterend', window.reiDoABCCommerceLinks.html);
  });
})();
