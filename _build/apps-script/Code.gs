/**
 * MedicalBillingTeam Leads: Apps Script web app, bound to the "MedicalBillingTeam Leads" Google Sheet
 * (https://docs.google.com/spreadsheets/d/1-6vsIf2-g_eHqXTy3Wb2JEEPIy7mfPEE-EYjTnXXVM4/edit, tab "Leads").
 * This is the ONLY lead backend for medicalbillingteam.com (Supabase was dropped on 2026-10-18).
 * Deploy: _build/apps-script/DEPLOY.md (one step, done by Tony as tony@altfunding.com).
 *
 * - Stores non-PHI practice-level fields only (the 20 columns below = the sheet's header row).
 * - Rejects anything that looks like patient data (DOB-like dates, long ID-like numbers) in the free-text fields.
 * - Honeypot, minimum time-to-submit, form-key check, light rate limits, formula-injection guard.
 * - Alert email goes ONLY to tony@altfunding.com. Never for test rows.
 * - FORM_KEY is PUBLIC (it ships in the site's form-config.js). It only filters casual junk; it is not a secret.
 */
var SHEET_NAME = 'Leads';
var ALERT_ENABLED = true;
var ALERT_TO = 'tony@altfunding.com';            // never anyone else
var FORM_KEY = 'mbt-public-v1';                  // PUBLIC value, must match _build/config.json form_backend.form_key
var MIN_ELAPSED_MS = 3000;
var RATE_GLOBAL_PER_10MIN = 30;                  // all submissions, all visitors
var RATE_EMAIL_WINDOW_S = 120;                   // same work_email at most once per 2 minutes

var FIELDS = ['received_at','form_id','name','role','practice_name','specialty','num_providers','monthly_collections',
  'billing_setup','help_areas','work_email','phone','tcpa_consent','tcpa_text_version','source_page','utm','user_agent',
  'elapsed_ms','is_test','status'];
var ALLOWED_FORMS = { hero: 1, full: 1, footer: 1, checklist: 1 };
// Allowed select values (mirror _build/config.json "form"). Anything else is stored blank.
var ENUMS = {
  role: ['Practice owner / physician','Practice administrator or office manager','Billing or RCM manager','Billing company owner or manager','Other'],
  specialty: ['Primary care','Behavioral health / mental health','Substance use treatment center','Physical / occupational therapy','Chiropractic','Laboratory','Ambulatory surgery center','Multi-specialty','Medical billing company','Other'],
  num_providers: ['1','2-5','6-15','16-50','50+',"I'm a billing company"],
  monthly_collections: ['Under $50k','$50k-$150k','$150k-$500k','$500k-$1M','Over $1M','Prefer not to say'],
  billing_setup: ['In-house staff','Outsourced to a billing company','Mix of in-house and outsourced','We are a billing company','Other'],
  help_areas: ['Billing / claims','A/R follow-up','Eligibility / VOB','Prior authorization','Payment posting','Denial follow-up','Admissions / intake','Coding','Credentialing','Not sure yet']
};
var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
var PHONE_RE = /^[0-9()+.\- ]{7,30}$/;
var PHI_RE = /\b(0?[1-9]|1[0-2])[\/\-](0?[1-9]|[12]\d|3[01])[\/\-](19|20)\d{2}\b|\b\d{9,}\b/;

function doPost(e) {
  var r = handle_(e && e.parameter ? e.parameter : {}, deps_());
  return ContentService.createTextOutput(JSON.stringify(r)).setMimeType(ContentService.MimeType.JSON);
}
function doGet() { return ContentService.createTextOutput('ok'); }

/** Pure-ish core so it can be unit-tested outside Apps Script (see _build/apps-script/test_code.js). */
function handle_(p, d) {
  try {
    if (str_(p.company_website)) return { ok: true };                       // honeypot: pretend success, store nothing
    if (str_(p.form_key) !== FORM_KEY) return { ok: false, error: 'bad_request' };
    if (!ALLOWED_FORMS[str_(p.form_id)]) return { ok: false, error: 'bad_request' };
    if (Number(p.elapsed_ms || 0) < MIN_ELAPSED_MS) return { ok: true };     // too fast = bot; drop quietly
    var lead = clean_(p);
    if (!lead.name || !lead.practice_name || !EMAIL_RE.test(lead.work_email) || (lead.form_id !== 'checklist' && !lead.num_providers))
      return { ok: false, error: 'missing_fields' };
    if (PHI_RE.test(lead.name + ' ' + lead.practice_name)) return { ok: false, error: 'possible_phi' };
    if (!d.rateOk(lead.work_email)) return { ok: false, error: 'rate_limited' };
    var row = FIELDS.map(function (k) {
      if (k === 'received_at') return d.now();
      if (k === 'status') return 'new';
      var v = lead[k] == null ? '' : String(lead[k]);
      return /^[=+\-@\t\r]/.test(v) ? "'" + v : v;                             // block spreadsheet formula injection
    });
    d.append(row);
    if (ALERT_ENABLED && !lead.is_test) d.mail(ALERT_TO, 'New MedicalBillingTeam lead (' + lead.form_id + ')', alertBody_(lead, d.sheetUrl()));
    return { ok: true };
  } catch (err) {
    console.error(err);
    return { ok: false, error: 'server_error' };
  }
}

function clean_(p) {
  var o = {};
  o.form_id = str_(p.form_id);
  o.name = str_(p.name).slice(0, 100);
  o.practice_name = str_(p.practice_name).slice(0, 150);
  o.work_email = str_(p.work_email).toLowerCase().slice(0, 150);
  o.phone = PHONE_RE.test(str_(p.phone)) ? str_(p.phone) : '';
  ['role','specialty','num_providers','monthly_collections','billing_setup'].forEach(function (k) {
    o[k] = ENUMS[k].indexOf(str_(p[k])) >= 0 ? str_(p[k]) : '';
  });
  var ha = [];
  try { ha = JSON.parse(p.help_areas || '[]'); } catch (x) { ha = []; }
  o.help_areas = (Array.isArray(ha) ? ha : []).filter(function (x) { return ENUMS.help_areas.indexOf(x) >= 0; }).join('; ');
  o.tcpa_consent = str_(p.tcpa_consent) === 'true' && !!o.phone;
  o.tcpa_text_version = o.tcpa_consent ? str_(p.tcpa_text_version).slice(0, 40) : '';
  o.source_page = str_(p.source_page).slice(0, 500);
  var u = {};
  try { var uo = JSON.parse(p.utm || '{}'); ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid'].forEach(function (k) { if (uo && uo[k]) u[k] = String(uo[k]).slice(0, 120); }); } catch (x) {}
  o.utm = Object.keys(u).length ? JSON.stringify(u) : '';
  o.user_agent = str_(p.user_agent).slice(0, 300);
  o.elapsed_ms = Math.max(0, Math.min(Number(p.elapsed_ms) || 0, 86400000));
  o.is_test = str_(p.is_test) === 'true';
  return o;
}

function alertBody_(l, url) {
  return ['A new lead was added to the MedicalBillingTeam Leads sheet.', '',
    'Form: ' + l.form_id, 'Name: ' + l.name, 'Practice/company: ' + l.practice_name, 'Role: ' + (l.role || '-'),
    'Specialty: ' + (l.specialty || '-'), 'Providers: ' + (l.num_providers || '-'), 'Work email: ' + l.work_email,
    'Phone: ' + (l.phone || '-') + (l.tcpa_consent ? ' (call/text consent given)' : ''), 'Page: ' + l.source_page, '',
    'Sheet: ' + url, '', 'Practice-level details only; the site never collects patient information.'].join('\n');
}

function str_(v) { return v == null ? '' : String(v).trim(); }

function deps_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var cache = CacheService.getScriptCache();
  return {
    now: function () { return new Date(); },
    sheetUrl: function () { return ss.getUrl(); },
    rateOk: function (email) {
      var lock = LockService.getScriptLock(); lock.waitLock(10000);
      try {
        var ek = 'e:' + Utilities.base64EncodeWebSafe(email).slice(0, 200);
        if (cache.get(ek)) return false;
        var bucket = 'g:' + Math.floor(Date.now() / 600000);
        var n = Number(cache.get(bucket) || 0);
        if (n >= RATE_GLOBAL_PER_10MIN) return false;
        cache.put(bucket, String(n + 1), 700);
        cache.put(ek, '1', RATE_EMAIL_WINDOW_S);
        return true;
      } finally { lock.releaseLock(); }
    },
    append: function (row) {
      var lock = LockService.getScriptLock(); lock.waitLock(10000);
      try {
        var sh = ss.getSheetByName(SHEET_NAME);
        if (sh.getLastRow() === 0) sh.appendRow(FIELDS);
        sh.appendRow(row);
      } finally { lock.releaseLock(); }
    },
    mail: function (to, subject, body) { MailApp.sendEmail({ to: to, subject: subject, body: body, name: 'MedicalBillingTeam.com' }); }
  };
}
