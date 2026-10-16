// Mobile menu, active-section highlighting, and click-to-enlarge images.
(function () {
  var toggle = document.querySelector('.nav__toggle');
  var menu = document.getElementById('nav-links');

  toggle.addEventListener('click', function () {
    var open = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  menu.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Highlight the nav link for the part of the page currently in view.
  var links = {};
  menu.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  function setActive(activeId) {
    Object.keys(links).forEach(function (id) {
      links[id].classList.toggle('is-active', id === activeId);
    });
  }
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) setActive(entry.target.id);
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    document.querySelectorAll('.part, #contact').forEach(function (part) { observer.observe(part); });
    // The contact band is too short to reach mid-screen, so mark it at the bottom of the page.
    window.addEventListener('scroll', function () {
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) setActive('contact');
    }, { passive: true });
  }

  // Click-to-enlarge for images marked data-zoom.
  var dialog = document.querySelector('.lightbox');
  if (!dialog || !dialog.showModal) return;
  var big = dialog.querySelector('img');
  document.querySelectorAll('img[data-zoom]').forEach(function (img) {
    img.addEventListener('click', function () {
      big.src = img.currentSrc || img.src;
      big.alt = img.alt;
      dialog.showModal();
    });
  });
  // Buttons that open a specific image, e.g. "Learn more" on a card.
  document.querySelectorAll('[data-zoom-for]').forEach(function (button) {
    button.addEventListener('click', function () {
      var target = document.getElementById(button.getAttribute('data-zoom-for'));
      if (target) target.click();
    });
  });
  dialog.addEventListener('click', function (e) {
    if (e.target !== big) dialog.close();
  });
})();
