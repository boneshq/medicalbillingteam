"""Synthetic fixtures only: no invoice evidence, public AGS prices or network calls."""
import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / '_build' / 'src' / 'outsourcing_estimator.py'
SPEC = importlib.util.spec_from_file_location('outsourcing_estimator', MODULE_PATH)
estimator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(estimator)


def fixture():
    return {
        'currency': 'USD', 'as_of': '2026-11-07',
        'observation_period': 'Synthetic test period',
        'source_note': 'Synthetic arithmetic fixtures; these are not AGS prices.',
        'hours_per_week': 40, 'weeks_per_year': 52, 'months_per_year': 12,
        'roles': [
            {'id': 'synthetic-hourly', 'label': 'Synthetic hourly fixture',
             'unit': 'hour', 'rate_min': 10.25, 'rate_max': 15.75, 'note': 'Synthetic scope'},
            {'id': 'synthetic-quote', 'label': 'Synthetic quote-only fixture',
             'quote_only': True, 'note': 'Scope requires review'},
        ],
    }


class Markup(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.by_id = {}
        self.labels = set()
        self.scripts = []
        self.script_data = []
        self.tags = []
        self.text = []
        self.in_script = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if 'id' in attrs:
            self.by_id[attrs['id']] = attrs
        if tag == 'label':
            self.labels.add(attrs.get('for'))
        if tag == 'script':
            self.scripts.append(attrs)
            self.in_script = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False

    def handle_data(self, text):
        (self.script_data if self.in_script else self.text).append(text)


class EstimatorTests(unittest.TestCase):
    def test_html_and_markdown_publish_equivalent_rates_methods_and_dates(self):
        data = fixture()
        markup = Markup(estimator.render_estimator(data))
        visible = ' '.join(markup.text)
        markdown = estimator.markdown_summary(data)
        for value in ('$10.25–$15.75 / hour', '$1,776.67–$2,730.00',
                      'Synthetic hourly fixture', 'Synthetic quote-only fixture',
                      'Scoped quote required', 'Contact AGS', data['as_of'],
                      data['observation_period'], data['source_note'],
                      '52 ÷ 12 × staff count', '4.33 weeks', 'not a binding quote'):
            with self.subTest(value=value):
                self.assertIn(value, visible)
                self.assertIn(value, markdown)
        self.assertIn('/pricing/#outsourcing-estimator', markdown)

    def test_fractional_hours_and_half_cents_match_server_rounding(self):
        data = fixture()
        data['hours_per_week'] = 37.5
        for output in (estimator.render_estimator(data), estimator.markdown_summary(data)):
            self.assertIn('$1,665.63–$2,559.38', output)
            self.assertIn('37.5 hours/week', output)
        data['hours_per_week'] = 17.5
        data['roles'][0].update(rate_min=1.13, rate_max=1.13)
        self.assertIn('Weekly budget: $19.78.', estimator.render_estimator(data))
        self.assertNotIn('$1.13–$1.13', estimator.markdown_summary(data))

    def test_quote_only_never_publishes_supplied_numeric_fields(self):
        data = fixture()
        data['roles'] = [data['roles'][1]]
        data['roles'][0].update(rate_min=999.99, rate_max=999.99, unit='hour')
        normalized = estimator.normalize_data(data)
        self.assertNotIn('rate_min', normalized['roles'][0])
        self.assertNotIn('rate_max', normalized['roles'][0])
        for output in (estimator.render_estimator(data), estimator.markdown_summary(data)):
            self.assertIn('Scoped quote required', output)
            self.assertNotIn('999.99', output)
            self.assertNotIn('$', output)

    def test_whitelist_drops_private_and_unknown_fields_without_mutating_input(self):
        data = fixture()
        data.update(client_email='private@example.invalid', invoice_id='PRIVATE-INVOICE',
                    payment_details={'bank': 'PRIVATE-BANK'})
        data['roles'][0].update(client_name='PRIVATE-CLIENT', invoice_lines=['PRIVATE-LINE'])
        original = copy.deepcopy(data)
        normalized = estimator.normalize_data(data)
        self.assertEqual(set(normalized), {'currency', 'as_of', 'observation_period', 'source_note',
                                          'hours_per_week', 'weeks_per_year', 'months_per_year', 'roles'})
        self.assertEqual(set(normalized['roles'][0]), {'id', 'label', 'note', 'unit', 'rate_min', 'rate_max', 'quote_only'})
        for output in (estimator.render_estimator(data), estimator.markdown_summary(data)):
            for private in ('private@example.invalid', 'PRIVATE-INVOICE', 'PRIVATE-BANK', 'PRIVATE-CLIENT', 'PRIVATE-LINE'):
                self.assertNotIn(private, output)
        self.assertEqual(data, original)

    def test_markup_escapes_text_and_embedded_json_cannot_close_script(self):
        data = fixture()
        data['roles'][0]['label'] = '<img src=x onerror="alert(1)"> & fixture'
        data['roles'][0]['note'] = 'Synthetic | scope\nwith a new line'
        data['source_note'] = '</script><script>alert("synthetic")</script> & source'
        source = estimator.render_estimator(data)
        markup = Markup(source)
        self.assertEqual(len(markup.scripts), 1)
        self.assertEqual(markup.scripts[0]['type'], 'application/json')
        self.assertNotIn('img', markup.tags)
        self.assertIn('&lt;img', source)
        self.assertIn('\\u003c/script\\u003e', source)
        self.assertEqual(json.loads(''.join(markup.script_data)), estimator.normalize_data(data))
        self.assertIn('Synthetic \\| scope with a new line', estimator.markdown_summary(data))

    def test_no_javascript_fallback_and_accessible_controls(self):
        markup = Markup(estimator.render_estimator(fixture()))
        self.assertIn('noscript', markup.tags)
        self.assertIn('table', markup.tags)
        self.assertLess(markup.tags.index('select'), markup.tags.index('table'))
        self.assertIn('full rate table below', ' '.join(markup.text))
        self.assertTrue({'oe-role', 'oe-count', 'oe-hours'} <= markup.labels)
        self.assertEqual(markup.by_id['oe-result']['role'], 'status')
        self.assertEqual(markup.by_id['oe-result']['aria-live'], 'polite')
        self.assertEqual(markup.by_id['oe-hours']['step'], 'any')
        self.assertEqual(markup.by_id['oe-quote']['href'], '#footer-cta')

    def test_invalid_metadata_and_assumptions_fail_closed(self):
        for changes in ({'currency': 'PHP'}, {'as_of': '2026-02-30'}, {'as_of': ''},
                        {'source_note': ''}, {'observation_period': ''}, {'roles': []},
                        {'weeks_per_year': 0}, {'months_per_year': 13},
                        {'hours_per_week': 41}, {'hours_per_week': 0},
                        {'hours_per_week': True}, {'hours_per_week': float('nan')},
                        {'hours_per_week': 37.555}):
            data = fixture()
            data.update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                estimator.render_estimator(data)
            with self.subTest(markdown_changes=changes), self.assertRaises(ValueError):
                estimator.markdown_summary(data)

    def test_invalid_or_duplicate_roles_fail_closed(self):
        for changes in ({'id': '<script>'}, {'label': ''}, {'unit': 'month'},
                        {'rate_min': -1}, {'rate_min': 20}, {'rate_max': float('inf')},
                        {'rate_min': True}, {'rate_min': 10.251}):
            data = fixture()
            data['roles'][0].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                estimator.normalize_data(data)
        data = fixture()
        data['roles'].append(copy.deepcopy(data['roles'][0]))
        with self.assertRaises(ValueError):
            estimator.normalize_data(data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
