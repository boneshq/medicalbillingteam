/* Medical Billing Team AI assistant widget (vanilla JS, no dependencies). Built into /chat.js by _build/src/build.py.
   Lazy: the inline loader injects this file only after window load + 8 s + idle. No visitor text ever goes to analytics. */
(function () {
  if (window.MBTChat) return;
  var C = {"endpoint": "https://tuolsdkjnzrtqmmzxvoq.supabase.co/functions/v1/mbt-chat", "ai": "AI assistant. It may make mistakes, and it isn't medical or legal advice.", "aff": "Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our <a href=\"/approved-vendors/\">approved vendor list</a>. Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. <a href=\"/how-we-vet-vendors/\">How we vet vendors</a>.", "phi": "Do not include any patient information. Please don't enter patient names, dates of birth, addresses, member or policy IDs, claim numbers, diagnoses or any health details anywhere on this site.", "tcpa": "By checking this box, I agree that Alliance Global Solutions may call or text me at the number I provided about remote medical billing and revenue cycle staffing, including calls or texts made with an autodialer or prerecorded or artificial voice. Consent is not a condition of any purchase or of receiving the assessment. Message and data rates may apply. Message frequency varies. Reply STOP to opt out or HELP for help.", "tcpaV": "2026-10-18-v1", "email": "By submitting, you agree that we may email you about your request and about remote billing and RCM staffing. Every marketing email includes an unsubscribe link, and we honor opt-outs promptly.", "ref": "Your request will be shared with Alliance Global Solutions, our affiliated approved vendor, so it can follow up."};
  var D = document, LS = window.localStorage, SS = window.sessionStorage;
  var K_DIS = 'mbt_chat_dismissed', K_S = 'mbt_chat_s', K_NAV = 'mbt_chat_nav';
  var IDLE_MS = 10 * 60 * 1000, MAX = 500;
  var isTest = /[?&]mbt_test=1\b/.test(location.search);
  var mq = window.matchMedia ? matchMedia('(max-width: 599px)') : { matches: false };
  function get(k, s) { try { return (s || LS).getItem(k); } catch (e) { return null; } }
  function set(k, v, s) { try { (s || LS).setItem(k, v); } catch (e) {} }
  var S; try { S = JSON.parse(get(K_S, SS) || 'null'); } catch (e) { S = null; }
  if (!S) S = { token: '', msgs: [], mailed: 0, open: 0, last: 0, lead: 0 };
  function save() { set(K_S, JSON.stringify(S), SS); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function md(s) {
    var h = esc(s);
    h = h.replace(/\[([^\]]{1,120})\]\((https:\/\/[^)\s"]+)\)/g, function (a, t, u) {
      var ext = !/^https:\/\/(www\.)?medicalbillingteam\.com\//.test(u);
      return '<a href="' + u + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '>' + t + '</a>';
    });
    h = h.replace(/\*\*([^*]{1,200})\*\*/g, '<strong>$1</strong>');
    return h.split(/\n+/).map(function (l) { return /^\s*[-*•]\s+/.test(l) ? '<span class="mc-li">' + l.replace(/^\s*[-*•]\s+/, '') + '</span>' : l; }).join('<br>');
  }
  var css = '#mbt-chat{--mc-n:var(--navy,#0b1a31);--mc-g:var(--gold,#e09e1c);font:15px/1.45 var(--sans,system-ui,-apple-system,Segoe UI,Roboto,sans-serif);color:#13233b}' +
    '#mbt-chat *{box-sizing:border-box}' +
    '.mc-launch{position:fixed;right:18px;bottom:calc(18px + var(--mc-off,0px));z-index:60;width:56px;height:56px;border-radius:50%;border:0;background:var(--mc-n);color:#fff;box-shadow:0 8px 24px rgba(11,26,49,.3);cursor:pointer;display:grid;place-items:center;transition:transform .2s}' +
    '.mc-launch:hover{transform:translateY(-2px)}.mc-launch svg{width:26px;height:26px}.mc-launch:focus-visible,.mc-x:focus-visible,.mc-btn:focus-visible{outline:3px solid var(--mc-g);outline-offset:2px}' +
    '.mc-dot{position:absolute;top:6px;right:6px;width:11px;height:11px;border-radius:50%;background:var(--mc-g);border:2px solid var(--mc-n)}' +
    '.mc-teaser{position:fixed;right:18px;bottom:calc(84px + var(--mc-off,0px));z-index:60;width:300px;background:#fff;border-radius:16px;box-shadow:0 12px 40px rgba(11,26,49,.22);padding:16px 40px 14px 16px;animation:mcIn .35s cubic-bezier(.2,.7,.2,1) both}' +
    '.mc-teaser p{margin:0 0 10px}.mc-teaser .mc-small{font-size:12px;color:#5a6b80;margin:8px 0 0}' +
    '.mc-x{position:absolute;top:6px;right:6px;width:32px;height:32px;border:0;background:transparent;border-radius:50%;font-size:20px;line-height:1;color:#5a6b80;cursor:pointer}.mc-x:hover{background:#eef2f7}' +
    '.mc-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:40px;padding:8px 14px;border-radius:999px;border:0;background:var(--mc-g);color:var(--mc-n);font-weight:700;font-size:14px;cursor:pointer}' +
    '.mc-btn.mc-ghost{background:#eef2f7;color:var(--mc-n)}.mc-btn[disabled]{opacity:.6;cursor:wait}' +
    '.mc-panel{position:fixed;right:18px;bottom:calc(84px + var(--mc-off,0px));z-index:61;width:380px;height:min(620px,calc(100vh - 110px));display:flex;flex-direction:column;background:#fff;border-radius:18px;box-shadow:0 18px 60px rgba(11,26,49,.3);overflow:hidden;animation:mcIn .3s cubic-bezier(.2,.7,.2,1) both}' +
    '.mc-panel[hidden],.mc-teaser[hidden],.mc-lead[hidden]{display:none}' +
    '.mc-head{background:var(--mc-n);color:#fff;padding:12px 44px 12px 16px;position:relative}.mc-head b{display:block;font-size:15px}.mc-head span{font-size:12px;color:#b9c7d8}.mc-head .mc-x{color:#b9c7d8;top:8px}.mc-head .mc-x:hover{background:rgba(255,255,255,.1)}' +
    '.mc-disc{font-size:12px;color:#4a5b70;background:#f6f8fb;padding:8px 14px;border-bottom:1px solid #e3e8ef}.mc-disc p{margin:0}.mc-disc details{margin-top:4px}.mc-disc summary{cursor:pointer;color:var(--mc-n);font-weight:600}.mc-disc a{color:inherit}' +
    '.mc-log{flex:1;overflow-y:auto;padding:12px 14px;display:flex;flex-direction:column;gap:10px;overscroll-behavior:contain}' +
    '.mc-m{max-width:88%;padding:9px 12px;border-radius:14px;word-wrap:break-word}.mc-a{background:#f1f4f8;align-self:flex-start;border-bottom-left-radius:4px}.mc-u{background:var(--mc-n);color:#fff;align-self:flex-end;border-bottom-right-radius:4px}' +
    '.mc-s{align-self:center;font-size:12px;color:#5a6b80;text-align:center}.mc-a a{color:#0b4f9c}.mc-li{display:block;padding-left:12px;text-indent:-10px}.mc-li:before{content:"• "}' +
    '.mc-src{font-size:12px;color:#5a6b80;margin-top:6px}.mc-src a{color:#0b4f9c}.mc-typing{color:#5a6b80;font-style:italic}' +
    '.mc-chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 8px}.mc-chips button{border:1px solid #cdd6e2;background:#fff;border-radius:999px;padding:6px 10px;font-size:13px;color:var(--mc-n);cursor:pointer}' +
    '.mc-foot{border-top:1px solid #e3e8ef;padding:8px 12px 10px}.mc-row{display:flex;gap:8px;align-items:flex-end}' +
    '.mc-row textarea{flex:1;resize:none;min-height:42px;max-height:110px;border:1px solid #cdd6e2;border-radius:12px;padding:10px 12px;font:inherit;font-size:16px}' +
    '.mc-phi{font-size:11.5px;color:#5a6b80;margin:6px 0 6px}.mc-acts{display:flex;justify-content:space-between;align-items:center;gap:8px}.mc-count{font-size:11px;color:#8191a5}' +
    '.mc-lead{padding:10px 14px;border-top:1px solid #e3e8ef;background:#fbfcfe;overflow-y:auto;max-height:62%}.mc-lead label{display:block;font-size:13px;font-weight:600;margin:6px 0 2px}' +
    '.mc-lead input[type=text],.mc-lead input[type=email],.mc-lead input[type=tel]{width:100%;border:1px solid #cdd6e2;border-radius:10px;padding:9px 10px;font:inherit;font-size:16px}' +
    '.mc-lead .mc-chk{display:flex;gap:8px;font-weight:400;font-size:11.5px;color:#4a5b70;line-height:1.35}.mc-lead .mc-chk input{margin-top:3px;flex:none}.mc-lead p{font-size:11.5px;color:#4a5b70;margin:6px 0}' +
    '.mc-tm{display:none}.mc-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}.mc-err{color:#b3261e;font-size:13px;min-height:1em;margin:4px 0}' +
    '@media(max-width:599px){.mc-launch{width:48px;height:48px;right:12px;bottom:calc(12px + var(--mc-off,0px))}.mc-launch svg{width:22px;height:22px}' +
    '.mc-teaser{right:68px;bottom:calc(14px + var(--mc-off,0px));width:auto;max-width:calc(100vw - 84px);padding:9px 34px 9px 12px;border-radius:999px;font-size:13.5px}.mc-teaser p{margin:0}.mc-teaser .mc-x{top:50%;transform:translateY(-50%);width:28px;height:28px;font-size:18px}' +
    '.mc-teaser .mc-small,.mc-teaser .mc-btn,.mc-tl{display:none}.mc-tm{display:inline!important}.mc-panel{right:0;left:0;bottom:0;width:auto;height:88vh;height:88dvh;border-radius:18px 18px 0 0}}' +
    '@keyframes mcIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}' +
    '@media(prefers-reduced-motion:reduce){.mc-teaser,.mc-panel{animation:none}.mc-launch{transition:none}}';
  var st = D.createElement('style'); st.textContent = css; D.head.appendChild(st);
  var R = D.createElement('div'); R.id = 'mbt-chat';
  R.innerHTML =
    '<div class="mc-teaser" role="complementary" aria-label="Chat assistant" hidden><button class="mc-x" type="button" aria-label="Dismiss chat prompt">×</button>' +
      '<p><span class="mc-tl">Questions about billing staff, VOB, credentialing or prior auth? </span><span class="mc-tm">Questions? </span><a href="#" class="mc-ask">Ask our AI assistant</a></p>' +
      '<button class="mc-btn mc-ask" type="button">Ask a question</button><p class="mc-small">' + esc(C.ai) + '</p></div>' +
    '<section class="mc-panel" role="dialog" aria-modal="false" aria-label="Medical Billing Team AI assistant" hidden>' +
      '<div class="mc-head"><b>Medical Billing Team assistant</b><span>AI assistant · answers from this site\'s guides</span><button class="mc-x mc-close" type="button" aria-label="Close chat">×</button></div>' +
      '<div class="mc-disc"><p><strong>' + esc(C.ai) + '</strong></p><details><summary>Affiliation disclosure</summary><p>' + C.aff + '</p></details></div>' +
      '<div class="mc-log" aria-live="polite"></div>' +
      '<div class="mc-chips"></div>' +
      '<form class="mc-lead" novalidate hidden><b>Schedule a consultation</b><p>Leave your details and a person will follow up. ' + esc(C.phi) + '</p>' +
        '<div class="mc-hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>' +
        '<label for="mc-n">Your name</label><input id="mc-n" name="name" type="text" autocomplete="name" maxlength="100" required>' +
        '<label for="mc-e">Work email</label><input id="mc-e" name="work_email" type="email" autocomplete="email" maxlength="150" required>' +
        '<label for="mc-p">Phone</label><input id="mc-p" name="phone" type="tel" autocomplete="tel" maxlength="30" required>' +
        '<label for="mc-o">Practice or company <i>(optional)</i></label><input id="mc-o" name="practice_name" type="text" autocomplete="organization" maxlength="150">' +
        '<label class="mc-chk"><input type="checkbox" name="tcpa_consent" value="yes"><span>' + esc(C.tcpa) + ' <i>(optional)</i></span></label>' +
        '<p>' + esc(C.email) + '</p><p>' + esc(C.ref) + '</p>' +
        '<p class="mc-err" role="status"></p><div class="mc-acts"><button class="mc-btn" type="submit">Request a consultation</button><button class="mc-btn mc-ghost mc-cancel" type="button">Back to chat</button></div></form>' +
      '<form class="mc-foot mc-in"><div class="mc-row"><label class="mc-hp" for="mc-t">Your question</label><textarea id="mc-t" rows="1" maxlength="' + MAX + '" placeholder="Ask about billing staff, VOB, prior auth…"></textarea>' +
        '<button class="mc-btn" type="submit" aria-label="Send">Send</button></div>' +
        '<p class="mc-phi" role="note"><strong>Do not include any patient information.</strong> ' + esc(C.phi.split('. ').slice(1).join('. ')) + '</p>' +
        '<div class="mc-acts"><button class="mc-btn mc-ghost mc-book" type="button">Schedule a consultation</button><span class="mc-count"></span></div></form>' +
    '</section>' +
    '<button class="mc-launch" type="button" aria-label="Open the AI chat assistant" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></button>';
  D.body.appendChild(R);
  var $ = function (s) { return R.querySelector(s); };
  var launch = $('.mc-launch'), teaser = $('.mc-teaser'), panel = $('.mc-panel'), log = $('.mc-log'), chips = $('.mc-chips'),
    inF = $('.mc-in'), ta = $('#mc-t'), leadF = $('.mc-lead'), cnt = $('.mc-count'), err = $('.mc-err');

  // keep the launcher above the sticky CTA bar when it's showing
  var sticky = D.querySelector('.sticky-cta');
  function off() { var o = 0; if (sticky && !sticky.hidden) { var r = sticky.getBoundingClientRect(); if (r.height) o = Math.max(0, innerHeight - r.top) + 4; } R.style.setProperty('--mc-off', o + 'px'); }
  if (sticky) { addEventListener('scroll', off, { passive: true }); addEventListener('resize', off); new MutationObserver(off).observe(sticky, { attributes: true }); } off();

  function api(o) {
    return fetch(C.endpoint, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body: JSON.stringify(o) })
      .then(function (r) { return r.json().catch(function () { return { ok: false, error: 'http_' + r.status }; }); });
  }
  function add(m, sources) {
    var d = D.createElement('div');
    d.className = 'mc-m ' + (m.r === 'u' ? 'mc-u' : m.r === 's' ? 'mc-s' : 'mc-a');
    d.innerHTML = m.r === 'a' ? md(m.c) : esc(m.c);
    if (sources && sources.length) d.innerHTML += '<div class="mc-src">Sources: ' + sources.map(function (s) { return '<a href="' + esc(s.u) + '">' + esc(s.t.split(' > ')[0].slice(0, 60)) + '</a>'; }).join(' · ') + '</div>';
    log.appendChild(d); log.scrollTop = log.scrollHeight; return d;
  }
  var GREET = 'Hi! I can answer questions about medical billing, RCM, VOB for treatment centers, credentialing and prior authorization, using this site\'s guides. When you\'re ready to talk with a person, tap "Schedule a consultation."';
  var CHIPS = ['What does an RCM team do?', 'How does VOB work for treatment centers?', 'What does a credentialing specialist do?', 'Can remote staff handle prior authorizations?'];
  function render() {
    log.innerHTML = ''; add({ r: 'a', c: GREET });
    S.msgs.forEach(function (m) { add(m); });
    chips.innerHTML = S.msgs.length ? '' : CHIPS.map(function (c) { return '<button type="button">' + esc(c) + '</button>'; }).join('');
    cnt.textContent = '';
  }
  function hideTeaser() { teaser.hidden = true; launch.querySelector('.mc-dot') && launch.querySelector('.mc-dot').remove(); }
  function dismiss() { hideTeaser(); set(K_DIS, '1'); }
  var starting = null;
  function ensure() {
    if (S.token) return Promise.resolve(true);
    if (!starting) starting = api({ action: 'start', page: location.href.split('#')[0].slice(0, 300), is_test: isTest }).then(function (j) {
      starting = null; if (j && j.ok && j.token) { S.token = j.token; S.t0 = Date.now(); save(); return true; } return false; }, function () { starting = null; return false; });
    return starting;
  }
  function open() { hideTeaser(); panel.hidden = false; launch.setAttribute('aria-expanded', 'true'); S.open = 1; save(); render(); ensure(); setTimeout(function () { (leadF.hidden ? ta : $('#mc-n')).focus({ preventScroll: true }); }, 30); }
  function close() { panel.hidden = true; launch.setAttribute('aria-expanded', 'false'); S.open = 0; save(); launch.focus({ preventScroll: true }); }
  launch.addEventListener('click', function () { panel.hidden ? open() : close(); });
  R.querySelectorAll('.mc-ask').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); open(); }); });
  teaser.querySelector('.mc-x').addEventListener('click', dismiss);
  $('.mc-close').addEventListener('click', function () { close(); set(K_DIS, '1'); });
  R.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) close(); });
  chips.addEventListener('click', function (e) { if (e.target.tagName === 'BUTTON') { ta.value = e.target.textContent; send(); } });
  ta.addEventListener('input', function () { ta.style.height = 'auto'; ta.style.height = Math.min(110, ta.scrollHeight) + 'px'; var n = ta.value.length; cnt.textContent = n > MAX - 80 ? n + '/' + MAX : ''; });
  ta.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } });
  inF.addEventListener('submit', function (e) { e.preventDefault(); send(); });
  var busy = false, idleT = null;
  function idle() { clearTimeout(idleT); var wait = Math.max(5000, (S.last || Date.now()) + IDLE_MS - Date.now()); if (S.msgs.length > S.mailed) idleT = setTimeout(function () { end('idle'); }, wait); }
  function send() {
    var t = ta.value.replace(/\s+/g, ' ').trim(); if (!t || busy) return;
    if (t.length > MAX) { add({ r: 's', c: 'Please keep messages under ' + MAX + ' characters.' }); return; }
    busy = true; chips.innerHTML = ''; ta.value = ''; ta.style.height = '';
    var u = add({ r: 'u', c: t }), w = add({ r: 'a', c: 'Thinking…' }); w.classList.add('mc-typing');
    var go = function (retry) {
      ensure().then(function (ok) {
        if (!ok) throw 0;
        return api({ action: 'msg', token: S.token, messages: S.msgs, text: t });
      }).then(function (j) {
        if (j && j.error === 'session' && !retry) { S.token = ''; S.msgs = []; S.mailed = 0; save(); return go(1); }
        if (j && j.error === 'slow_down' && !retry) { return setTimeout(function () { go(1); }, 1600); }
        w.remove(); busy = false;
        if (!j || !j.ok) { add({ r: 's', c: j && j.error === 'rate_limited' ? 'Too many messages. Please wait a few minutes, or tap "Schedule a consultation."' : j && j.error === 'too_long' ? 'Please keep messages under ' + MAX + ' characters.' : 'Sorry, the assistant is unavailable right now. Please try again shortly, or tap "Schedule a consultation."' }); return; }
        if (j.flagged) u.textContent = j.user;
        S.msgs.push({ r: 'u', c: j.user }, { r: 'a', c: j.reply }); S.token = j.token; S.last = Date.now(); save();
        add({ r: 'a', c: j.reply }, j.sources); idle();
        if (j.limit) $('.mc-book').click();
      }).catch(function () { w.remove(); busy = false; add({ r: 's', c: 'Sorry, the assistant is unavailable right now. Please try again shortly, or tap "Schedule a consultation."' }); });
    };
    go(0);
  }
  $('.mc-book').addEventListener('click', function () { if (S.lead) { add({ r: 's', c: 'Thanks, we already have your details. A person will follow up.' }); return; } leadF.hidden = false; inF.hidden = true; ensure(); $('#mc-n').focus(); });
  $('.mc-cancel').addEventListener('click', function () { leadF.hidden = true; inF.hidden = false; ta.focus(); });
  var EM = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/, PH = /^[0-9()+.\- ]{7,30}$/;
  var PHI = /\b(0?[1-9]|1[0-2])[\/\-](0?[1-9]|[12]\d|3[01])[\/\-](19|20)\d{2}\b|\b\d{9,}\b/;
  leadF.addEventListener('submit', function (e) {
    e.preventDefault(); if (busy) return;
    var f = new FormData(leadF), v = function (k) { return String(f.get(k) || '').trim(); };
    if (v('company_website')) { leadF.hidden = true; inF.hidden = false; add({ r: 's', c: 'Thanks.' }); return; }
    if (!v('name') || !EM.test(v('work_email')) || !PH.test(v('phone'))) { err.textContent = 'Please add your name, a valid email and a phone number. Remember: no patient information.'; return; }
    if (PHI.test(v('name') + ' ' + v('practice_name'))) { err.textContent = 'This looks like it may contain patient information. Please remove it.'; return; }
    busy = true; err.textContent = 'Sending…'; var btn = leadF.querySelector('[type=submit]'); btn.disabled = true;
    var q = new URLSearchParams(location.search), utm = {}; ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid'].forEach(function (k) { if (q.get(k)) utm[k] = q.get(k).slice(0, 120); });
    ensure().then(function (ok) {
      if (!ok) throw 0;
      return api({ action: 'lead', token: S.token, messages: S.msgs, name: v('name'), work_email: v('work_email').toLowerCase(), phone: v('phone'), practice_name: v('practice_name'),
        tcpa_consent: f.get('tcpa_consent') === 'yes', tcpa_text_version: f.get('tcpa_consent') === 'yes' ? C.tcpaV : '', company_website: '', page: location.href.split('#')[0].slice(0, 300), utm: utm });
    }).then(function (j) {
      busy = false; btn.disabled = false;
      if (j && j.ok) {
        if (j.token) { S.msgs.push({ r: 's', c: j.note }); S.token = j.token; S.mailed = S.msgs.length; }
        S.lead = 1; save(); leadF.reset(); leadF.hidden = true; inF.hidden = false; err.textContent = '';
        add({ r: 'a', c: 'Thanks, ' + v('name').split(' ')[0].replace(/^\[TEST\]$/i, 'there') + '! Your request is in. A person will follow up by email or phone, usually within one business day.' });
        // GA4 generate_lead on confirmed success only; no form values or chat text are sent.
        if (window.gtag) try { gtag('event', 'generate_lead', { form_type: 'chat' }); } catch (x) {}
        return;
      }
      err.textContent = j && j.error === 'possible_phi' ? 'This looks like it may contain patient information. Please remove it.' :
        j && j.error === 'missing_fields' ? 'Please add your name, a valid email and a phone number.' :
        j && (j.error === 'rate_limited' || j.error === 'already') ? 'We already have a request from you. We\'ll be in touch.' :
        j && j.error === 'slow_down' ? 'Please take a moment to review your details, then submit again.' : 'Sorry, something went wrong. Please try again in a minute.';
    }).catch(function () { busy = false; btn.disabled = false; err.textContent = 'Sorry, something went wrong. Please try again in a minute.'; });
  });
  function end(reason, beacon) {
    if (!S.token || S.msgs.length <= S.mailed || !S.msgs.some(function (m) { return m.r === 'u'; })) return;
    var body = JSON.stringify({ action: 'end', token: S.token, messages: S.msgs, reason: reason });
    if (beacon && navigator.sendBeacon) { if (navigator.sendBeacon(C.endpoint, new Blob([body], { type: 'text/plain;charset=UTF-8' }))) { S.mailed = S.msgs.length; save(); } return; }
    api(JSON.parse(body)).then(function (j) { if (j && j.ok && j.token) { S.token = j.token; S.mailed = S.msgs.length; save(); } });
  }
  // session end: leaving the site (not same-site navigation, which keeps the session) or 10 min idle
  D.addEventListener('click', function (e) { var a = e.target.closest && e.target.closest('a[href]'); if (a && a.host === location.host && !a.target) set(K_NAV, '1', SS); }, true);
  addEventListener('pagehide', function () { if (get(K_NAV, SS)) { try { SS.removeItem(K_NAV); } catch (x) {} return; } end('pagehide', true); });
  try { SS.removeItem(K_NAV); } catch (x) {}
  idle();
  window.MBTChat = { open: open, close: close, end: end };
  // first appearance: restore an open session, otherwise a small teaser (unless dismissed before)
  if (S.open && !mq.matches) open();
  else if (!get(K_DIS) && !S.msgs.length) { teaser.hidden = false; var dot = D.createElement('span'); dot.className = 'mc-dot'; launch.appendChild(dot); }
})();
