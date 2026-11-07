/* Synthetic fixtures test arithmetic; these values are not AGS prices. No network requests. */
'use strict';
const assert = require('node:assert/strict');
const path = require('node:path');
const api = require(path.join(__dirname, '../_build/static/outsourcing-estimator.js'));
const fixture = {
  currency: 'USD', as_of: '2026-11-07', hours_per_week: 40, weeks_per_year: 52, months_per_year: 12,
  roles: [
    { id: 'synthetic-hourly', label: 'Synthetic hourly fixture', unit: 'hour', rate_min: 10.25, rate_max: 15.75, note: 'Not a public price' },
    { id: 'synthetic-quote', label: 'Synthetic quote-only fixture', quote_only: true }
  ]
};
let checks = 0;
function test(name, fn) { fn(); checks++; process.stdout.write('PASS ' + name + '\n'); }
test('Hourly ranges use staff count and 52/12 average months', () => {
  const result = api.calculate(fixture, { role: 'synthetic-hourly', n: 2, hours: 40 });
  assert.deepEqual(result.weekly, { min: 820, max: 1260 });
  assert.deepEqual(result.monthly, { min: 3553.33, max: 5460 });
});
test('Fractional hours retain cents and do not round the weekly intermediary', () => {
  const result = api.calculate(fixture, { role: 'synthetic-hourly', n: 1, hours: 37.5 });
  assert.deepEqual(result.weekly, { min: 384.38, max: 590.63 });
  assert.deepEqual(result.monthly, { min: 1665.63, max: 2559.38 });
});
test('Exact half-cent totals round up consistently with the server renderer', () => {
  const data = { ...fixture, roles: [{ ...fixture.roles[0], rate_min: 1.13, rate_max: 2.01 }] };
  assert.equal(api.calculate(data, { hours: 17.5 }).weekly.min, 19.78);
  assert.equal(api.calculate(data, { hours: 1.5 }).weekly.max, 3.02);
});
test('Missing and invalid params use valid defaults; unknown role cannot inject a price', () => {
  assert.deepEqual(api.normalizeInputs(fixture, { role: '__proto__', n: '', hours: 'Infinity' }), { role: 'synthetic-hourly', n: 1, hours: 40 });
  assert.deepEqual(api.normalizeInputs(fixture, { role: 'bogus', n: '1e999', hours: '<script>' }), { role: 'synthetic-hourly', n: 1, hours: 40 });
});
test('Headcount/hours clamp to documented bounds and headcount is integral', () => {
  assert.deepEqual(api.normalizeInputs(fixture, { n: '101', hours: '99' }), { role: 'synthetic-hourly', n: 100, hours: 40 });
  assert.deepEqual(api.normalizeInputs(fixture, { n: '-20', hours: '-5' }), { role: 'synthetic-hourly', n: 1, hours: 1 });
  assert.deepEqual(api.normalizeInputs(fixture, { n: '2.9', hours: '25.5' }), { role: 'synthetic-hourly', n: 2, hours: 25.5 });
  assert.deepEqual(api.normalizeInputs(fixture, { hours: '37.555' }), { role: 'synthetic-hourly', n: 1, hours: 37.56 });
});
test('Quote-only roles never acquire a numeric result', () => {
  const result = api.calculate(fixture, { role: 'synthetic-quote', n: 5, hours: 20 });
  assert.equal(result.quoteOnly, true);
  assert.equal(result.monthly, undefined);
  assert.equal(result.weekly, undefined);
  assert.equal(result.hourly, undefined);
});
test('Scenario URL preserves test mode and captures only approved scenario fields', () => {
  const state = api.normalizeInputs(fixture, { n: 2, hours: 37.5 });
  const url = new URL(api.buildScenarioUrl('https://medicalbillingteam.com/pricing/?mbt_test=1&work_email=private%40example.invalid&utm_source=test#footer-cta', state, fixture.as_of));
  assert.equal(url.pathname, '/pricing/');
  assert.equal(url.searchParams.get('mbt_test'), '1');
  assert.equal(url.searchParams.get('pricing_as_of'), '2026-11-07');
  assert.equal(url.searchParams.get('n'), '2');
  assert.equal(url.searchParams.get('hours'), '37.5');
  assert.equal(url.searchParams.has('work_email'), false);
  assert.equal(url.searchParams.has('utm_source'), false);
  assert.equal(url.hash, '');
  assert.ok(url.toString().length < 500);
  assert.deepEqual(api.normalizeInputs(fixture, Object.fromEntries(url.searchParams)), state);
});
test('Inverted, negative, nonfinite and non-hourly rates fail closed', () => {
  for (const change of [{ rate_min: -1 }, { rate_min: 100 }, { rate_max: Infinity }, { unit: 'month' }]) {
    const bad = { ...fixture, roles: [{ ...fixture.roles[0], ...change }] };
    assert.throws(() => api.calculate(bad, {}), /Invalid pricing role/);
  }
  assert.throws(() => api.calculate({ ...fixture, currency: 'PHP' }, {}), /Unsupported pricing data/);
  assert.throws(() => api.calculate({ ...fixture, weeks_per_year: 0 }, {}), /Unsupported pricing data/);
  assert.throws(() => api.calculate({ ...fixture, months_per_year: 0 }, {}), /Unsupported pricing data/);
  assert.throws(() => api.calculate({ ...fixture, roles: [] }, {}), /No pricing roles/);
});
test('Formatting retains cents and equal rates do not imply a spread', () => {
  assert.equal(api.moneyRange({ min: 10.25, max: 15.75 }), '$10.25–$15.75');
  assert.equal(api.moneyRange({ min: 10.25, max: 10.25 }), '$10.25');
});
function mountedFixture() {
  function element() {
    return {
      value: '', dataset: {}, textContent: '', children: [], listeners: {},
      replaceChildren() { this.children = []; },
      appendChild(child) { this.children.push(child); },
      addEventListener(type, listener) { (this.listeners[type] ||= []).push(listener); },
      dispatch(type) { (this.listeners[type] || []).forEach(listener => listener()); }
    };
  }
  const nodes = Object.fromEntries(['outsourcing-estimator', 'outsourcing-estimator-data', 'oe-role', 'oe-count',
    'oe-hours', 'oe-result', 'oe-role-note', 'oe-quote', 'form-footer'].map(id => [id, element()]));
  nodes['outsourcing-estimator-data'].textContent = JSON.stringify(fixture);
  api.mount({ getElementById: id => nodes[id], createElement: element },
    { location: { search: '?mbt_test=1', href: 'https://medicalbillingteam.com/pricing/?mbt_test=1' } });
  return nodes;
}
test('Typing updates the result and quote scenario without rewriting unfinished fields', () => {
  const nodes = mountedFixture();
  nodes['oe-count'].value = '3';
  nodes['oe-count'].dispatch('input');
  nodes['oe-hours'].value = '20';
  nodes['oe-hours'].dispatch('input');
  assert.match(nodes['oe-result'].children[1].textContent, /3 staff members × 20 hours\/week/);
  assert.match(nodes['oe-result'].children[1].textContent, /\$615\.00–\$945\.00/);
  assert.equal(new URL(nodes['form-footer'].dataset.source).searchParams.get('hours'), '20');
  nodes['oe-count'].value = '';
  nodes['oe-count'].dispatch('input');
  assert.equal(nodes['oe-count'].value, '');
  nodes['oe-count'].value = '1000';
  nodes['oe-count'].dispatch('input');
  assert.equal(nodes['oe-count'].value, '1000');
  assert.equal(new URL(nodes['form-footer'].dataset.source).searchParams.get('n'), '100');
  nodes['oe-count'].dispatch('change');
  assert.equal(String(nodes['oe-count'].value), '100');
});
test('Quote click refreshes captured values even if a field has not fired change', () => {
  const nodes = mountedFixture();
  nodes['oe-count'].value = '2.9';
  nodes['oe-hours'].value = '37.555';
  nodes['oe-quote'].dispatch('click');
  assert.equal(String(nodes['oe-count'].value), '2');
  assert.equal(String(nodes['oe-hours'].value), '37.56');
  const params = new URL(nodes['form-footer'].dataset.source).searchParams;
  assert.equal(params.get('n'), '2');
  assert.equal(params.get('hours'), '37.56');
  assert.equal(params.get('mbt_test'), '1');
  nodes['oe-role'].value = 'synthetic-quote';
  nodes['oe-role'].dispatch('change');
  assert.match(nodes['oe-result'].children[0].children[0].textContent, /scoped quote required/);
  assert.doesNotMatch(nodes['oe-result'].children[1].textContent, /\$/);
});
process.stdout.write('outsourcing-estimator: ' + checks + ' checks passed\n');
