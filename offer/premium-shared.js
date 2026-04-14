/* ===== 10xSEO Premium Offer System — Shared JS ===== */

// --- Analytics stub (PostHog/Plausible-ready) ---
const offerAnalytics = {
  trackSectionView(section, clientSlug) {
    console.log('[Analytics] Section view:', section, clientSlug);
  },
  trackCTAClick(ctaId, context) {
    console.log('[Analytics] CTA click:', ctaId, context);
  },
  trackPricingInteraction(tier, action) {
    console.log('[Analytics] Pricing:', tier, action);
  },
  trackShareAction(recipient) {
    console.log('[Analytics] Share:', recipient);
  },
  trackVideoProgress(videoId, progress) {
    console.log('[Analytics] Video progress:', videoId, progress + '%');
  },
  trackMAPStepToggle(stepId, newStatus) {
    console.log('[Analytics] MAP toggle:', stepId, newStatus);
  },
  trackExportPDF(clientSlug) {
    console.log('[Analytics] PDF export:', clientSlug);
  }
};

// --- Reveal on scroll ---
const premiumRevealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      // Track section view
      const sectionId = e.target.closest('section')?.id;
      if (sectionId) offerAnalytics.trackSectionView(sectionId, window.__clientSlug || '');
      premiumRevealObs.unobserve(e.target);
    }
  });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal-p').forEach(el => premiumRevealObs.observe(el));

// --- Load premium client data ---
function loadPremiumClient(callback) {
  const slug = new URLSearchParams(window.location.search).get('client') ||
               window.location.hash.replace('#','');
  if (!slug) return;
  window.__clientSlug = slug;
  fetch('offer/clients-premium.json')
    .then(r => r.json())
    .then(data => {
      const c = data[slug];
      if (c && callback) callback(c, slug);
    })
    .catch(() => {
      // Try relative path (if we're in offer/ subdirectory)
      fetch('clients-premium.json')
        .then(r => r.json())
        .then(data => {
          const c = data[slug];
          if (c && callback) callback(c, slug);
        })
        .catch(() => {});
    });
}

// --- Format number ---
function fmtNum(n) {
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// --- Format currency ---
function fmtCurrency(amount, currency) {
  if (currency === 'AED') return 'AED ' + fmtNum(amount);
  if (currency === 'USD') return '$' + fmtNum(amount);
  return fmtNum(amount) + ' ₾';
}

// --- Scroll spy for deal room nav ---
function initScrollSpy() {
  const navItems = document.querySelectorAll('.deal-nav-item');
  const sections = [];
  navItems.forEach(item => {
    const targetId = item.getAttribute('href')?.replace('#', '');
    if (targetId) {
      const section = document.getElementById(targetId);
      if (section) sections.push({ el: section, nav: item });
    }
  });
  if (!sections.length) return;

  function updateActive() {
    const scrollY = window.scrollY + 120;
    let active = sections[0];
    for (const s of sections) {
      if (s.el.offsetTop <= scrollY) active = s;
    }
    navItems.forEach(n => n.classList.remove('active'));
    active.nav.classList.add('active');
  }
  window.addEventListener('scroll', updateActive, { passive: true });
  updateActive();
}

// --- Smooth scroll to section ---
function scrollToSection(sectionId) {
  const el = document.getElementById(sectionId);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    offerAnalytics.trackCTAClick('nav-scroll', sectionId);
  }
}

// --- MAP interactivity ---
function initMAP() {
  document.querySelectorAll('.map-check').forEach(check => {
    check.addEventListener('click', function() {
      const wasChecked = this.classList.contains('checked');
      this.classList.toggle('checked');
      const stepId = this.dataset.step;
      const newStatus = wasChecked ? 'pending' : 'done';
      offerAnalytics.trackMAPStepToggle(stepId, newStatus);
      updateMAPProgress();
    });
  });
}

function updateMAPProgress() {
  const total = document.querySelectorAll('.map-check').length;
  const done = document.querySelectorAll('.map-check.checked').length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  const bar = document.getElementById('map-progress-fill');
  const label = document.getElementById('map-progress-label');
  if (bar) bar.style.width = pct + '%';
  if (label) label.textContent = pct + '% complete (' + done + '/' + total + ')';
}

// --- FAQ toggle (premium) ---
function togglePFaq(el) {
  el.closest('.pfaq-item').classList.toggle('open');
}

// --- Share to stakeholder modal ---
function openShareModal() {
  document.getElementById('share-modal')?.classList.add('open');
  offerAnalytics.trackCTAClick('share-modal-open', '');
}
function closeShareModal() {
  document.getElementById('share-modal')?.classList.remove('open');
}
function sendShareEmail() {
  const name = document.getElementById('share-name')?.value || '';
  const email = document.getElementById('share-email')?.value || '';
  const msg = document.getElementById('share-message')?.value || '';
  if (!email) { alert('Please enter an email address'); return; }
  // In production, this would POST to an API
  const subject = encodeURIComponent('SEO Proposal for Review — 10xSEO');
  const body = encodeURIComponent(msg || 'Please review the attached SEO proposal from 10xSEO.\n\nLink: ' + window.location.href);
  window.open('mailto:' + email + '?subject=' + subject + '&body=' + body);
  offerAnalytics.trackShareAction(email);
  closeShareModal();
}

// --- PDF export (print) ---
function exportPDF() {
  offerAnalytics.trackExportPDF(window.__clientSlug || '');
  window.print();
}

// --- Counter animation ---
function animatePremiumCounters() {
  document.querySelectorAll('.p-counter').forEach(el => {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';
    const isDecimal = el.dataset.decimal === 'true';
    let current = 0;
    const increment = target / 35;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = prefix + (isDecimal ? current.toFixed(1) : fmtNum(Math.floor(current))) + suffix;
    }, 30);
  });
}

// Counter observer
const counterObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      animatePremiumCounters();
      counterObs.unobserve(e.target);
    }
  });
}, { threshold: 0.2 });

// --- Calendly integration ---
function openCalendly() {
  if (window.Calendly) {
    Calendly.initPopupWidget({ url: 'https://calendly.com/10xseo/strategy-call' });
  }
  offerAnalytics.trackCTAClick('calendly', 'schedule-call');
}

// --- Pricing tier select ---
function selectTier(tierId) {
  document.querySelectorAll('.pricing-tier').forEach(t => {
    t.classList.remove('selected');
    t.style.borderColor = '';
  });
  const selected = document.querySelector('[data-tier="' + tierId + '"]');
  if (selected) {
    selected.classList.add('selected');
    selected.style.borderColor = 'var(--accent)';
  }
  offerAnalytics.trackPricingInteraction(tierId, 'select');
}

// --- Video chapter click ---
function jumpToChapter(sectionId, time) {
  scrollToSection(sectionId);
  // If Loom/video player supports time seeking, do it here
  offerAnalytics.trackCTAClick('chapter-jump', sectionId + '@' + time);
}

// --- Approval action ---
function approveProposal() {
  const slug = window.__clientSlug || '';
  offerAnalytics.trackCTAClick('approve-proposal', slug);
  // In production: POST to API
  alert('Thank you! Your approval has been recorded. Our team will follow up within 24 hours.');
}

function requestRevision() {
  const comment = document.getElementById('revision-comment')?.value || '';
  if (!comment) { alert('Please add your feedback'); return; }
  offerAnalytics.trackCTAClick('request-revision', window.__clientSlug || '');
  alert('Thank you for your feedback. We\'ll address your comments and update the proposal.');
}

// --- Init on DOM ready ---
document.addEventListener('DOMContentLoaded', () => {
  // Re-observe reveals (for dynamically added content)
  document.querySelectorAll('.reveal-p:not(.visible)').forEach(el => premiumRevealObs.observe(el));

  // Init scroll spy if deal room nav exists
  if (document.querySelector('.deal-nav')) initScrollSpy();

  // Init MAP if present
  if (document.querySelector('.map-check')) initMAP();

  // Init counter observer
  const counterSection = document.querySelector('.p-counter');
  if (counterSection) counterObs.observe(counterSection.closest('section') || counterSection);
});
