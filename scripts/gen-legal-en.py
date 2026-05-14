#!/usr/bin/env python3
"""Generate 3 English legal pages (privacy/terms/cookies) for 10xseo.ge/en/.

Uses en/contact-us.html as the structural template (header, footer, fonts,
scripts) and substitutes head meta, JSON-LD schema, and main content for
each legal page. Strips contact-form scripts, FAQ schema, and Calendly
widget that don't apply to legal pages.

Run from anywhere:
    python3 /Users/imac/SEO/command-center/scripts/gen-legal-en.py
"""
import re
from pathlib import Path

ROOT = Path('/Users/imac/SEO/command-center')
TEMPLATE = (ROOT / 'en' / 'contact-us.html').read_text(encoding='utf-8')

LAST_UPDATED_EN = "Last updated: May 13, 2026 · Effective: May 13, 2026"

# ============================================================
# CONTENT: PRIVACY POLICY (EN)
# ============================================================
PRIVACY_MAIN = """  <!-- ========== HERO ========== -->
  <section class="relative pt-24 lg:pt-32 pb-12 lg:pb-16 overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-br from-gray-50 via-white to-primary/5 dark:from-surface-dark dark:via-surface-dark dark:to-primary/5"></div>
    <div class="absolute top-20 right-0 w-[400px] h-[400px] bg-primary/5 dark:bg-primary/10 rounded-full blur-3xl"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-4 sm:px-6 text-center">
      <p class="text-xs font-semibold uppercase tracking-wider text-primary dark:text-primary-light mb-3">Legal</p>
      <h1 class="font-heading text-[28px] sm:text-[36px] lg:text-[48px] font-extrabold text-heading dark:text-heading-dark !leading-[1.15] mb-4">
        <span class="gradient-text">Privacy Policy</span>
      </h1>
      <p class="text-sm text-body dark:text-body-dark/60">__LAST_UPDATED__</p>
    </div>
  </section>

  <!-- ========== ARTICLE ========== -->
  <article class="pb-16 lg:pb-20 bg-white dark:bg-surface-dark">
    <div class="max-w-3xl mx-auto px-4 sm:px-6">
      <p class="text-base text-body dark:text-body-dark mb-8 leading-relaxed">
        This Privacy Policy describes how <strong>LLC 10ixsio.ge</strong> (Georgian legal entity: შპს 10იქსსიო.ჯი; trading as "10xSEO", "we", "us", "our") collects, uses, stores, and protects personal data of visitors and clients of <a href="https://10xseo.ge" class="text-primary dark:text-primary-light hover:underline">10xseo.ge</a>. We comply with the Georgian Law on Personal Data Protection, the EU General Data Protection Regulation (GDPR) where applicable, and applicable UAE data protection laws for visitors located in the United Arab Emirates.
      </p>

      <nav aria-label="Table of contents" class="bg-surface-alt dark:bg-surface-dark-alt border border-gray-100 dark:border-gray-800 rounded-2xl p-5 mb-10">
        <p class="text-xs font-semibold uppercase tracking-wider text-body-dark/60 mb-3">On this page</p>
        <ol class="list-decimal pl-5 text-sm text-body dark:text-body-dark space-y-1">
          <li><a href="#controller" class="hover:text-primary dark:hover:text-primary-light">Data Controller</a></li>
          <li><a href="#data-we-collect" class="hover:text-primary dark:hover:text-primary-light">Data We Collect</a></li>
          <li><a href="#legal-basis" class="hover:text-primary dark:hover:text-primary-light">Legal Basis for Processing</a></li>
          <li><a href="#retention" class="hover:text-primary dark:hover:text-primary-light">Data Retention</a></li>
          <li><a href="#processors" class="hover:text-primary dark:hover:text-primary-light">Third-Party Processors</a></li>
          <li><a href="#transfers" class="hover:text-primary dark:hover:text-primary-light">International Transfers</a></li>
          <li><a href="#your-rights" class="hover:text-primary dark:hover:text-primary-light">Your Rights</a></li>
          <li><a href="#cookies" class="hover:text-primary dark:hover:text-primary-light">Cookies</a></li>
          <li><a href="#children" class="hover:text-primary dark:hover:text-primary-light">Children's Privacy</a></li>
          <li><a href="#security" class="hover:text-primary dark:hover:text-primary-light">Security</a></li>
          <li><a href="#uae" class="hover:text-primary dark:hover:text-primary-light">UAE Residents — Additional Terms</a></li>
          <li><a href="#updates" class="hover:text-primary dark:hover:text-primary-light">Updates to this Policy</a></li>
          <li><a href="#contact" class="hover:text-primary dark:hover:text-primary-light">Contact &amp; Complaints</a></li>
        </ol>
      </nav>

      <h2 id="controller" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">1. Data Controller</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">The data controller for personal data processed via 10xseo.ge is:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-1">
        <li><strong>Legal entity:</strong> შპს 10იქსსიო.ჯი (LLC "10ixsio.ge"), registered in Georgia</li>
        <li><strong>Registered address:</strong> 8 Bakhtrioni Street, Tbilisi 0194, Georgia</li>
        <li><strong>Email:</strong> <a href="mailto:sales@10xseo.ge" class="text-primary dark:text-primary-light hover:underline">sales@10xseo.ge</a></li>
        <li><strong>Phone:</strong> <a href="tel:+995510101517" class="text-primary dark:text-primary-light hover:underline">+995 510 10 15 17</a></li>
      </ul>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">For data protection inquiries, complaints, or requests to exercise your rights, contact us at <a href="mailto:sales@10xseo.ge" class="text-primary dark:text-primary-light hover:underline">sales@10xseo.ge</a> with the subject line "Data Protection Request".</p>

      <h2 id="data-we-collect" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">2. Data We Collect</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">We collect personal data in the following categories:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>Contact data</strong> — name, email, phone, company name, message — provided voluntarily through contact forms on our website.</li>
        <li><strong>Booking data</strong> — name, email, scheduled time, meeting notes — collected when you schedule a consultation via our Calendly widget.</li>
        <li><strong>Analytics data</strong> — page views, session duration, device type, browser, approximate location (country/city level), referral source — collected via Google Analytics 4. Identifiers are pseudonymized; IP addresses are anonymized before storage.</li>
        <li><strong>Behavioral data</strong> — session recordings, mouse movements, clicks, scroll depth, heatmaps — collected via Hotjar and/or Microsoft Clarity. All form fields and personally identifiable information are masked by default; we do not capture passwords, payment card details, or sensitive personal data.</li>
        <li><strong>Server log data</strong> — IP address, user agent, request timestamps, HTTP status codes — collected automatically by our hosting provider for security, fraud prevention, and performance diagnostics.</li>
      </ul>

      <h2 id="legal-basis" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">3. Legal Basis for Processing</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">Under GDPR Article 6 and the Georgian Personal Data Protection Law, we process your data on the following legal bases:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>Consent</strong> (Art. 6(1)(a) GDPR) — for analytics cookies, behavioral tracking (Hotjar, Clarity), and marketing communications. You may withdraw consent at any time.</li>
        <li><strong>Contract performance</strong> (Art. 6(1)(b)) — when you engage us as a client; processing is necessary to deliver agreed services.</li>
        <li><strong>Legitimate interest</strong> (Art. 6(1)(f)) — for security logs, fraud prevention, and aggregate performance analysis. We balance this against your rights and freedoms.</li>
        <li><strong>Legal obligation</strong> (Art. 6(1)(c)) — for tax records, accounting, and regulatory reporting under Georgian law.</li>
      </ul>

      <h2 id="retention" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">4. Data Retention</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>Contact form submissions</strong> — 24 months from last contact, then deleted or anonymized.</li>
        <li><strong>Client engagement records</strong> — 7 years after contract end, as required by Georgian Tax Code.</li>
        <li><strong>Analytics data</strong> — 14 months (GA4 default), then automatically deleted.</li>
        <li><strong>Session recordings</strong> — 365 days, then automatically deleted by Hotjar/Clarity.</li>
        <li><strong>Server logs</strong> — 90 days for security purposes, then rotated.</li>
      </ul>

      <h2 id="processors" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">5. Third-Party Processors</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">We share data with the following processors who act on our instructions under a Data Processing Agreement:</p>
      <div class="overflow-x-auto mb-3">
        <table class="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
          <thead class="bg-surface-alt dark:bg-surface-dark-alt">
            <tr><th class="px-4 py-3 text-left font-semibold text-heading dark:text-heading-dark">Processor</th><th class="px-4 py-3 text-left font-semibold text-heading dark:text-heading-dark">Purpose</th><th class="px-4 py-3 text-left font-semibold text-heading dark:text-heading-dark">Location</th></tr>
          </thead>
          <tbody class="text-body dark:text-body-dark">
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-4 py-3">Google LLC</td><td class="px-4 py-3">Analytics (GA4)</td><td class="px-4 py-3">USA (SCCs)</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-4 py-3">Calendly LLC</td><td class="px-4 py-3">Booking scheduling</td><td class="px-4 py-3">USA (SCCs)</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-4 py-3">Hotjar Ltd</td><td class="px-4 py-3">Behavioral analytics</td><td class="px-4 py-3">Malta (EU)</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-4 py-3">Microsoft Corp</td><td class="px-4 py-3">Clarity analytics</td><td class="px-4 py-3">USA (SCCs)</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-4 py-3">Hosting provider</td><td class="px-4 py-3">Website hosting</td><td class="px-4 py-3">Georgia/EU</td></tr>
          </tbody>
        </table>
      </div>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">We do not sell your personal data to any third party.</p>

      <h2 id="transfers" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">6. International Transfers</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">Some processors are located outside Georgia and the EEA (notably in the United States). For transfers of personal data from the EEA to the US, we rely on Standard Contractual Clauses (SCCs) approved by the European Commission under GDPR Article 46, supplemented by technical and organizational safeguards. For Georgia, transfers comply with Article 41 of the Georgian Personal Data Protection Law.</p>

      <h2 id="your-rights" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">7. Your Rights</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">Subject to applicable law, you have the right to:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-1">
        <li><strong>Access</strong> the personal data we hold about you (GDPR Art. 15)</li>
        <li><strong>Rectification</strong> of inaccurate or incomplete data (Art. 16)</li>
        <li><strong>Erasure</strong> of your data ("right to be forgotten", Art. 17) — subject to legal retention obligations</li>
        <li><strong>Restriction</strong> of processing (Art. 18)</li>
        <li><strong>Data portability</strong> — receive your data in a structured, machine-readable format (Art. 20)</li>
        <li><strong>Object</strong> to processing based on legitimate interest (Art. 21)</li>
        <li><strong>Withdraw consent</strong> at any time, without affecting prior lawful processing</li>
        <li><strong>Lodge a complaint</strong> with the Personal Data Protection Service of Georgia (<a href="https://personaldata.ge" class="text-primary dark:text-primary-light hover:underline" target="_blank" rel="noopener">personaldata.ge</a>) or your local EU supervisory authority</li>
      </ul>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">To exercise any of these rights, email <a href="mailto:sales@10xseo.ge" class="text-primary dark:text-primary-light hover:underline">sales@10xseo.ge</a>. We respond within 30 days (extendable by two months for complex requests).</p>

      <h2 id="cookies" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">8. Cookies</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">We use cookies and similar technologies to operate the website, measure performance, and improve user experience. For a detailed list of cookies, their purposes, and how to manage them, see our <a href="cookies-policy.html" class="text-primary dark:text-primary-light hover:underline">Cookies Policy</a>.</p>

      <h2 id="children" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">9. Children's Privacy</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">Our services are directed at businesses and professionals; we do not knowingly collect data from individuals under 16. If you believe we hold data about a minor, contact us and we will delete it.</p>

      <h2 id="security" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">10. Security</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">We apply industry-standard technical and organizational measures: TLS 1.3 encryption in transit, access controls, regular backups, principle of least privilege, and security review of processors. No system is fully impervious; we will notify affected users and the regulator within 72 hours of becoming aware of a breach involving high risk to your rights.</p>

      <h2 id="uae" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">11. UAE Residents — Additional Terms</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">If you reside in the United Arab Emirates or your data is processed in connection with our UAE engagements:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li>For mainland UAE, processing complies with UAE Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data (PDPL).</li>
        <li>For DIFC-registered clients, processing complies with DIFC Data Protection Law No. 5 of 2020.</li>
        <li>You have rights analogous to GDPR rights above: access, correction, deletion, objection, and complaint to the UAE Data Office or the DIFC Commissioner of Data Protection.</li>
        <li>We do not transfer your data outside the UAE without ensuring an adequate level of protection per the applicable UAE law.</li>
        <li>For UAE-specific data requests, email <a href="mailto:sales@10xseo.ge" class="text-primary dark:text-primary-light hover:underline">sales@10xseo.ge</a> with the subject line "UAE Data Request".</li>
      </ul>

      <h2 id="updates" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">12. Updates to this Policy</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">We may update this Privacy Policy from time to time. Material changes will be announced on this page with an updated "Last updated" date. For substantial changes affecting your rights, we will provide notice via email (where we have your address) or a banner on the website.</p>

      <h2 id="contact" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">13. Contact &amp; Complaints</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">For any questions about this Privacy Policy or our data practices:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-8 space-y-1">
        <li>Email: <a href="mailto:sales@10xseo.ge" class="text-primary dark:text-primary-light hover:underline">sales@10xseo.ge</a></li>
        <li>Phone: <a href="tel:+995510101517" class="text-primary dark:text-primary-light hover:underline">+995 510 10 15 17</a></li>
        <li>Postal: 10xSEO Data Protection, 8 Bakhtrioni Street, Tbilisi 0194, Georgia</li>
      </ul>
      <p class="text-sm text-body-dark/60 italic">This policy does not constitute legal advice. For specific legal questions, please consult a qualified attorney.</p>
    </div>
  </article>
"""

# ============================================================
# CONTENT: TERMS OF SERVICE (EN)
# ============================================================
TERMS_MAIN = """  <!-- ========== HERO ========== -->
  <section class="relative pt-24 lg:pt-32 pb-12 lg:pb-16 overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-br from-gray-50 via-white to-primary/5 dark:from-surface-dark dark:via-surface-dark dark:to-primary/5"></div>
    <div class="absolute top-20 right-0 w-[400px] h-[400px] bg-primary/5 dark:bg-primary/10 rounded-full blur-3xl"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-4 sm:px-6 text-center">
      <p class="text-xs font-semibold uppercase tracking-wider text-primary dark:text-primary-light mb-3">Legal</p>
      <h1 class="font-heading text-[28px] sm:text-[36px] lg:text-[48px] font-extrabold text-heading dark:text-heading-dark !leading-[1.15] mb-4">
        <span class="gradient-text">Terms of Service</span>
      </h1>
      <p class="text-sm text-body dark:text-body-dark/60">__LAST_UPDATED__</p>
    </div>
  </section>

  <!-- ========== ARTICLE ========== -->
  <article class="pb-16 lg:pb-20 bg-white dark:bg-surface-dark">
    <div class="max-w-3xl mx-auto px-4 sm:px-6">
      <p class="text-base text-body dark:text-body-dark mb-8 leading-relaxed">
        These Terms of Service ("Terms") govern your use of the website <a href="https://10xseo.ge" class="text-primary dark:text-primary-light hover:underline">10xseo.ge</a> and any SEO, content marketing, copywriting, Google Ads, conversion optimization, AI search optimization, training, or consultation services ("Services") provided by <strong>LLC 10ixsio.ge</strong> (Georgian legal entity: შპს 10იქსსიო.ჯი; "10xSEO", "we", "us"). By accessing the website or engaging us, you agree to these Terms.
      </p>

      <nav aria-label="Table of contents" class="bg-surface-alt dark:bg-surface-dark-alt border border-gray-100 dark:border-gray-800 rounded-2xl p-5 mb-10">
        <p class="text-xs font-semibold uppercase tracking-wider text-body-dark/60 mb-3">On this page</p>
        <ol class="list-decimal pl-5 text-sm text-body dark:text-body-dark space-y-1">
          <li><a href="#about" class="hover:text-primary dark:hover:text-primary-light">About Us</a></li>
          <li><a href="#acceptance" class="hover:text-primary dark:hover:text-primary-light">Acceptance of Terms</a></li>
          <li><a href="#services" class="hover:text-primary dark:hover:text-primary-light">Services Provided</a></li>
          <li><a href="#engagement" class="hover:text-primary dark:hover:text-primary-light">Engagement &amp; Deliverables</a></li>
          <li><a href="#payment" class="hover:text-primary dark:hover:text-primary-light">Fees &amp; Payment</a></li>
          <li><a href="#ip" class="hover:text-primary dark:hover:text-primary-light">Intellectual Property</a></li>
          <li><a href="#confidentiality" class="hover:text-primary dark:hover:text-primary-light">Confidentiality</a></li>
          <li><a href="#warranties" class="hover:text-primary dark:hover:text-primary-light">Warranties &amp; Disclaimers</a></li>
          <li><a href="#liability" class="hover:text-primary dark:hover:text-primary-light">Limitation of Liability</a></li>
          <li><a href="#termination" class="hover:text-primary dark:hover:text-primary-light">Termination</a></li>
          <li><a href="#dispute" class="hover:text-primary dark:hover:text-primary-light">Dispute Resolution &amp; Governing Law</a></li>
          <li><a href="#uae" class="hover:text-primary dark:hover:text-primary-light">UAE Clients — Additional Terms</a></li>
          <li><a href="#general" class="hover:text-primary dark:hover:text-primary-light">General Provisions</a></li>
        </ol>
      </nav>

      <h2 id="about" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">1. About Us</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">10xSEO is the trading name of <strong>შპს 10იქსსიო.ჯი</strong> (LLC 10ixsio.ge), a limited liability company registered in Georgia, with registered offices at 8 Bakhtrioni Street, Tbilisi 0194, Georgia. We provide SEO, content, paid media, and digital growth services to businesses globally, with a focus on the Georgian, EU, and UAE markets.</p>

      <h2 id="acceptance" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">2. Acceptance of Terms</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">By using our website or signing a Service Order (Statement of Work, "SOW"), you confirm that you have read, understood, and accepted these Terms. If you do not agree, do not use the website or engage us. Individual SOWs may include additional terms; in case of conflict, the SOW prevails over these Terms for that engagement.</p>

      <h2 id="services" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">3. Services Provided</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">We provide the following Services (scope confirmed per engagement):</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-1">
        <li>SEO management, audits, technical SEO, and strategy</li>
        <li>Content marketing, SEO copywriting, and UI/UX copy</li>
        <li>Google Ads, paid media management, and conversion rate optimization (CRO)</li>
        <li>AI SEO and generative engine optimization (GEO)</li>
        <li>SEO consultation, training, and online courses</li>
        <li>Custom digital growth engagements per SOW</li>
      </ul>

      <h2 id="engagement" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">4. Engagement &amp; Deliverables</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>Scope:</strong> Each engagement is defined in a written SOW signed by both parties, specifying deliverables, milestones, timelines, and fees.</li>
        <li><strong>Client cooperation:</strong> Timely delivery depends on your timely provision of access, content, approvals, and feedback. Delays caused by client inaction may shift agreed timelines without penalty to us.</li>
        <li><strong>Revisions:</strong> Each deliverable includes up to two rounds of revisions within scope; additional revisions are billed at our standard hourly rate.</li>
        <li><strong>Acceptance:</strong> Deliverables are deemed accepted if you do not provide written objection within 7 business days of delivery.</li>
      </ul>

      <h2 id="payment" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">5. Fees &amp; Payment</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>Currency:</strong> GEL (₾) for Georgian clients, EUR (€) for EU clients, USD ($) or AED for UAE/international clients, as specified in the SOW.</li>
        <li><strong>Invoicing:</strong> Monthly in advance for retainer Services; milestone-based for fixed-fee projects.</li>
        <li><strong>Payment terms:</strong> Net 14 days from invoice date unless otherwise specified.</li>
        <li><strong>Late payment:</strong> We reserve the right to suspend Services after 14 days past due. Interest may accrue at 0.05% per day on overdue amounts.</li>
        <li><strong>Taxes:</strong> Fees are exclusive of VAT/sales tax, which is added where applicable.</li>
      </ul>

      <h2 id="ip" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">6. Intellectual Property</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>Client deliverables:</strong> Upon full payment, you own all final deliverables created specifically for you (content, reports, custom artifacts).</li>
        <li><strong>Methodology &amp; tools:</strong> We retain all rights to our methodologies, frameworks, templates, internal tools, training materials, and pre-existing IP. We grant you a non-exclusive license to use these as embedded in deliverables for your business purposes.</li>
        <li><strong>Portfolio rights:</strong> Unless prohibited in writing, we may showcase non-confidential work and metrics in our portfolio and case studies. We will mask any data you flag as confidential.</li>
        <li><strong>Third-party content:</strong> You are responsible for the legality of content, brand assets, and access credentials you provide to us.</li>
      </ul>

      <h2 id="confidentiality" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">7. Confidentiality</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">Both parties agree to treat non-public business information shared during the engagement as confidential and use it only for the purpose of performing the Services. This obligation survives termination for 3 years. Standard exceptions apply (information already public, independently developed, or required to be disclosed by law).</p>

      <h2 id="warranties" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">8. Warranties &amp; Disclaimers</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li>We warrant that Services will be performed with reasonable care and skill in accordance with industry best practices.</li>
        <li><strong>No ranking guarantees.</strong> SEO outcomes depend on factors outside our control, including search engine algorithm changes, competitor activity, your industry, and prior site history. We do not guarantee specific keyword rankings, traffic levels, conversion rates, or revenue outcomes.</li>
        <li><strong>No guarantee of inclusion.</strong> We cannot guarantee inclusion or visibility in Google AI Overviews, ChatGPT, Perplexity, or other AI search platforms, which operate on opaque proprietary criteria.</li>
        <li>Except as expressly stated, Services are provided "as is" without further warranties, express or implied.</li>
      </ul>

      <h2 id="liability" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">9. Limitation of Liability</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">To the maximum extent permitted by applicable law:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li>Our aggregate liability under any engagement is capped at the total fees paid by you to us in the 12 months preceding the event giving rise to the claim.</li>
        <li>We are not liable for indirect, incidental, consequential, special, or punitive damages, including lost profits, lost revenue, lost data, or business interruption.</li>
        <li>Nothing in these Terms excludes liability for gross negligence, willful misconduct, or matters that cannot be excluded under applicable law.</li>
      </ul>

      <h2 id="termination" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">10. Termination</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>For convenience:</strong> Either party may terminate an ongoing engagement with 30 days' written notice unless the SOW specifies otherwise.</li>
        <li><strong>For cause:</strong> Either party may terminate immediately for material breach that is not cured within 14 days of written notice.</li>
        <li><strong>Effect of termination:</strong> You pay for work performed up to the termination date. We deliver work-in-progress and transfer credentials/assets owned by you. Confidentiality and IP terms survive termination.</li>
      </ul>

      <h2 id="dispute" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">11. Dispute Resolution &amp; Governing Law</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">These Terms are governed by the laws of Georgia, without regard to conflict-of-laws principles. The parties will first attempt to resolve any dispute through good-faith negotiation for 30 days, then mediation. If unresolved, the dispute will be submitted to the exclusive jurisdiction of the courts of Tbilisi, Georgia.</p>

      <h2 id="uae" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">12. UAE Clients — Additional Terms</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">For clients headquartered in the United Arab Emirates or contracting via a UAE-based entity:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>Currency:</strong> Fees may be invoiced in AED at the prevailing exchange rate on invoice date.</li>
        <li><strong>Regulatory compliance:</strong> For engagements with DFSA-, ADGM-, RERA-, or DHA-regulated entities, we acknowledge applicable sector regulations on marketing communications and will adapt deliverables accordingly. The client remains responsible for final regulatory sign-off.</li>
        <li><strong>Alternative forum:</strong> By mutual written agreement, parties may elect the DIFC Courts (Dubai) as an alternative jurisdiction for disputes arising from UAE-based engagements.</li>
        <li><strong>Public holidays &amp; working week:</strong> We accommodate the UAE working week (Monday–Friday) and observe agreed UAE public holidays for project timelines.</li>
      </ul>

      <h2 id="general" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">13. General Provisions</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-8 space-y-2">
        <li><strong>Entire agreement:</strong> These Terms together with any signed SOW constitute the entire agreement between the parties.</li>
        <li><strong>Severability:</strong> If any provision is unenforceable, the remainder remains in force.</li>
        <li><strong>Assignment:</strong> Neither party may assign the agreement without the other's written consent, except in connection with a merger or sale of substantially all assets.</li>
        <li><strong>Force majeure:</strong> Neither party is liable for failure to perform due to events beyond reasonable control (natural disasters, war, sanctions, internet outages, etc.).</li>
        <li><strong>Updates:</strong> We may update these Terms; material changes will be noted on this page. Continued use of Services after notice constitutes acceptance.</li>
        <li><strong>Contact:</strong> For questions about these Terms, email <a href="mailto:sales@10xseo.ge" class="text-primary dark:text-primary-light hover:underline">sales@10xseo.ge</a>.</li>
      </ul>
      <p class="text-sm text-body-dark/60 italic">These Terms do not constitute legal advice. For specific contractual questions, please consult a qualified attorney.</p>
    </div>
  </article>
"""

# ============================================================
# CONTENT: COOKIES POLICY (EN)
# ============================================================
COOKIES_MAIN = """  <!-- ========== HERO ========== -->
  <section class="relative pt-24 lg:pt-32 pb-12 lg:pb-16 overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-br from-gray-50 via-white to-primary/5 dark:from-surface-dark dark:via-surface-dark dark:to-primary/5"></div>
    <div class="absolute top-20 right-0 w-[400px] h-[400px] bg-primary/5 dark:bg-primary/10 rounded-full blur-3xl"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-4 sm:px-6 text-center">
      <p class="text-xs font-semibold uppercase tracking-wider text-primary dark:text-primary-light mb-3">Legal</p>
      <h1 class="font-heading text-[28px] sm:text-[36px] lg:text-[48px] font-extrabold text-heading dark:text-heading-dark !leading-[1.15] mb-4">
        <span class="gradient-text">Cookies Policy</span>
      </h1>
      <p class="text-sm text-body dark:text-body-dark/60">__LAST_UPDATED__</p>
    </div>
  </section>

  <!-- ========== ARTICLE ========== -->
  <article class="pb-16 lg:pb-20 bg-white dark:bg-surface-dark">
    <div class="max-w-3xl mx-auto px-4 sm:px-6">
      <p class="text-base text-body dark:text-body-dark mb-8 leading-relaxed">
        This Cookies Policy explains how <strong>LLC 10ixsio.ge</strong> (Georgian legal entity: შპს 10იქსსიო.ჯი; "10xSEO") uses cookies and similar technologies on <a href="https://10xseo.ge" class="text-primary dark:text-primary-light hover:underline">10xseo.ge</a>. Read together with our <a href="privacy-policy.html" class="text-primary dark:text-primary-light hover:underline">Privacy Policy</a>.
      </p>

      <h2 id="what-are-cookies" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">1. What are cookies?</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">Cookies are small text files placed on your device by websites you visit. They store information such as preferences, session identifiers, or analytics IDs. Similar technologies (local storage, pixel tags, SDKs) function the same way for the purposes of this policy.</p>

      <h2 id="categories" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">2. Categories of cookies we use</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-2">
        <li><strong>Strictly necessary</strong> — required for the site to function (e.g., session continuity, security tokens). Cannot be disabled.</li>
        <li><strong>Functional</strong> — remember preferences like language toggle (KA/EN) and theme (dark/light).</li>
        <li><strong>Analytics</strong> — measure traffic and usage in aggregate. Set only with your consent.</li>
        <li><strong>Behavioral</strong> — record session interactions (heatmaps, scroll, clicks) to diagnose UX issues. Form fields and PII are masked by default. Set only with your consent.</li>
        <li><strong>Marketing</strong> — currently <em>none</em>. We do not run remarketing pixels at this time.</li>
      </ul>

      <h2 id="cookies-table" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">3. Specific cookies</h2>
      <div class="overflow-x-auto mb-3">
        <table class="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
          <thead class="bg-surface-alt dark:bg-surface-dark-alt">
            <tr><th class="px-3 py-3 text-left font-semibold text-heading dark:text-heading-dark">Cookie</th><th class="px-3 py-3 text-left font-semibold text-heading dark:text-heading-dark">Provider</th><th class="px-3 py-3 text-left font-semibold text-heading dark:text-heading-dark">Purpose</th><th class="px-3 py-3 text-left font-semibold text-heading dark:text-heading-dark">Lifetime</th><th class="px-3 py-3 text-left font-semibold text-heading dark:text-heading-dark">Category</th></tr>
          </thead>
          <tbody class="text-body dark:text-body-dark">
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-3 py-3 font-mono text-xs">_ga</td><td class="px-3 py-3">Google</td><td class="px-3 py-3">Distinguish visitors</td><td class="px-3 py-3">13 months</td><td class="px-3 py-3">Analytics</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-3 py-3 font-mono text-xs">_ga_&lt;ID&gt;</td><td class="px-3 py-3">Google</td><td class="px-3 py-3">GA4 session state</td><td class="px-3 py-3">13 months</td><td class="px-3 py-3">Analytics</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-3 py-3 font-mono text-xs">_hjSession*</td><td class="px-3 py-3">Hotjar</td><td class="px-3 py-3">Session tracking</td><td class="px-3 py-3">30 minutes</td><td class="px-3 py-3">Behavioral</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-3 py-3 font-mono text-xs">_hjid</td><td class="px-3 py-3">Hotjar</td><td class="px-3 py-3">User identifier</td><td class="px-3 py-3">12 months</td><td class="px-3 py-3">Behavioral</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-3 py-3 font-mono text-xs">__cf_bm</td><td class="px-3 py-3">Calendly</td><td class="px-3 py-3">Booking widget session</td><td class="px-3 py-3">30 minutes</td><td class="px-3 py-3">Functional</td></tr>
            <tr class="border-t border-gray-100 dark:border-gray-800"><td class="px-3 py-3 font-mono text-xs">theme</td><td class="px-3 py-3">10xSEO</td><td class="px-3 py-3">Dark/light mode</td><td class="px-3 py-3">1 year</td><td class="px-3 py-3">Functional</td></tr>
          </tbody>
        </table>
      </div>
      <p class="text-sm text-body-dark/60 italic">List updated as of __LAST_UPDATED_DATE__. Cookie names and lifetimes may vary slightly per provider updates.</p>

      <h2 id="consent" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">4. Consent &amp; control</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">For visitors from the EEA, UK, Switzerland, and UAE, analytics and behavioral cookies are set only after your explicit consent via our cookie banner. You can withdraw consent at any time by clearing your cookies and refreshing the page (the banner will reappear).</p>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">A consent management banner is being implemented; until live, we restrict analytics and behavioral cookies from setting for EEA/UK IP addresses.</p>

      <h2 id="how-to-manage" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">5. How to manage cookies</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">You can refuse or delete cookies via your browser settings:</p>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-1">
        <li><a href="https://support.google.com/chrome/answer/95647" class="text-primary dark:text-primary-light hover:underline" target="_blank" rel="noopener">Google Chrome</a></li>
        <li><a href="https://support.mozilla.org/en-US/kb/clear-cookies-and-site-data-firefox" class="text-primary dark:text-primary-light hover:underline" target="_blank" rel="noopener">Mozilla Firefox</a></li>
        <li><a href="https://support.apple.com/guide/safari/manage-cookies-sfri11471/mac" class="text-primary dark:text-primary-light hover:underline" target="_blank" rel="noopener">Safari (macOS)</a></li>
        <li><a href="https://support.microsoft.com/en-us/microsoft-edge/delete-cookies-in-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" class="text-primary dark:text-primary-light hover:underline" target="_blank" rel="noopener">Microsoft Edge</a></li>
      </ul>

      <h2 id="opt-out" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">6. Opt out of specific services</h2>
      <ul class="list-disc pl-6 text-base text-body dark:text-body-dark mb-3 space-y-1">
        <li><strong>Google Analytics:</strong> <a href="https://tools.google.com/dlpage/gaoptout" class="text-primary dark:text-primary-light hover:underline" target="_blank" rel="noopener">Google Analytics Opt-out Browser Add-on</a></li>
        <li><strong>Hotjar:</strong> <a href="https://www.hotjar.com/legal/compliance/opt-out" class="text-primary dark:text-primary-light hover:underline" target="_blank" rel="noopener">Hotjar Opt-out</a></li>
      </ul>

      <h2 id="uae" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">7. UAE Residents</h2>
      <p class="text-base text-body dark:text-body-dark mb-3 leading-relaxed">For visitors located in the United Arab Emirates, we treat cookie consent in line with UAE Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data, and (for DIFC-related processing) DIFC Data Protection Law No. 5 of 2020. You have the same withdrawal-of-consent and access rights as described in our <a href="privacy-policy.html#uae" class="text-primary dark:text-primary-light hover:underline">Privacy Policy — UAE Residents section</a>.</p>

      <h2 id="contact" class="font-heading text-[22px] sm:text-[26px] font-bold text-heading dark:text-heading-dark mt-10 mb-4">8. Contact</h2>
      <p class="text-base text-body dark:text-body-dark mb-8 leading-relaxed">Questions about cookies? Email us at <a href="mailto:sales@10xseo.ge" class="text-primary dark:text-primary-light hover:underline">sales@10xseo.ge</a>.</p>

      <p class="text-sm text-body-dark/60 italic">This policy is informational and does not constitute legal advice.</p>
    </div>
  </article>
"""

# ============================================================
# PAGE METADATA
# ============================================================
PAGES = {
    'privacy-policy': {
        'title': 'Privacy Policy | 10xSEO',
        'description': 'How 10xSEO collects, uses, and protects your personal data. GDPR + Georgian Data Protection Law + UAE PDPL compliant. Contact us for data requests.',
        'og_image_alt': 'Privacy Policy — 10xSEO',
        'breadcrumb': 'Privacy Policy',
        'main': PRIVACY_MAIN,
        'page_name': 'Privacy Policy',
    },
    'terms-of-service': {
        'title': 'Terms of Service | 10xSEO',
        'description': 'Terms governing use of 10xseo.ge and SEO, content, and growth services by LLC 10ixsio.ge. Governed by Georgian law, with UAE addendum for Dubai clients.',
        'og_image_alt': 'Terms of Service — 10xSEO',
        'breadcrumb': 'Terms of Service',
        'main': TERMS_MAIN,
        'page_name': 'Terms of Service',
    },
    'cookies-policy': {
        'title': 'Cookies Policy | 10xSEO',
        'description': 'How 10xseo.ge uses cookies — analytics (GA4), behavioral (Hotjar), and functional cookies. Manage your cookie preferences and opt out.',
        'og_image_alt': 'Cookies Policy — 10xSEO',
        'breadcrumb': 'Cookies Policy',
        'main': COOKIES_MAIN,
        'page_name': 'Cookies Policy',
    },
}


def build_webpage_schema(slug, page):
    return f'''  <!-- Schema: WebPage -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{page['page_name']} — 10xSEO",
    "description": "{page['description']}",
    "url": "https://10xseo.ge/en/{slug}.html",
    "inLanguage": "en-US",
    "isPartOf": {{
      "@type": "WebSite",
      "name": "10xSEO",
      "url": "https://10xseo.ge"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "10xSEO",
      "legalName": "LLC 10ixsio.ge",
      "url": "https://10xseo.ge",
      "email": "sales@10xseo.ge",
      "telephone": "+995510101517",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "8 Bakhtrioni Street",
        "addressLocality": "Tbilisi",
        "postalCode": "0194",
        "addressCountry": "GE"
      }}
    }}
  }}
  </script>

'''


def build_breadcrumb_schema(slug, page):
    return f'''  <!-- Schema: BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://10xseo.ge/en/"}},
      {{"@type": "ListItem", "position": 2, "name": "{page['breadcrumb']}", "item": "https://10xseo.ge/en/{slug}.html"}}
    ]
  }}
  </script>
'''


def generate(slug, page):
    html = TEMPLATE

    # 1. Remove ContactPage schema block
    html = re.sub(
        r'  <!-- Schema: ContactPage -->\n  <script type="application/ld\+json">\n.*?\n  </script>\n\n',
        '',
        html, count=1, flags=re.DOTALL,
    )

    # 2. Remove FAQPage schema block
    html = re.sub(
        r'  <!-- Schema: FAQPage -->\n  <script type="application/ld\+json">\n.*?\n  </script>\n\n',
        '',
        html, count=1, flags=re.DOTALL,
    )

    # 3. Replace BreadcrumbList schema with new one + insert WebPage schema before it
    new_schemas = build_webpage_schema(slug, page) + build_breadcrumb_schema(slug, page)
    html = re.sub(
        r'  <!-- Schema: BreadcrumbList -->\n  <script type="application/ld\+json">\n.*?\n  </script>',
        new_schemas.rstrip(),
        html, count=1, flags=re.DOTALL,
    )

    # 4. Update head meta tags (precise replacements)
    page_url = f'https://10xseo.ge/en/{slug}.html'
    ka_url = f'https://10xseo.ge/{slug}.html'
    og_image = f'https://10xseo.ge/images/og/page-{slug}-en.jpg'

    replacements = [
        (r'<title>[^<]*</title>', f'<title>{page["title"]}</title>'),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{page["description"]}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{page["title"]}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{page["description"]}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{page_url}">'),
        (r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{og_image}">'),
        (r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{page["og_image_alt"]}">'),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{page["title"]}">'),
        (r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{page["description"]}">'),
        (r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{og_image}">'),
        (r'<meta name="twitter:image:alt" content="[^"]*">', f'<meta name="twitter:image:alt" content="{page["og_image_alt"]}">'),
        (r'<link rel="alternate" hreflang="ka" href="[^"]*">', f'<link rel="alternate" hreflang="ka" href="{ka_url}">'),
        (r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{page_url}">'),
        (r'<link rel="alternate" hreflang="x-default" href="[^"]*">', f'<link rel="alternate" hreflang="x-default" href="{ka_url}">'),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{page_url}">'),
    ]
    for pattern, replacement in replacements:
        html = re.sub(pattern, replacement, html, count=1)

    # 5. Replace main content
    main_body = page['main'].replace('__LAST_UPDATED__', LAST_UPDATED_EN)
    main_body = main_body.replace('__LAST_UPDATED_DATE__', 'May 13, 2026')
    new_main = f'<main id="main-content">\n{main_body}\n  </main>'
    html = re.sub(
        r'<main id="main-content">.*?</main>',
        lambda m: new_main,
        html, count=1, flags=re.DOTALL,
    )

    # 6. Strip the first <script> block after </footer> (contact form + theme + FAQ logic)
    # That block contains broken JS that errors out anyway; cleaner to remove for legal pages.
    html = re.sub(
        r'  <!-- ========== SCRIPTS ========== -->\n  <script>\n    // Theme toggle.*?\n  </script>\n\n  <script>\n    // Mobile menu with animation',
        '  <!-- ========== SCRIPTS ========== -->\n  <script>\n    // Mobile menu with animation',
        html, count=1, flags=re.DOTALL,
    )

    # 7. Calendly widget kept intact — mobile menu "Book Consultation" button references openCalendly()

    # Sanity checks
    assert page_url in html, f'canonical URL not set in {slug}'
    assert page['title'] in html, f'title not set in {slug}'
    assert '<main id="main-content">' in html, f'main wrapper missing in {slug}'
    assert 'sales@10xseo.ge' in html, f'NAP email missing in {slug}'
    assert '+995510101517' in html or '+995 510 10 15 17' in html, f'NAP phone missing in {slug}'

    out = ROOT / 'en' / f'{slug}.html'
    out.write_text(html, encoding='utf-8')
    print(f'  ✓ Wrote {out} ({len(html):,} bytes)')


def main():
    print('Generating EN legal pages from en/contact-us.html template...\n')
    for slug, page in PAGES.items():
        print(f'=== {slug} ===')
        generate(slug, page)
    print('\nDone.')


if __name__ == '__main__':
    main()
