/**
 * 10xSEO — Centralized Tracking Loader
 * --------------------------------------------------------------------
 * ID-ები ჩასვი ქვემოთ. ცარიელი ID = pixel-ი არ ჩაიტვირთება (zero overhead).
 * ყველა pixel იტვირთება DOMContentLoaded-ის შემდეგ defer-ით.
 *
 * Page-ებში ერთი ხაზი head-ის ბოლოში ან body-ის ბოლოში:
 *   <script src="/assets/js/tracking.js" defer></script>
 *
 * ⚠ GSC verification — მე-2 ვარიანტი:
 *   - ან ცოცხალი meta tag-ით (`<meta name="google-site-verification" ...>`)
 *     ამ ფაილში ცვლადი GSC_VERIFY_INJECT=true თუ გინდა JS-ით ჩასმა
 *   - ან HTML file-ით (Search Console-დან გადმოწერი `google[hash].html` და root-ში დადე)
 *   - ჯობია HTML file მეთოდი — guaranteed working
 * --------------------------------------------------------------------
 */
(function () {
  'use strict';

  // ============================================================
  // CONFIG — ID-ები აქ ჩასვი
  // ============================================================
  var CONFIG = {
    // Google Analytics 4 — Property → Admin → Data Streams → Web → Measurement ID
    GA4_ID: 'G-XX9YG8BD37',           // reused from WP property (historical continuity)

    // Google Tag Manager (alternative-ი GA4-ის — თუ GTM გამოიყენებ, GA4_ID დატოვე ცარიელი)
    GTM_ID: '',                       // e.g. 'GTM-XXXXXXX'

    // Google Search Console — verification token (meta-ის content)
    GSC_VERIFY: '',                   // e.g. 'abc123_long_token_xyz'
    GSC_VERIFY_INJECT: false,         // true = JS-ით ჩასმა; false = ცოცხალი meta-ი ვაკეთებ ცალკე
                                       // recommended: false + html file ვერიფიკაცია

    // Hotjar — Site Settings → Tracking
    HOTJAR_ID: '3838380',             // reused from WP
    HOTJAR_SV: 6,                     // Hotjar snippet version (default 6)

    // Meta (Facebook) Pixel — Events Manager → Settings → Pixel ID
    META_PIXEL_ID: '',                // user will provide new Pixel ID (old: 838083750969721 deprecated)

    // LinkedIn Insight Tag — Campaign Manager → Insight Tag
    LINKEDIN_PARTNER_ID: '',          // e.g. '1234567'

    // TikTok Pixel
    TIKTOK_PIXEL_ID: '',              // e.g. 'CTGXXXXXXXXXXXX'

    // Microsoft Clarity (heatmaps + recordings, free alternative to Hotjar)
    CLARITY_ID: '',                   // e.g. 'abc12dxyz'

    // Yandex Metrica (CIS market relevance)
    YANDEX_METRICA_ID: '',            // e.g. '12345678' (numeric)

    // Ahrefs Web Analytics — Project Settings → Web Analytics → Tracking Code → data-key
    AHREFS_WA_KEY: 'tRsC3vlcBKyqqXh/8oI2sQ',  // 10xseo.ge project (id 9845495)

    // Behavior flags
    RESPECT_DNT: false,               // true = Do-Not-Track header-ის მქონე user-ებზე არ ჩაიტვირთოს
    DEBUG: false                      // true = console.log-ი დიაგნოსტიკისთვის
  };

  // ============================================================
  // Helpers
  // ============================================================
  var log = function () {
    if (CONFIG.DEBUG && typeof console !== 'undefined') {
      console.log.apply(console, ['[tracking.js]'].concat(Array.prototype.slice.call(arguments)));
    }
  };

  var loadScript = function (src, attrs) {
    var s = document.createElement('script');
    s.async = true;
    s.src = src;
    if (attrs) {
      for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) s.setAttribute(k, attrs[k]);
    }
    var first = document.getElementsByTagName('script')[0];
    if (first && first.parentNode) {
      first.parentNode.insertBefore(s, first);
    } else {
      (document.head || document.documentElement).appendChild(s);
    }
    return s;
  };

  // Defer heavy 3rd-party network loads past LCP window
  // (window.load + 3s — events fired earlier go into stub queues and flush on load)
  var DEFER_LOAD_MS = 3000;
  var _scheduleDeferredLoad = function (fn) {
    var run = function () { setTimeout(fn, DEFER_LOAD_MS); };
    if (document.readyState === 'complete') {
      run();
    } else {
      window.addEventListener('load', run, { once: true });
    }
  };

  // DNT respect
  if (CONFIG.RESPECT_DNT && (navigator.doNotTrack === '1' || window.doNotTrack === '1')) {
    log('DNT enabled — skipping all tracking');
    return;
  }

  // ============================================================
  // 1) Google Search Console (meta tag injection — optional)
  // ============================================================
  if (CONFIG.GSC_VERIFY && CONFIG.GSC_VERIFY_INJECT) {
    var m = document.createElement('meta');
    m.setAttribute('name', 'google-site-verification');
    m.setAttribute('content', CONFIG.GSC_VERIFY);
    document.head.appendChild(m);
    log('GSC verification meta injected');
  }

  // ============================================================
  // 2) Google Analytics 4 — stub sync, network load deferred past LCP
  // ============================================================
  if (CONFIG.GA4_ID) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', CONFIG.GA4_ID, { anonymize_ip: true });
    _scheduleDeferredLoad(function () {
      loadScript('https://www.googletagmanager.com/gtag/js?id=' + CONFIG.GA4_ID);
      log('GA4 script loaded (deferred):', CONFIG.GA4_ID);
    });
  }

  // ============================================================
  // 3) Google Tag Manager (alternative to GA4 above) — also deferred
  // ============================================================
  if (CONFIG.GTM_ID) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    _scheduleDeferredLoad(function () {
      loadScript('https://www.googletagmanager.com/gtm.js?id=' + CONFIG.GTM_ID);
      log('GTM script loaded (deferred):', CONFIG.GTM_ID);
    });
  }

  // ============================================================
  // 4) Hotjar — stub sync, network load deferred past LCP
  // ============================================================
  if (CONFIG.HOTJAR_ID) {
    window.hj = window.hj || function () { (window.hj.q = window.hj.q || []).push(arguments); };
    window._hjSettings = { hjid: CONFIG.HOTJAR_ID, hjsv: CONFIG.HOTJAR_SV };
    _scheduleDeferredLoad(function () {
      var r = document.createElement('script');
      r.async = 1;
      r.src = 'https://static.hotjar.com/c/hotjar-' + window._hjSettings.hjid + '.js?sv=' + window._hjSettings.hjsv;
      (document.getElementsByTagName('head')[0] || document.documentElement).appendChild(r);
      log('Hotjar script loaded (deferred):', CONFIG.HOTJAR_ID);
    });
  }

  // ============================================================
  // 5) Meta (Facebook) Pixel
  // ============================================================
  if (CONFIG.META_PIXEL_ID) {
    !(function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = !0;
      n.version = '2.0';
      n.queue = [];
      t = b.createElement(e);
      t.async = !0;
      t.src = v;
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', CONFIG.META_PIXEL_ID);
    window.fbq('track', 'PageView');
    log('Meta Pixel loaded:', CONFIG.META_PIXEL_ID);
  }

  // ============================================================
  // 6) LinkedIn Insight Tag
  // ============================================================
  if (CONFIG.LINKEDIN_PARTNER_ID) {
    window._linkedin_partner_id = CONFIG.LINKEDIN_PARTNER_ID;
    window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
    window._linkedin_data_partner_ids.push(CONFIG.LINKEDIN_PARTNER_ID);
    (function (l) {
      if (!l) {
        window.lintrk = function (a, b) { window.lintrk.q.push([a, b]); };
        window.lintrk.q = [];
      }
      loadScript('https://snap.licdn.com/li.lms-analytics/insight.min.js');
    })(window.lintrk);
    log('LinkedIn Insight loaded:', CONFIG.LINKEDIN_PARTNER_ID);
  }

  // ============================================================
  // 7) TikTok Pixel
  // ============================================================
  if (CONFIG.TIKTOK_PIXEL_ID) {
    !(function (w, d, t) {
      w.TiktokAnalyticsObject = t;
      var ttq = (w[t] = w[t] || []);
      ttq.methods = ['page', 'track', 'identify', 'instances', 'debug', 'on', 'off', 'once', 'ready', 'alias', 'group', 'enableCookie', 'disableCookie'];
      ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; };
      for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
      ttq.instance = function (t) { for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]); return e; };
      ttq.load = function (e, n) {
        var i = 'https://analytics.tiktok.com/i18n/pixel/events.js';
        ttq._i = ttq._i || {};
        ttq._i[e] = [];
        ttq._i[e]._u = i;
        ttq._t = ttq._t || {};
        ttq._t[e] = +new Date();
        ttq._o = ttq._o || {};
        ttq._o[e] = n || {};
        var o = document.createElement('script');
        o.type = 'text/javascript';
        o.async = !0;
        o.src = i + '?sdkid=' + e + '&lib=' + t;
        var a = document.getElementsByTagName('script')[0];
        a.parentNode.insertBefore(o, a);
      };
      ttq.load(CONFIG.TIKTOK_PIXEL_ID);
      ttq.page();
    })(window, document, 'ttq');
    log('TikTok Pixel loaded:', CONFIG.TIKTOK_PIXEL_ID);
  }

  // ============================================================
  // 8) Microsoft Clarity
  // ============================================================
  if (CONFIG.CLARITY_ID) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r);
      t.async = 1;
      t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0];
      y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CONFIG.CLARITY_ID);
    log('Clarity loaded:', CONFIG.CLARITY_ID);
  }

  // ============================================================
  // 9) Yandex Metrica
  // ============================================================
  if (CONFIG.YANDEX_METRICA_ID) {
    (function (m, e, t, r, i, k, a) {
      m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
      m[i].l = 1 * new Date();
      for (var j = 0; j < document.scripts.length; j++) {
        if (document.scripts[j].src === r) return;
      }
      k = e.createElement(t);
      a = e.getElementsByTagName(t)[0];
      k.async = 1;
      k.src = r;
      a.parentNode.insertBefore(k, a);
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
    window.ym(CONFIG.YANDEX_METRICA_ID, 'init', {
      clickmap: true,
      trackLinks: true,
      accurateTrackBounce: true,
      webvisor: true
    });
    log('Yandex Metrica loaded:', CONFIG.YANDEX_METRICA_ID);
  }

  // ============================================================
  // 10) Ahrefs Web Analytics — async, deferred past LCP like the rest
  // ============================================================
  if (CONFIG.AHREFS_WA_KEY) {
    _scheduleDeferredLoad(function () {
      loadScript('https://analytics.ahrefs.com/analytics.js', { 'data-key': CONFIG.AHREFS_WA_KEY });
      log('Ahrefs WA loaded (deferred):', CONFIG.AHREFS_WA_KEY);
    });
  }

  // ============================================================
  // 11) UTM Capture + Attribution (last-touch, 30-day TTL)
  // ============================================================
  var ATTRIB_KEY = '_10x_attrib';
  var ATTRIB_TTL_MS = 30 * 24 * 60 * 60 * 1000; // 30 days
  var EXPLICIT_PARAMS = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content',
                        'gclid','fbclid','msclkid','li_fat_id','ttclid'];
  var SEARCH_ENGINE_HOSTS = /(^|\.)(google|bing|yahoo|duckduckgo|yandex|baidu|ecosia|qwant|brave)\./i;

  function _readStorage(key) {
    try { return JSON.parse(localStorage.getItem(key) || 'null'); } catch (_) { return null; }
  }
  function _writeStorage(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch (_) {}
  }

  function _captureExplicit() {
    var qs = new URLSearchParams(location.search);
    var found = {};
    var hasAny = false;
    EXPLICIT_PARAMS.forEach(function (p) {
      var v = qs.get(p);
      if (v) { found[p] = v; hasAny = true; }
    });
    if (!hasAny) return null;
    found.captured_at = Date.now();
    found.landing_page = location.pathname + location.search;
    found.referrer = document.referrer || '';
    return found;
  }

  function _deriveSynthetic() {
    var ref = document.referrer;
    if (!ref) return { source: 'direct', medium: '(none)', captured_at: Date.now() };
    try {
      var host = new URL(ref).hostname;
      var isSelf = host === location.hostname || host.endsWith('.' + location.hostname);
      if (isSelf) return null; // internal navigation — don't overwrite session attribution
      var isSearch = SEARCH_ENGINE_HOSTS.test(host);
      return {
        source: host.replace(/^www\./, ''),
        medium: isSearch ? 'organic' : 'referral',
        captured_at: Date.now()
      };
    } catch (_) {
      return { source: 'direct', medium: '(none)', captured_at: Date.now() };
    }
  }

  // Run capture on init
  var _activeAttribution = (function () {
    var explicit = _captureExplicit();
    if (explicit) {
      _writeStorage(ATTRIB_KEY, explicit);
      log('attribution captured (explicit):', explicit);
      return explicit;
    }
    var stored = _readStorage(ATTRIB_KEY);
    if (stored && stored.captured_at && (Date.now() - stored.captured_at) < ATTRIB_TTL_MS) {
      log('attribution preserved (stored):', stored);
      return stored;
    }
    if (stored) {
      try { localStorage.removeItem(ATTRIB_KEY); } catch (_) {} // expired
    }
    var synthetic = _deriveSynthetic();
    if (synthetic) log('attribution synthetic:', synthetic);
    return synthetic;
  })();

  window.getAttribution = function () { return _activeAttribution; };

  // Flatten attribution for event payload (prefixed to avoid clobbering event params)
  function _attributionParams() {
    var a = _activeAttribution || {};
    return {
      attrib_source: a.utm_source || a.source || '',
      attrib_medium: a.utm_medium || a.medium || '',
      attrib_campaign: a.utm_campaign || '',
      attrib_content: a.utm_content || '',
      attrib_term: a.utm_term || '',
      attrib_landing_page: a.landing_page || '',
      attrib_gclid: a.gclid || '',
      attrib_fbclid: a.fbclid || '',
      page_language: location.pathname.indexOf('/en/') === 0 ? 'en' : 'ka'
    };
  }

  // ============================================================
  // 11) Click-context resolver — find nearest data-cta + <section id>
  // ============================================================
  function _resolveClickContext(el) {
    var ctx = { cta_location: '', section: '', text: '' };
    if (!el || !el.closest) return ctx;
    var ctaEl = el.closest('[data-cta]');
    if (ctaEl) ctx.cta_location = ctaEl.getAttribute('data-cta');
    var sectionEl = el.closest('section[id], header, footer, main, nav, aside');
    if (sectionEl) ctx.section = sectionEl.id || sectionEl.tagName.toLowerCase();
    var btn = el.closest('a, button');
    if (btn) ctx.text = (btn.innerText || btn.textContent || '').trim().substring(0, 40);
    if (!ctx.cta_location) {
      ctx.cta_location = ctx.section ? (ctx.section + '-cta') : 'unknown';
    }
    return ctx;
  }

  // Track the last clicked element that triggers a Calendly open
  // (since inline `onclick="openCalendly()"` doesn't expose the event)
  var _lastCalendlyTrigger = null;
  document.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('[onclick*="openCalendly"], [data-calendly]') : null;
    if (t) _lastCalendlyTrigger = t;
  }, true);

  // ============================================================
  // Public helper: გადახდის/CTA-ის event tracking
  // გამოყენება: window.trackEvent('book_consultation', { source: 'header' })
  // Attribution params auto-merged into every event.
  // ============================================================
  window.trackEvent = function (eventName, params) {
    params = params || {};
    var attrib = _attributionParams();
    var merged = {};
    for (var k in attrib) if (Object.prototype.hasOwnProperty.call(attrib, k)) merged[k] = attrib[k];
    for (var k2 in params) if (Object.prototype.hasOwnProperty.call(params, k2)) merged[k2] = params[k2];
    if (typeof window.gtag === 'function') window.gtag('event', eventName, merged);
    if (typeof window.fbq === 'function') window.fbq('trackCustom', eventName, merged);
    if (typeof window.lintrk === 'function') window.lintrk('track', { conversion_id: merged.linkedin_conversion_id });
    if (window.ttq && typeof window.ttq.track === 'function') window.ttq.track(eventName, merged);
    log('event:', eventName, merged);
  };

  // ============================================================
  // 12) Calendly wrapper — inject UTM params + fire book_consultation_click
  // Wraps the inline `openCalendly()` defined on every page.
  // ============================================================
  (function wrapCalendly() {
    var IS_EN = location.pathname.indexOf('/en/') !== -1 || /\/en$/.test(location.pathname);
    var CAL_URL = IS_EN
      ? 'https://calendly.com/10xseo-sales/quick-seo-consultation-15-minutes'
      : 'https://calendly.com/10xseo-sales/30-seo-clone';
    var STYLE = 'background_color=0f172a&text_color=f8fafc&primary_color=8b5cf6';

    function build(ctx) {
      var a = _activeAttribution || {};
      var params = new URLSearchParams();
      params.set('utm_source', a.utm_source || a.source || 'direct');
      params.set('utm_medium', a.utm_medium || a.medium || '(none)');
      params.set('utm_campaign', a.utm_campaign || 'site_cta');
      params.set('utm_content', (ctx.cta_location || 'unknown') + '|' + (ctx.section || 'no-section'));
      params.set('utm_term', location.pathname);
      return CAL_URL + '?' + params.toString() + '&' + STYLE;
    }

    function attemptWrap() {
      if (typeof window.openCalendly !== 'function') return false;
      if (window.openCalendly._10xWrapped) return true;
      var orig = window.openCalendly;
      window.openCalendly = function () {
        var ctx = _resolveClickContext(_lastCalendlyTrigger);
        var url = build(ctx);
        window.trackEvent('book_consultation_click', {
          cta_location: ctx.cta_location,
          page_section: ctx.section,
          page_path: location.pathname,
          button_text: ctx.text
        });
        if (typeof window.Calendly !== 'undefined' && window._calendlyReady) {
          window.Calendly.initPopupWidget({ url: url });
        } else {
          window.open(url, '_blank');
        }
        return false;
      };
      window.openCalendly._10xWrapped = true;
      log('openCalendly wrapped');
      return true;
    }

    if (!attemptWrap()) {
      // Inline openCalendly may not have parsed yet when we run; try after DOMContentLoaded
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', attemptWrap, { once: true });
      } else {
        setTimeout(attemptWrap, 0);
      }
    }
  })();

  // ============================================================
  // 13) Event taxonomy — delegated listeners (capture phase)
  // ============================================================
  (function wireEvents() {
    var DOWNLOAD_EXT_RE = /\.(pdf|zip|xlsx?|docx?|csv|pptx?|rar|7z|dmg|exe)(\?|#|$)/i;
    var INTERNAL_HOSTS = ['10xseo.ge', 'www.10xseo.ge', location.hostname];
    var CALENDLY_HOSTS = ['calendly.com', 'assets.calendly.com'];

    function isInternalHost(h) {
      for (var i = 0; i < INTERNAL_HOSTS.length; i++) if (INTERNAL_HOSTS[i] === h) return true;
      return false;
    }
    function isCalendlyHost(h) {
      for (var i = 0; i < CALENDLY_HOSTS.length; i++) if (CALENDLY_HOSTS[i] === h) return true;
      return false;
    }

    // ----- click handler: phone, email, outbound, file_download -----
    document.addEventListener('click', function (e) {
      var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      var href = a.getAttribute('href') || '';
      if (!href || href.charAt(0) === '#') return;
      var ctx = _resolveClickContext(a);

      if (/^tel:/i.test(href)) {
        window.trackEvent('phone_click', {
          phone_number: href.replace(/^tel:/i, '').trim(),
          page_section: ctx.section, page_path: location.pathname
        });
        return;
      }
      if (/^mailto:/i.test(href)) {
        window.trackEvent('email_click', {
          email_target: href.replace(/^mailto:/i, '').split('?')[0],
          page_section: ctx.section, page_path: location.pathname
        });
        return;
      }
      if (/^https?:\/\//i.test(href)) {
        var host = '';
        try { host = new URL(href).hostname; } catch (_) {}
        if (!host) return;
        if (isCalendlyHost(host)) return; // Calendly handled by wrapCalendly
        if (DOWNLOAD_EXT_RE.test(href)) {
          var ext = (href.match(DOWNLOAD_EXT_RE) || [])[1] || '';
          window.trackEvent('file_download', {
            file_name: href.split('/').pop().split('?')[0],
            file_extension: ext.toLowerCase(),
            link_url: href, page_section: ctx.section
          });
          return;
        }
        if (!isInternalHost(host)) {
          window.trackEvent('outbound_click', {
            link_url: href, link_domain: host,
            link_text: ctx.text, page_section: ctx.section
          });
        }
      }
    }, true);

    // ----- form_start (focusin one-shot per form) + form_submit -----
    var _formsStarted = new WeakSet();
    document.addEventListener('focusin', function (e) {
      var form = e.target && e.target.closest ? e.target.closest('form') : null;
      if (!form || _formsStarted.has(form)) return;
      _formsStarted.add(form);
      window.trackEvent('form_start', {
        form_id: form.id || form.getAttribute('name') || 'unnamed',
        page_path: location.pathname
      });
    }, true);

    document.addEventListener('submit', function (e) {
      var form = e.target;
      if (!form || form.tagName !== 'FORM') return;
      window.trackEvent('form_submit', {
        form_id: form.id || form.getAttribute('name') || 'unnamed',
        page_path: location.pathname
      });
    }, true);

    // ----- scroll depth: fire once at 25/50/75/100% -----
    var SCROLL_THRESHOLDS = [25, 50, 75, 100];
    var _scrollFired = {};
    var _scrollTimer = null;
    function checkScroll() {
      var doc = document.documentElement;
      var scrollTop = window.pageYOffset || doc.scrollTop || 0;
      var viewportH = window.innerHeight || doc.clientHeight;
      var docH = Math.max(doc.scrollHeight, doc.offsetHeight, document.body.scrollHeight, document.body.offsetHeight);
      var scrollable = docH - viewportH;
      if (scrollable <= 0) return;
      var pct = Math.min(100, Math.round(((scrollTop + viewportH) / docH) * 100));
      for (var i = 0; i < SCROLL_THRESHOLDS.length; i++) {
        var t = SCROLL_THRESHOLDS[i];
        if (pct >= t && !_scrollFired[t]) {
          _scrollFired[t] = true;
          window.trackEvent('scroll', { percent_scrolled: t });
        }
      }
    }
    window.addEventListener('scroll', function () {
      if (_scrollTimer) return;
      _scrollTimer = setTimeout(function () { _scrollTimer = null; checkScroll(); }, 250);
    }, { passive: true });

    // ----- video_play / video_complete (lite-yt-embed + <video>) -----
    document.addEventListener('play', function (e) {
      var el = e.target;
      if (!el) return;
      var tag = el.tagName;
      if (tag === 'VIDEO') {
        window.trackEvent('video_play', {
          video_url: el.currentSrc || el.src || 'inline',
          video_title: el.getAttribute('title') || el.getAttribute('aria-label') || ''
        });
      }
    }, true);

    // lite-yt-embed dispatches no native 'play' on the wrapper; listen for iframe creation
    document.addEventListener('click', function (e) {
      var lyt = e.target && e.target.closest ? e.target.closest('lite-youtube') : null;
      if (!lyt || lyt._10xVideoFired) return;
      lyt._10xVideoFired = true;
      window.trackEvent('video_play', {
        video_url: 'https://youtube.com/watch?v=' + (lyt.getAttribute('videoid') || ''),
        video_title: lyt.getAttribute('videotitle') || lyt.getAttribute('aria-label') || ''
      });
    }, true);

    // ----- cta_view: fires once per CTA per page session when CTA enters viewport -----
    // Combined with book_consultation_click etc., enables per-button CR% calculation:
    //   CR% = (events with cta_location = X) / (cta_view events with cta_location = X)
    if (typeof IntersectionObserver !== 'undefined') {
      var _viewSeen = new WeakSet();
      function markView(el) {
        if (_viewSeen.has(el)) return;
        _viewSeen.add(el);
        var ctx = _resolveClickContext(el);
        if (!ctx.cta_location || ctx.cta_location === 'unknown') return;
        window.trackEvent('cta_view', {
          cta_location: ctx.cta_location,
          page_section: ctx.section,
          page_path: location.pathname,
          button_text: ctx.text
        });
      }
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
            markView(entry.target);
            io.unobserve(entry.target);
          }
        });
      }, { threshold: [0.5] });
      function observeCtas() {
        var seen = new Set();
        // Explicit data-cta annotations (preferred)
        document.querySelectorAll('[data-cta]').forEach(function (el) {
          if (seen.has(el)) return; seen.add(el); io.observe(el);
        });
        // Calendly-trigger elements without data-cta (DOM-traversal fallback applies)
        document.querySelectorAll('[onclick*="openCalendly"], [data-calendly]').forEach(function (el) {
          if (seen.has(el)) return; seen.add(el); io.observe(el);
        });
        // Phone & email anchors (these are CTAs too)
        document.querySelectorAll('a[href^="tel:"], a[href^="mailto:"]').forEach(function (el) {
          if (seen.has(el)) return; seen.add(el); io.observe(el);
        });
      }
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', observeCtas, { once: true });
      } else {
        observeCtas();
      }
    }

    log('event listeners wired');
  })();

  log('tracking.js initialized');
})();
