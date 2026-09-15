import os
import re

from django.test import SimpleTestCase

SUIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUIT_CSS = os.path.join(SUIT_ROOT, 'static', 'suit5', 'css', 'suit.css')

RAIL_TOKEN = '--suit-nav-rail-bg'

# #suit-left,#sidebarOffcanvas{...background:var(--suit-nav-rail-bg)}
SIDEBAR_RE = re.compile(r'#suit-left,#sidebarOffcanvas\{([^}]*)\}')
# body:not(.popup):not(.login) #wrap{background:linear-gradient(...)}
RAIL_FILL_RE = re.compile(r'body:not\(\.popup\):not\(\.login\) #wrap\{([^}]*)\}')


class NavRailBackgroundTestCase(SimpleTestCase):
    """Guards the two-piece left navigation rail.

    ``#suit-left`` is a flex item, so it is only ever as tall as the taller of the nav
    and the page content. A gradient on ``#wrap`` (which is ``min-height: 100%``)
    continues the rail below it. Because the rail is painted in two separate places,
    recolouring one and not the other silently produces a half-painted sidebar on any
    short page -- the colour simply changes partway down, with no error anywhere.

    Both must therefore resolve the same custom property, so that a consumer overriding
    ``--suit-nav-rail-bg`` at ``:root`` recolours the whole rail in one declaration.
    """

    def setUp(self):
        with open(SUIT_CSS, encoding='utf-8') as fh:
            self.css = fh.read()

    def test_token_defaults_to_box_bg(self):
        """The token exists and falls back to --suit-box-bg, so existing themes are unchanged."""
        self.assertIn('%s: var(--suit-box-bg)' % RAIL_TOKEN, self.css)

    def test_sidebar_element_uses_the_token(self):
        match = SIDEBAR_RE.search(self.css)
        self.assertIsNotNone(match, 'sidebar rule not found -- selector renamed?')
        self.assertIn('background:var(%s)' % RAIL_TOKEN, match.group(1))

    def test_rail_continuation_uses_the_same_token(self):
        """The gradient below the sidebar must not drift away from the element's colour."""
        match = RAIL_FILL_RE.search(self.css)
        self.assertIsNotNone(match, 'rail continuation gradient not found -- selector renamed?')
        declaration = match.group(1)
        self.assertIn('linear-gradient', declaration)
        colours = set(re.findall(r'var\((--[a-z-]+)\)', declaration))
        self.assertEqual(
            colours, {RAIL_TOKEN},
            'rail gradient paints %s but #suit-left paints %s -- a short page will show '
            'the seam between them' % (sorted(colours), RAIL_TOKEN))
