// Local unit test for Code.gs (no Google services). Run: node _build/apps-script/test_code.js
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const ctx = { console, JSON, Date, Math, Number, String, Array, Object };
vm.createContext(ctx); vm.runInContext(fs.readFileSync(__dirname + '/Code.gs', 'utf8'), ctx);
function deps(opts = {}) {
  const d = { rows: [], mails: [], seen: {}, count: 0,
    now: () => 'NOW', sheetUrl: () => 'https://docs.google.com/spreadsheets/d/SHEET/edit',
    rateOk(e) { if (d.seen[e] || d.count >= (opts.max || 30)) return false; d.seen[e] = 1; d.count++; return true; },
    append(r) { d.rows.push(r); }, mail(to, s, b) { d.mails.push({ to, s, b }); } };
  return d;
}
const base = { form_key: 'mbt-public-v1', form_id: 'hero', name: 'Jane Doe', practice_name: 'Acme Family Medicine', num_providers: '2-5',
  work_email: 'Jane@AcmeFM.com', phone: '', elapsed_ms: '9000', company_website: '', is_test: 'false', help_areas: '[]', utm: '{}',
  source_page: 'https://boneshq.github.io/medicalbillingteam/', user_agent: 'UA', tcpa_consent: 'false' };
let t = 0; const T = (name, fn) => { fn(); t++; console.log('PASS', name); };
T('valid hero lead appends 20-col row + 1 alert to tony@ only', () => { const d = deps(); const r = ctx.handle_({ ...base }, d);
  assert.deepStrictEqual(JSON.parse(JSON.stringify(r)), { ok: true }); assert.equal(d.rows.length, 1); assert.equal(d.rows[0].length, 20);
  assert.equal(d.rows[0][10], 'jane@acmefm.com'); assert.equal(d.rows[0][19], 'new'); assert.equal(d.mails.length, 1);
  assert.equal(d.mails[0].to, 'tony@altfunding.com'); });
T('header order matches sheet', () => assert.equal(Array.from(ctx.FIELDS).join(','), 'received_at,form_id,name,role,practice_name,specialty,num_providers,monthly_collections,billing_setup,help_areas,work_email,phone,tcpa_consent,tcpa_text_version,source_page,utm,user_agent,elapsed_ms,is_test,status'));
T('honeypot -> ok, nothing stored', () => { const d = deps(); assert.equal(ctx.handle_({ ...base, company_website: 'x.com' }, d).ok, true); assert.equal(d.rows.length, 0); assert.equal(d.mails.length, 0); });
T('too fast -> dropped', () => { const d = deps(); ctx.handle_({ ...base, elapsed_ms: '500' }, d); assert.equal(d.rows.length, 0); });
T('wrong form key -> rejected', () => { const d = deps(); assert.equal(ctx.handle_({ ...base, form_key: 'nope' }, d).ok, false); assert.equal(d.rows.length, 0); });
T('unknown form_id -> rejected', () => { const d = deps(); assert.equal(ctx.handle_({ ...base, form_id: 'evil' }, d).ok, false); });
T('missing email -> missing_fields', () => { const d = deps(); assert.equal(ctx.handle_({ ...base, work_email: 'bad' }, d).error, 'missing_fields'); });
T('PHI-like DOB in name -> rejected', () => { const d = deps(); assert.equal(ctx.handle_({ ...base, name: 'John 04/12/1961' }, d).error, 'possible_phi'); assert.equal(d.rows.length, 0); });
T('PHI-like member id -> rejected', () => { const d = deps(); assert.equal(ctx.handle_({ ...base, practice_name: 'ID 123456789' }, d).error, 'possible_phi'); });
T('formula injection neutralised', () => { const d = deps(); ctx.handle_({ ...base, name: '=HYPERLINK("x")' }, d); assert.equal(d.rows[0][2], "'=HYPERLINK(\"x\")"); });
T('enum outside list stored blank; help_areas filtered', () => { const d = deps(); ctx.handle_({ ...base, form_id: 'full', role: 'Hacker', specialty: 'Chiropractic', help_areas: JSON.stringify(['Coding', 'DROP TABLE']) }, d);
  assert.equal(d.rows[0][3], ''); assert.equal(d.rows[0][5], 'Chiropractic'); assert.equal(d.rows[0][9], 'Coding'); });
T('tcpa only counts with a valid phone', () => { const d = deps(); ctx.handle_({ ...base, tcpa_consent: 'true', tcpa_text_version: 'v1' }, d); assert.equal(d.rows[0][12], 'false');
  const d2 = deps(); ctx.handle_({ ...base, phone: '(555) 010-2000', tcpa_consent: 'true', tcpa_text_version: '2026-10-18-v1' }, d2); assert.equal(d2.rows[0][12], 'true'); assert.equal(d2.rows[0][13], '2026-10-18-v1'); });
T('test rows stored but no alert', () => { const d = deps(); ctx.handle_({ ...base, is_test: 'true' }, d); assert.equal(d.rows.length, 1); assert.equal(d.mails.length, 0); });
T('rate limit: same email twice -> second rejected', () => { const d = deps(); ctx.handle_({ ...base }, d); assert.equal(ctx.handle_({ ...base }, d).error, 'rate_limited'); assert.equal(d.rows.length, 1); });
T('rate limit: global cap', () => { const d = deps({ max: 2 }); ['a@x.com', 'b@x.com', 'c@x.com'].forEach(e => ctx.handle_({ ...base, work_email: e }, d)); assert.equal(d.rows.length, 2); });
T('checklist form needs no provider count', () => { const d = deps(); assert.equal(ctx.handle_({ ...base, form_id: 'checklist', num_providers: '' }, d).ok, true); });
T('backend throw -> server_error, not silent ok', () => { const d = deps(); d.append = () => { throw new Error('x'); }; assert.equal(ctx.handle_({ ...base }, d).error, 'server_error'); });
T('alert body has no free text beyond fields', () => { const d = deps(); ctx.handle_({ ...base }, d); assert.ok(!/patient name|DOB/i.test(d.mails[0].b)); });
console.log(`\n${t} tests passed`);
