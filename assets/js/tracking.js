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
    GA4_ID: '',                       // e.g. 'G-XXXXXXXXXX'

    // Google Tag Manager (alternative-ი GA4-ის — თუ GTM გამოიყენებ, GA4_ID დატოვე ცარიელი)
    GTM_ID: '',                       // e.g. 'GTM-XXXXXXX'

    // Google Search Console — verification token (meta-ის content)
    GSC_VERIFY: '',                   // e.g. 'abc123_long_token_xyz'
    GSC_VERIFY_INJECT: false,         // true = JS-ით ჩასმა; false = ცოცხალი meta-ი ვაკეთებ ცალკე
                                       // recommended: false + html file ვერიფიკაცია

    // Hotjar — Site Settings → Tracking
    HOTJAR_ID: '',                    // e.g. '1234567' (numeric)
    HOTJAR_SV: 6,                     // Hotjar snippet version (default 6)

    // Meta (Facebook) Pixel — Events Manager → Settings → Pixel ID
    META_PIXEL_ID: '',                // e.g. '123456789012345'

    // LinkedIn Insight Tag — Campaign Manager → Insight Tag
    LINKEDIN_PARTNER_ID: '',          // e.g. '1234567'

    // TikTok Pixel
    TIKTOK_PIXEL_ID: '',              // e.g. 'CTGXXXXXXXXXXXX'

    // Microsoft Clarity (heatmaps + recordings, free alternative to Hotjar)
    CLARITY_ID: '',                   // e.g. 'abc12dxyz'

    // Yandex Metrica (CIS market relevance)
    YANDEX_METRICA_ID: '',            // e.g. '12345678' (numeric)

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
  // 2) Google Analytics 4
  // ============================================================
  if (CONFIG.GA4_ID) {
    loadScript('https://www.googletagmanager.com/gtag/js?id=' + CONFIG.GA4_ID);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', CONFIG.GA4_ID, { anonymize_ip: true });
    log('GA4 loaded:', CONFIG.GA4_ID);
  }

  // ============================================================
  // 3) Google Tag Manager (alternative to GA4 above)
  // ============================================================
  if (CONFIG.GTM_ID) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    loadScript('https://www.googletagmanager.com/gtm.js?id=' + CONFIG.GTM_ID);
    log('GTM loaded:', CONFIG.GTM_ID);
  }

  // ============================================================
  // 4) Hotjar
  // ============================================================
  if (CONFIG.HOTJAR_ID) {
    (function (h, o, t, j) {
      h.hj = h.hj || function () { (h.hj.q = h.hj.q || []).push(arguments); };
      h._hjSettings = { hjid: CONFIG.HOTJAR_ID, hjsv: CONFIG.HOTJAR_SV };
      var a = o.getElementsByTagName('head')[0];
      var r = o.createElement('script');
      r.async = 1;
      r.src = t + h._hjSettings.hjid + j + h._hjSettings.hjsv;
      a.appendChild(r);
    })(window, document, 'https://static.hotjar.com/c/hotjar-', '.js?sv=');
    log('Hotjar loaded:', CONFIG.HOTJAR_ID);
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
  // Public helper: გადახდის/CTA-ის event tracking
  // გამოყენება: window.trackEvent('book_consultation', { source: 'header' })
  // ============================================================
  window.trackEvent = function (eventName, params) {
    params = params || {};
    if (typeof window.gtag === 'function') window.gtag('event', eventName, params);
    if (typeof window.fbq === 'function') window.fbq('trackCustom', eventName, params);
    if (typeof window.lintrk === 'function') window.lintrk('track', { conversion_id: params.linkedin_conversion_id });
    if (window.ttq && typeof window.ttq.track === 'function') window.ttq.track(eventName, params);
    log('event:', eventName, params);
  };

  log('tracking.js initialized');
})();
