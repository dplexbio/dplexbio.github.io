// Highlights the figure panel that matches the step in the middle of the viewport.
document.querySelectorAll('.scrolly').forEach(function (section) {
  var steps = section.querySelectorAll('.scrolly__step');
  var frame = section.querySelector('.scrolly__frame');
  var masks = section.querySelectorAll('.scrolly__mask');
  if (!('IntersectionObserver' in window) || !frame) return;

  function activate(step) {
    var panel = step.getAttribute('data-panel');
    steps.forEach(function (s) { s.classList.toggle('is-active', s === step); });
    frame.classList.toggle('has-active', Boolean(panel));
    masks.forEach(function (m) {
      m.classList.toggle('is-active', m.getAttribute('data-panel') === panel);
    });
  }

  section.classList.add('is-enhanced');
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) activate(entry.target);
    });
  }, { rootMargin: '-45% 0px -45% 0px' });

  steps.forEach(function (step) { observer.observe(step); });
});
