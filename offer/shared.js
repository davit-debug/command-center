/* ===== 10xSEO Offer Pages — Shared JS ===== */

// --- Reveal on scroll ---
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); } });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

// --- Sticky CTA hide/show ---
(function() {
  let lastY = 0;
  const sc = document.getElementById('sticky-cta');
  if (!sc) return;
  window.addEventListener('scroll', () => {
    const y = window.pageYOffset;
    sc.style.transform = (y > lastY && y > 300) ? 'translateY(100%)' : 'translateY(0)';
    lastY = y;
  }, { passive: true });
})();

// --- FAQ toggle ---
function toggleFaq(el) {
  el.closest('.fq-card').classList.toggle('open');
}

// --- Counter animation ---
function animateCounters() {
  document.querySelectorAll('.counter-stat').forEach(el => {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';
    const isDecimal = el.dataset.decimal === 'true';
    let current = 0;
    const increment = target / 40;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = prefix + (isDecimal ? current.toFixed(1) : Math.floor(current)) + suffix;
    }, 30);
  });
}

// --- Client personalization ---
function loadClientData(callback) {
  const slug = window.location.hash.replace('#','') || new URLSearchParams(window.location.search).get('client');
  if (!slug) return;
  fetch('offer/clients.json').then(r => r.json()).then(data => {
    const c = data[slug];
    if (c && callback) callback(c, slug);
  }).catch(() => {});
}

// --- Format number with commas ---
function fmtNum(n) {
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
