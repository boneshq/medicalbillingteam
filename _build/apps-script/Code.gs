/**
 * MedicalBillingTeam Leads — Apps Script web app bound to the "MedicalBillingTeam Leads" Sheet
 * (https://docs.google.com/spreadsheets/d/1-6vsIf2-g_eHqXTy3Wb2JEEPIy7mfPEE-EYjTnXXVM4/edit, tab "Leads").
 * Alternative backend to Supabase. Free. Deploy steps: _build/apps-script/DEPLOY.md.
 * Non-PHI fields only. Optional alert goes ONLY to tony@altfunding.com (off by default).
 */
var SHEET_NAME = 'Leads';
var ALERT_ENABLED = false;              // flip to true only with Tony's okay
var ALERT_TO = 'tony@altfunding.com';   // never AGS staff
var MIN_ELAPSED_MS = 3000;
var FIELDS = ['received_at','form_id','name','role','practice_name','specialty','num_providers','monthly_collections',
  'billing_setup','help_areas','work_email','phone','tcpa_consent','tcpa_text_version','source_page','utm','user_agent',
  'elapsed_ms','is_test','status'];
var ALLOWED_FORMS = { hero: 1, full: 1, footer: 1, checklist: 1 };

function doPost(e) {
  var p = (e && e.parameter) || {};
  try {
    if (p.company_website) return ok_();                                   // honeypot
    if (!ALLOWED_FORMS[p.form_id]) return ok_();
    if (Number(p.elapsed_ms || 0) < MIN_ELAPSED_MS) return ok_();          // too fast = bot
    if (!p.name || !p.practice_name || !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(p.work_email || '')) return ok_();
    if (p.phone && !/^[0-9()+.\- ]{7,30}$/.test(p.phone)) p.phone = '';
    var lock = LockService.getScriptLock(); lock.waitLock(10000);
    try {
      var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
      if (sh.getLastRow() === 0) sh.appendRow(FIELDS);
      var row = FIELDS.map(function (k) {
        if (k === 'received_at') return new Date();
        if (k === 'status') return 'new';
        var v = String(p[k] == null ? '' : p[k]).slice(0, 500);
        return /^[=+\-@]/.test(v) ? "'" + v : v;                             // block formula injection
      });
      sh.appendRow(row);
    } finally { lock.releaseLock(); }
    var isTest = String(p.is_test) === 'true';
    if (ALERT_ENABLED && !isTest) {
      MailApp.sendEmail(ALERT_TO, 'New MedicalBillingTeam lead (' + p.form_id + ')',
        'A new lead was added to the MedicalBillingTeam Leads sheet. Open the sheet to view it.\n' +
        SpreadsheetApp.getActiveSpreadsheet().getUrl());                    // no lead details in the email body
    }
  } catch (err) { console.error(err); }
  return ok_();
}
function doGet() { return ContentService.createTextOutput('ok'); }
function ok_() { return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON); }
