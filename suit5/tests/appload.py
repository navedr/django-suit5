import os
import subprocess
import sys

from django.test import SimpleTestCase

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Run in a fresh interpreter: once any other test has imported suit5.config, the defaults
# are already applied and this check can no longer fail.
PROBE = """
import os, sys, json, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'suit5.tests.settings'
django.setup()
from django.contrib.admin import ModelAdmin
json.dump({
    'config_imported': 'suit5.config' in sys.modules,
    'actions_on_top': ModelAdmin.actions_on_top,
    'actions_on_bottom': ModelAdmin.actions_on_bottom,
    'list_per_page': ModelAdmin.list_per_page,
}, sys.stdout)
"""


class AppLoadDefaultsTestCase(SimpleTestCase):
    """Suit5's global ModelAdmin defaults must be applied by django.setup().

    They live as import-time side effects in suit5/config.py. When nothing imported that
    module at startup it was pulled in lazily by the template tags -- during the first
    changelist render, after ModelAdmin.changelist_view had already read actions_on_top
    into the context. The first changelist of every process therefore drew its action bar
    above the table and every later one below it.
    """

    def _probe(self):
        result = subprocess.run(
            [sys.executable, '-c', PROBE],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        import json
        return json.loads(result.stdout)

    def test_config_is_imported_during_setup(self):
        self.assertTrue(
            self._probe()['config_imported'],
            'suit5.config must be imported by app loading, not lazily by the template tags',
        )

    def test_action_placement_is_applied_before_any_request(self):
        state = self._probe()
        self.assertFalse(state['actions_on_top'], 'actions should default to the bottom')
        self.assertTrue(state['actions_on_bottom'])

    def test_list_per_page_is_applied_before_any_request(self):
        from suit5.config import get_config
        self.assertEqual(self._probe()['list_per_page'], get_config('LIST_PER_PAGE'))
