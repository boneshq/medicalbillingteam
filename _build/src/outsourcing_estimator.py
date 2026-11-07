"""Render public, aggregate AGS pricing data; never read private invoice evidence."""
import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import html
import json
import re


def _number(value, name):
    if isinstance(value, bool):
        raise ValueError(f'{name} must be a number')
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f'{name} must be a finite number') from None
    if not number.is_finite():
        raise ValueError(f'{name} must be a finite number')
    return number


def normalize_data(data):
    """Whitelist the public contract and fail the build on unusable pricing."""
    if data.get('currency') != 'USD':
        raise ValueError('Outsourcing estimator supports USD only')
    as_of = str(data.get('as_of', ''))
    datetime.date.fromisoformat(as_of)
    weeks = _number(data.get('weeks_per_year', 52), 'weeks_per_year')
    months = _number(data.get('months_per_year', 12), 'months_per_year')
    if weeks != 52 or months != 12:
        raise ValueError('Monthly budget uses 52 weeks / 12 months')
    hours = _number(data.get('hours_per_week', 40), 'hours_per_week')
    if not 1 <= hours <= 40:
        raise ValueError('Default hours_per_week must be between 1 and 40')
    if hours != hours.quantize(Decimal('0.01')):
        raise ValueError('Default hours_per_week must use at most two decimal places')
    result = {
        'currency': 'USD', 'as_of': as_of,
        'observation_period': str(data.get('observation_period', '')).strip(),
        'source_note': str(data.get('source_note', '')).strip(),
        'hours_per_week': float(hours), 'weeks_per_year': 52, 'months_per_year': 12,
        'roles': [],
    }
    if not result['observation_period'] or not result['source_note']:
        raise ValueError('Public observation_period and source_note are required')
    seen = set()
    for item in data.get('roles', []):
        role_id = str(item.get('id', ''))
        label = str(item.get('label', '')).strip()
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,59}', role_id) or role_id in seen or not label:
            raise ValueError('Roles require a unique slug id and nonempty label')
        seen.add(role_id)
        role = {'id': role_id, 'label': label, 'note': str(item.get('note', '')).strip()}
        if item.get('quote_only') is True:
            role['quote_only'] = True
        else:
            if item.get('unit') != 'hour':
                raise ValueError(f'{role_id}: only hourly rates or quote_only are supported')
            low = _number(item.get('rate_min'), f'{role_id}.rate_min')
            high = _number(item.get('rate_max'), f'{role_id}.rate_max')
            if low <= 0 or high < low:
                raise ValueError(f'{role_id}: require 0 < rate_min <= rate_max')
            if low != low.quantize(Decimal('0.01')) or high != high.quantize(Decimal('0.01')):
                raise ValueError(f'{role_id}: hourly rates must use at most two decimal places')
            role.update(unit='hour', rate_min=float(low), rate_max=float(high), quote_only=False)
        result['roles'].append(role)
    if not result['roles']:
        raise ValueError('At least one priced or quote-only role is required')
    return result


def _money(value):
    rounded = Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return f'${rounded:,.2f}'


def _range(low, high):
    return _money(low) if low == high else _money(low) + '–' + _money(high)


def _monthly(role, hours):
    factor = Decimal(str(hours)) * Decimal(52) / Decimal(12)
    return _range(Decimal(str(role['rate_min'])) * factor,
                  Decimal(str(role['rate_max'])) * factor)


def render_estimator(data):
    data = normalize_data(data)
    esc = lambda value: html.escape(str(value), quote=True)
    default = next((r for r in data['roles'] if not r.get('quote_only')), data['roles'][0])
    hours = Decimal(str(data['hours_per_week']))
    hours_label = format(hours.normalize(), 'f')
    rows = []
    options = []
    for role in data['roles']:
        options.append(f'<option value="{esc(role["id"])}"' + (' selected' if role['id'] == default['id'] else '') + f'>{esc(role["label"])}</option>')
        if role.get('quote_only'):
            rate, monthly = 'Scoped quote required', 'Contact AGS'
        else:
            rate = _range(role['rate_min'], role['rate_max']) + ' / hour'
            monthly = _monthly(role, hours)
        rows.append(f'<tr><th scope="row">{esc(role["label"])}</th><td>{esc(rate)}</td><td>{esc(monthly)}</td><td>{esc(role["note"])}</td></tr>')
    if default.get('quote_only'):
        initial = '<p><strong>Scoped quote required.</strong> Ask AGS to price this role for your workload, schedule and required experience.</p>'
    else:
        weekly = _range(Decimal(str(default['rate_min'])) * hours, Decimal(str(default['rate_max'])) * hours)
        initial = (f'<p><strong>{esc(default["label"])}: {_monthly(default, hours)} per average month</strong></p>'
                   f'<p>1 staff member × {hours_label} hours/week. Weekly budget: {weekly}. '
                   f'Hourly range: {_range(default["rate_min"], default["rate_max"])} per person.</p>')
    payload = json.dumps(data, ensure_ascii=True, separators=(',', ':')).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return f'''<section id="outsourcing-estimator" aria-labelledby="oe-title">
<h3 id="oe-title">Estimate your AGS staffing budget</h3>
<div class="calc">
<div class="calc-grid">
<label for="oe-role">Position<select id="oe-role" aria-describedby="oe-role-note">{''.join(options)}</select></label>
<label for="oe-count">Number of staff<input id="oe-count" type="number" min="1" max="100" step="1" value="1" inputmode="numeric" aria-describedby="oe-assumptions"></label>
<label for="oe-hours">Budgeted hours per person per week<input id="oe-hours" type="number" min="1" max="40" step="any" value="{hours_label}" inputmode="decimal" aria-describedby="oe-assumptions"></label>
</div>
<p id="oe-role-note" class="fine">{esc(default['note'])}</p>
<div class="calc-out" id="oe-result" role="status" aria-live="polite" aria-atomic="true">{initial}</div>
<p id="oe-assumptions" class="fig-src">Monthly budget = hourly rate × hours per week × 52 ÷ 12 × staff count. An average month has about 4.33 weeks; an actual invoice reflects its billing period and agreed terms. Changing hours models a budget scenario and does not confirm part-time availability, minimum engagement or staffing availability.</p>
<p class="fine"><strong>Budget estimate, not a binding quote.</strong> These historical billed ranges are not a guaranteed current rate or a market-wide benchmark. Role, experience, workload, coverage, contract terms and any separately agreed charges can change the final price. Confirm inclusions and the final scope with AGS.</p>
<p><a class="btn btn-cta" id="oe-quote" href="#footer-cta">Request an AGS staffing quote</a></p>
<noscript><p>The starting budget above and full rate table below are available without JavaScript. Enable JavaScript to change the scenario and submit a quote request.</p></noscript>
</div>
<h3>Hourly rates and monthly budget examples</h3>
<div class="table-wrap"><table><caption>AGS staffing budget ranges in USD; one person at {hours_label} hours/week for monthly examples</caption><thead><tr><th scope="col">Position</th><th scope="col">Hourly budget range</th><th scope="col">Average monthly budget</th><th scope="col">Scope and limitations</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="fig-src">Reviewed <time datetime="{esc(data['as_of'])}">{esc(data['as_of'])}</time>. Invoice observation period: {esc(data['observation_period'])}. {esc(data['source_note'])}</p>
<script type="application/json" id="outsourcing-estimator-data">{payload}</script>
</section>'''


def markdown_summary(data):
    data = normalize_data(data)
    clean = lambda text: str(text).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
    hours = data['hours_per_week']
    lines = ['### AGS staffing budget ranges', '',
             f'Currency: USD. Reviewed: {data["as_of"]}. Invoice observation period: {clean(data["observation_period"])}.',
             clean(data['source_note']), '',
             '| Position | Hourly budget range | Average monthly budget for one person | Scope and limitations |',
             '|---|---|---|---|']
    for role in data['roles']:
        rate = 'Scoped quote required' if role.get('quote_only') else _range(role['rate_min'], role['rate_max']) + ' / hour'
        monthly = 'Contact AGS' if role.get('quote_only') else _monthly(role, hours)
        lines.append('| ' + ' | '.join(clean(x) for x in (role['label'], rate, monthly, role['note'])) + ' |')
    lines += ['', f'Monthly examples use {hours:g} hours/week. Monthly budget = hourly rate × hours/week × 52 ÷ 12 × staff count. '
              'An average month has about 4.33 weeks; actual invoices reflect their billing periods and agreed terms. '
              'Hours are a budget scenario, not confirmation of part-time availability or minimum engagement.', '',
              'Budget estimate, not a binding quote. Historical billed ranges are not guaranteed current prices or a market-wide benchmark. '
              'Role, experience, workload, coverage, contract terms and separately agreed charges can change the final price. Confirm scope and inclusions with AGS.', '',
              '[Use the AGS staffing estimator or request a quote](/pricing/#outsourcing-estimator).']
    return '\n'.join(lines)
