/* Lead forms: honeypot + minimum time-to-submit + validation + PHI guard.
   Backend from data-* attributes (set by _build/config.json form_backend). No form values go to analytics. */
(function () {
  var MIN_MS = 4000, EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/, PHONE = /^[0-9()+.\- ]{7,30}$/;
  var PHI = /\b(0?[1-9]|1[0-2])[\/\-](0?[1-9]|[12]\d|3[01])[\/\-](19|20)\d{2}\b|\b\d{9,}\b/; // DOB-like dates, long ID-like numbers
  var start = Date.now(), C = window.MBT_FORM || { enabled: false };
  function msg(f, t, bad) { var m = f.querySelector('.form-msg'); m.textContent = t; m.className = 'form-msg' + (bad ? ' bad' : ' ok'); }
  function utm() { var q = new URLSearchParams(location.search), o = {}; ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid'].forEach(function (k) { if (q.get(k)) o[k] = q.get(k).slice(0, 120); }); return o; }
  document.querySelectorAll('form.lead-form').forEach(function (f) {
    // Backend not connected: keep submit disabled and the 'temporarily unavailable' notice visible (nothing is ever silently dropped).
    if (!C.enabled || !C.endpoint) { f.querySelectorAll('button[type=submit]').forEach(function (b) { b.disabled = true; }); f.classList.add('is-off'); }
    else { f.classList.remove('is-off'); var off = f.querySelector('.form-off'); if (off) off.remove(); f.querySelectorAll('button[type=submit]').forEach(function (b) { b.disabled = false; b.removeAttribute('aria-disabled'); }); }
    var phone = f.querySelector('[name=phone]'), tcpa = f.querySelector('.tcpa');
    if (phone && tcpa) phone.addEventListener('input', function () { tcpa.hidden = !phone.value.trim(); if (tcpa.hidden) tcpa.querySelector('input').checked = false; });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (f.dataset.busy) return;
      var d = new FormData(f);
      if ((d.get('company_website') || '').trim()) { msg(f, 'Thanks.'); return; }                // honeypot: silently drop
      if (Date.now() - start < MIN_MS) { msg(f, 'Please take a moment to review your details, then submit again.', true); return; }
      var bad = [];
      f.querySelectorAll('[required]').forEach(function (el) { var ok = el.value.trim() !== ''; el.toggleAttribute('aria-invalid', !ok); if (!ok) bad.push(el); });
      var em = f.querySelector('[name=work_email]');
      if (em && em.value && !EMAIL.test(em.value.trim())) { bad.push(em); em.setAttribute('aria-invalid', ''); }
      if (phone && phone.value.trim() && !PHONE.test(phone.value.trim())) { bad.push(phone); phone.setAttribute('aria-invalid', ''); }
      if (bad.length) { msg(f, 'Please complete the required fields. Remember: no patient information.', true); bad[0].focus(); return; }
      var texts = ['name', 'practice_name'].map(function (k) { return d.get(k) || ''; }).join(' ');
      if (PHI.test(texts)) { msg(f, 'This looks like it may contain patient information. Please remove it.', true); return; }
      var row = {
        form_id: d.get('form_id'), name: (d.get('name') || '').trim(), role: d.get('role') || null,
        practice_name: (d.get('practice_name') || '').trim(), specialty: d.get('specialty') || null,
        num_providers: d.get('num_providers') || null, monthly_collections: d.get('monthly_collections') || null,
        billing_setup: d.get('billing_setup') || null, help_areas: d.getAll('help_areas'),
        work_email: (d.get('work_email') || '').trim().toLowerCase(), phone: (d.get('phone') || '').trim() || null,
        tcpa_consent: d.get('tcpa_consent') === 'yes', tcpa_text_version: d.get('tcpa_consent') === 'yes' ? f.dataset.tcpaVersion : null,
        source_page: location.href.split('#')[0].slice(0, 500), utm: utm(), user_agent: navigator.userAgent.slice(0, 300),
        elapsed_ms: Date.now() - start, is_test: /[?&]mbt_test=1\b/.test(location.search)
      };
      if (!C.enabled || !C.endpoint) { msg(f, 'Online requests are temporarily unavailable. Please try again shortly. Nothing was sent.', true); return; }
      f.dataset.busy = '1'; msg(f, 'Sending…');
      var done = function () {
        var t = f.dataset.thanks || '', went = false;
        var go = function () { if (went) return; went = true;
          if (t.charAt(0) === '#') { var g = document.querySelector(t); if (g) { g.hidden = false; f.hidden = true; g.scrollIntoView(); } return; }
          location.href = t; };
        // GA4 generate_lead fires on confirmed success only (no form values); navigation waits at most 1.2 s for it.
        if (window.gtag) { try { gtag('event', 'generate_lead', { form_type: row.form_id, event_callback: go, event_timeout: 1200 }); } catch (x) {} setTimeout(go, 1300); } else go();
      };
      var fail = function () { delete f.dataset.busy; msg(f, 'Sorry, something went wrong. Please try again in a minute.', true); };
      // Google Apps Script web app (form-urlencoded = CORS "simple" request, no preflight). The endpoint URL is public by design.
      var body = new URLSearchParams(); body.append('form_key', C.formKey || '');
      Object.keys(row).forEach(function (k) { var v = row[k]; body.append(k, typeof v === 'object' && v !== null ? JSON.stringify(v) : (v == null ? '' : String(v))); });
      var errs = { possible_phi: 'This looks like it may contain patient information. Please remove it.',
        missing_fields: 'Please complete the required fields. Remember: no patient information.',
        rate_limited: "We already have a request from this email. We'll be in touch by email." };
      fetch(C.endpoint, { method: 'POST', body: body, redirect: 'follow' })
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.ok) done(); else { delete f.dataset.busy; if (j && errs[j.error]) msg(f, errs[j.error], true); else fail(); } }, fail);
      // An unreadable response (network error, non-JSON, CORS) shows the visible error; we never report success we can't confirm.
    });
  });
  document.querySelectorAll('[data-unlock]').forEach(function (b) { b.addEventListener('click', function () { var g = document.getElementById('unlocked'); if (g) g.hidden = false; }); });
  var s = document.querySelector('.sticky-cta'), hero = document.querySelector('.hero');
  if (s && !sessionStorage.getItem('mbt_cta_x')) {
    var onScroll = function () {
      var h = document.documentElement, past = hero ? hero.getBoundingClientRect().bottom < 0 : (h.scrollTop + innerHeight) / h.scrollHeight > 0.4;
      if (past) { s.hidden = false; removeEventListener('scroll', onScroll); }
    };
    addEventListener('scroll', onScroll, { passive: true });
    s.querySelector('.x').addEventListener('click', function () { s.hidden = true; sessionStorage.setItem('mbt_cta_x', '1'); });
  }
  // presentation only: header shadow on scroll + subtle reveal (skipped when the user prefers reduced motion)
  var hdr = document.querySelector('.site-header');
  if (hdr) { var sh = function () { hdr.classList.toggle('scrolled', scrollY > 8); }; addEventListener('scroll', sh, { passive: true }); sh(); }
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.tile, .feature-list li, .resource-card, .faq details, .trust-row li').forEach(function (el) {
      if (el.getBoundingClientRect().top > innerHeight) { el.classList.add('reveal'); io.observe(el); }
    });
  }
})();
