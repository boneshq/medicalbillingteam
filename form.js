/* Lead forms: honeypot + minimum time-to-submit + validation + PHI guard.
   Backend from data-* attributes (set by _build/config.json form_backend). No form values go to analytics. */
(function () {
  var MIN_MS = 4000, EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/, PHONE = /^[0-9()+.\- ]{7,30}$/;
  var PHI = /\b(0?[1-9]|1[0-2])[\/\-](0?[1-9]|[12]\d|3[01])[\/\-](19|20)\d{2}\b|\b\d{9,}\b/; // DOB-like dates, long ID-like numbers
  var start = Date.now(), C = window.MBT_FORM || { enabled: false };
  function msg(f, t, bad) { var m = f.querySelector('.form-msg'); m.textContent = t; m.className = 'form-msg' + (bad ? ' bad' : ' ok'); }
  function utm() { var q = new URLSearchParams(location.search), o = {}; ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid'].forEach(function (k) { if (q.get(k)) o[k] = q.get(k).slice(0, 120); }); return o; }
  document.querySelectorAll('form.lead-form').forEach(function (f) {
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
      if (!C.enabled) { msg(f, 'Preview build: the form backend is not connected yet, so nothing was sent.', true); return; }
      f.dataset.busy = '1'; msg(f, 'Sending…');
      var done = function () {
        try { window.gtag && gtag('event', 'generate_lead', { form_id: row.form_id }); } catch (x) {}
        var t = f.dataset.thanks || '';
        if (t.charAt(0) === '#') { var g = document.querySelector(t); if (g) { g.hidden = false; f.hidden = true; g.scrollIntoView(); } return; }
        location.href = t;
      };
      var fail = function () { delete f.dataset.busy; msg(f, 'Sorry, something went wrong. Please try again in a minute.', true); };
      if (C.mode === 'supabase' && C.anonKey) {
        fetch(C.supabaseUrl + '/rest/v1/' + C.table, { method: 'POST',
          headers: { apikey: C.anonKey, Authorization: 'Bearer ' + C.anonKey, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
          body: JSON.stringify(row) }).then(function (r) { r.ok ? done() : fail(); }, fail);
      } else if (C.mode === 'apps_script' && C.appsScriptUrl) {
        var body = new URLSearchParams(); Object.keys(row).forEach(function (k) { var v = row[k]; body.append(k, typeof v === 'object' && v !== null ? JSON.stringify(v) : (v == null ? '' : String(v))); });
        fetch(C.appsScriptUrl, { method: 'POST', mode: 'no-cors', body: body }).then(done, fail);
      } else fail();
    });
  });
  document.querySelectorAll('[data-unlock]').forEach(function (b) { b.addEventListener('click', function () { var g = document.getElementById('unlocked'); if (g) g.hidden = false; }); });
  var s = document.querySelector('.sticky-cta');
  if (s && !sessionStorage.getItem('mbt_cta_x')) {
    var onScroll = function () { var h = document.documentElement; if ((h.scrollTop + innerHeight) / h.scrollHeight > 0.4) { s.hidden = false; removeEventListener('scroll', onScroll); } };
    addEventListener('scroll', onScroll, { passive: true });
    s.querySelector('.x').addEventListener('click', function () { s.hidden = true; sessionStorage.setItem('mbt_cta_x', '1'); });
  }
})();
