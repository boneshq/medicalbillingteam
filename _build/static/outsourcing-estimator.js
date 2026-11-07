/* AGS staffing budget estimator. Public aggregate rates only; no invoice or client data. */
(function (factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (typeof document !== 'undefined' && typeof window !== 'undefined') {
    var start = function () { api.mount(document, window); };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
    else start();
  }
})(function () {
  'use strict';
  var formatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function finite(value, fallback) {
    if (value === null || value === undefined || value === '' || typeof value === 'boolean') return fallback;
    var n = Number(value);
    return Number.isFinite(n) ? n : fallback;
  }

  function validRole(role) {
    if (!role || !/^[a-z][a-z0-9-]{0,59}$/.test(role.id || '') || typeof role.label !== 'string' || !role.label.trim()) return false;
    if (role.quote_only === true) return true;
    return role.unit === 'hour' && typeof role.rate_min === 'number' && typeof role.rate_max === 'number' &&
      Number.isFinite(role.rate_min) && Number.isFinite(role.rate_max) && role.rate_min > 0 && role.rate_max >= role.rate_min;
  }

  function rolesFor(data) {
    if (!data || data.currency !== 'USD' || Number(data.weeks_per_year === undefined ? 52 : data.weeks_per_year) !== 52 || Number(data.months_per_year === undefined ? 12 : data.months_per_year) !== 12 || !Array.isArray(data.roles)) {
      throw new Error('Unsupported pricing data');
    }
    var ids = new Set();
    data.roles.forEach(function (role) {
      if (!validRole(role) || ids.has(role.id)) throw new Error('Invalid pricing role');
      ids.add(role.id);
    });
    if (!data.roles.length) throw new Error('No pricing roles');
    return data.roles;
  }

  function normalizeInputs(data, input) {
    input = input || {};
    var roles = rolesFor(data);
    var first = roles.find(function (role) { return !role.quote_only; }) || roles[0];
    var role = roles.find(function (item) { return item.id === input.role; }) || first;
    var count = Math.min(100, Math.max(1, Math.trunc(finite(input.n, 1))));
    var defaultHours = Math.min(40, Math.max(1, finite(data.hours_per_week, 40)));
    var hours = Math.min(40, Math.max(1, finite(input.hours, defaultHours)));
    hours = Math.round(hours * 100) / 100;
    return { role: role.id, n: count, hours: hours };
  }

  function total(rate, hundredthHours, count, weeks, months) {
    // Integer cents and hundredths of hours avoid binary half-cent errors.
    return Math.round(Math.round(rate * 100) * hundredthHours * count * weeks / (100 * months)) / 100;
  }

  function calculate(data, input) {
    var state = normalizeInputs(data, input);
    var role = data.roles.find(function (item) { return item.id === state.role; });
    var result = { state: state, label: role.label, note: role.note || '', quoteOnly: role.quote_only === true };
    if (result.quoteOnly) return result;
    var hundredthHours = Math.round(state.hours * 100);
    result.hourly = { min: role.rate_min, max: role.rate_max };
    result.weekly = { min: total(role.rate_min, hundredthHours, state.n, 1, 1), max: total(role.rate_max, hundredthHours, state.n, 1, 1) };
    // Calculate monthly from unrounded hourly totals, not the displayed weekly amount.
    result.monthly = { min: total(role.rate_min, hundredthHours, state.n, 52, 12), max: total(role.rate_max, hundredthHours, state.n, 52, 12) };
    return result;
  }

  function moneyRange(range) {
    return formatter.format(range.min) + (range.max === range.min ? '' : '–' + formatter.format(range.max));
  }

  function buildScenarioUrl(baseUrl, state, asOf) {
    var url = new URL(baseUrl);
    var test = url.searchParams.get('mbt_test') === '1';
    url.search = '';
    url.hash = '';
    url.searchParams.set('role', state.role);
    url.searchParams.set('n', String(state.n));
    url.searchParams.set('hours', String(state.hours));
    if (/^\d{4}-\d{2}-\d{2}$/.test(asOf || '')) url.searchParams.set('pricing_as_of', asOf);
    if (test) url.searchParams.set('mbt_test', '1');
    var result = url.toString();
    if (result.length > 500) throw new Error('Scenario URL exceeds lead-source limit');
    return result;
  }

  function mount(doc, win) {
    var container = doc.getElementById('outsourcing-estimator');
    var payload = doc.getElementById('outsourcing-estimator-data');
    if (!container || !payload || container.dataset.ready === '1') return;
    var data;
    try { data = JSON.parse(payload.textContent); rolesFor(data); }
    catch (error) { return; } // The server-rendered table and quote CTA remain available.
    var roleInput = doc.getElementById('oe-role');
    var countInput = doc.getElementById('oe-count');
    var hoursInput = doc.getElementById('oe-hours');
    var resultNode = doc.getElementById('oe-result');
    var noteNode = doc.getElementById('oe-role-note');
    if (!roleInput || !countInput || !hoursInput || !resultNode || !noteNode) return;
    container.dataset.ready = '1';
    var params = new URLSearchParams(win.location.search);
    var initial = normalizeInputs(data, { role: params.get('role'), n: params.get('n'), hours: params.get('hours') });
    roleInput.value = initial.role; countInput.value = initial.n; hoursInput.value = initial.hours;

    function render(normalizeFields) {
      var result = calculate(data, { role: roleInput.value, n: countInput.value, hours: hoursInput.value });
      var state = result.state;
      // Preserve unfinished input while typing; normalize on commitment or quote capture.
      if (normalizeFields) {
        roleInput.value = state.role; countInput.value = state.n; hoursInput.value = state.hours;
      }
      noteNode.textContent = result.note;
      resultNode.replaceChildren();
      var heading = doc.createElement('p');
      var strong = doc.createElement('strong');
      heading.appendChild(strong);
      resultNode.appendChild(heading);
      var detail = doc.createElement('p');
      if (result.quoteOnly) {
        strong.textContent = result.label + ': scoped quote required';
        detail.textContent = 'Ask AGS to price this role for your workload, schedule and required experience. No numerical estimate is available for this role.';
      } else {
        strong.textContent = result.label + ': ' + moneyRange(result.monthly) + ' per average month';
        detail.textContent = state.n + (state.n === 1 ? ' staff member' : ' staff members') + ' × ' + state.hours +
          ' hours/week. Weekly budget: ' + moneyRange(result.weekly) + '. Hourly range: ' + moneyRange(result.hourly) + ' per person.';
      }
      resultNode.appendChild(detail);
      var footer = doc.getElementById('form-footer');
      if (footer) {
        try { footer.dataset.source = buildScenarioUrl(win.location.href, state, data.as_of); }
        catch (error) { delete footer.dataset.source; }
      }
    }
    [countInput, hoursInput].forEach(function (input) {
      input.addEventListener('input', function () { render(false); });
    });
    [roleInput, countInput, hoursInput].forEach(function (input) {
      input.addEventListener('change', function () { render(true); });
    });
    var quoteLink = doc.getElementById('oe-quote');
    if (quoteLink) quoteLink.addEventListener('click', function () { render(true); });
    render(true);
  }

  return { normalizeInputs: normalizeInputs, calculate: calculate, moneyRange: moneyRange, buildScenarioUrl: buildScenarioUrl, mount: mount };
});
