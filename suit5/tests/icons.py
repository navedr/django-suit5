import json
import os
import re
import unittest

from django.test import SimpleTestCase

SUIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(SUIT_ROOT)
ICONS_SCSS = os.path.join(SUIT_ROOT, 'static', 'suit5', 'scss', '_icons.scss')
ICONS_JSON = os.path.join(REPO_ROOT, 'node_modules', 'bootstrap-icons', 'font', 'bootstrap-icons.json')
ICONS_CSS = os.path.join(SUIT_ROOT, 'static', 'suit5', 'css', 'suit.css')

# .icon-a::before,\n.icon-b::before { content: "\f1f6"; } // bi-calendar
RULE_RE = re.compile(
    r'((?:\.[a-z0-9-]+::before,?\s*)+)\{\s*content:\s*"\\([0-9a-f]{4})";\s*\}\s*//\s*bi-([a-z0-9-]+)')


def load_icon_names():
    with open(ICONS_JSON, encoding='utf-8') as fh:
        return json.load(fh)


@unittest.skipUnless(os.path.exists(ICONS_JSON),
                     'bootstrap-icons not installed (run npm install)')
class IconCompatMapTestCase(SimpleTestCase):
    """Guards the Glyphicon -> Bootstrap Icons compatibility layer.

    Bootstrap Icons assigns codepoints alphabetically, so adding an icon upstream shifts
    every codepoint after it. A stale literal in _icons.scss does not fail loudly -- the
    class keeps rendering and simply draws the wrong picture (0.3.8 shipped .icon-calendar
    pointing at bi-calendar-x-fill). These tests compare every codepoint against the
    bootstrap-icons package, so the drift becomes a test failure instead of a surprise.
    """

    def test_every_codepoint_matches_its_named_icon(self):
        icons = load_icon_names()
        with open(ICONS_SCSS, encoding='utf-8') as fh:
            source = fh.read()

        rules = RULE_RE.findall(source)
        self.assertGreater(len(rules), 50, 'icon map looks truncated')

        mismatched = []
        for selectors, codepoint, name in rules:
            expected = icons.get(name)
            if expected is None:
                mismatched.append('bi-%s does not exist in bootstrap-icons' % name)
                continue
            if '%04x' % expected != codepoint:
                mismatched.append('%s: bi-%s is \\%04x, map says \\%s'
                                  % (selectors.strip(), name, expected, codepoint))

        self.assertEqual(mismatched, [],
                         'Icon map is out of date -- run: npm run build:icons')

    def test_annotated_codepoints_anywhere_in_the_scss_tree(self):
        """The generated map is not the only place codepoints are written by hand.

        ``ui/_form.scss`` carried its own ``.date-icon::before { content: "\\f1f4" } // bi-calendar``
        and drifted exactly like the map did. Any ``content`` literal annotated with the
        icon it is meant to be is checked here, wherever it lives.
        """
        icons = load_icon_names()
        scss_root = os.path.join(SUIT_ROOT, 'static', 'suit5', 'scss')

        annotated = re.compile(
            r'content:\s*"\\([0-9a-f]{4})";?\s*(?:\}\s*)?//\s*bi-([a-z0-9-]+)')

        wrong = []
        checked = 0
        for dirpath, _dirnames, filenames in os.walk(scss_root):
            for filename in sorted(filenames):
                if not filename.endswith('.scss'):
                    continue
                path = os.path.join(dirpath, filename)
                with open(path, encoding='utf-8') as fh:
                    for lineno, line in enumerate(fh, 1):
                        match = annotated.search(line)
                        if match is None:
                            continue
                        checked += 1
                        codepoint, name = match.groups()
                        expected = icons.get(name)
                        where = '%s:%d' % (os.path.relpath(path, SUIT_ROOT), lineno)
                        if expected is None:
                            wrong.append('%s: bi-%s does not exist' % (where, name))
                        elif '%04x' % expected != codepoint:
                            wrong.append('%s: bi-%s is \\%04x, css says \\%s'
                                         % (where, name, expected, codepoint))

        self.assertGreater(checked, 50, 'scss scan found almost nothing -- bad regex?')
        self.assertEqual(wrong, [], 'icon codepoints are stale')

    def test_no_legacy_class_is_mapped_twice(self):
        with open(ICONS_SCSS, encoding='utf-8') as fh:
            source = fh.read()

        seen = {}
        duplicates = []
        for selectors, _codepoint, name in RULE_RE.findall(source):
            for selector in re.findall(r'\.([a-z0-9-]+)::before', selectors):
                if selector in seen:
                    duplicates.append('.%s: bi-%s and bi-%s' % (selector, seen[selector], name))
                seen[selector] = name

        self.assertEqual(duplicates, [], 'a class mapped twice silently takes the last value')

    def test_compiled_css_is_in_sync_with_the_scss(self):
        """suit.css is committed, so a regenerated map that was never compiled is a bug."""
        with open(ICONS_SCSS, encoding='utf-8') as fh:
            expected = {}
            for selectors, codepoint, _name in RULE_RE.findall(fh.read()):
                for selector in re.findall(r'\.([a-z0-9-]+)::before', selectors):
                    expected[selector] = codepoint

        with open(ICONS_CSS, encoding='utf-8') as fh:
            css = fh.read()

        stale = []
        for selector, codepoint in expected.items():
            match = re.search(r'[,{]?\.%s::before[,{][^}]*content:"(.)"' % re.escape(selector), css)
            if match is None:
                match = re.search(r'\.%s::before[^}]*?content:"(.)"' % re.escape(selector), css)
            if match is None:
                stale.append('%s missing from compiled css' % selector)
            elif '%04x' % ord(match.group(1)) != codepoint:
                stale.append('%s: css has \\%04x, scss has \\%s'
                             % (selector, ord(match.group(1)), codepoint))

        self.assertEqual(stale, [], 'suit.css is stale -- run: npm run build:css')
