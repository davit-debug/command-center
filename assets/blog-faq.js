/* Blog FAQ accordion: one answer open at a time, like the site FAQ (v29).
   The open height is measured rather than capped, so long answers are never clipped. */
(function () {
  function init(root) {
    var cards = root.querySelectorAll('.v29-card');

    function setOpen(card, open) {
      var btn = card.querySelector('.v29-cq');
      var ans = card.querySelector('.v29-ca');
      if (open) {
        card.classList.add('v29-open');
        btn.setAttribute('aria-expanded', 'true');
        ans.style.maxHeight = ans.scrollHeight + 'px';
        return;
      }
      if (!card.classList.contains('v29-open')) return;
      // max-height may be 'none' (fully open); it needs a pixel value to animate down from.
      ans.style.maxHeight = ans.scrollHeight + 'px';
      void ans.offsetHeight;
      card.classList.remove('v29-open');
      btn.setAttribute('aria-expanded', 'false');
      ans.style.maxHeight = '0px';
    }

    Array.prototype.forEach.call(cards, function (card) {
      var ans = card.querySelector('.v29-ca');
      ans.addEventListener('transitionend', function (e) {
        if (e.propertyName === 'max-height' && card.classList.contains('v29-open')) ans.style.maxHeight = 'none';
      });
      card.querySelector('.v29-cq').addEventListener('click', function () {
        var wasOpen = card.classList.contains('v29-open');
        Array.prototype.forEach.call(cards, function (c) { setOpen(c, false); });
        if (!wasOpen) setOpen(card, true);
      });
    });

    root.classList.add('js');
  }

  function run() { Array.prototype.forEach.call(document.querySelectorAll('.blog-faq'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
