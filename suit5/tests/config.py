from types import SimpleNamespace

from django.contrib.admin import AdminSite
from django.contrib.admin import ModelAdmin
from django.conf import settings
from django.test import override_settings
from suit5 import VERSION
from suit5.config import default_config, get_config, get_config_name
from suit5.templatetags.suit_tags import admin_url
from suit5.tests.models import Book
from suit5.tests.mixins import UserTestCaseMixin, ModelsTestCaseMixin


class ConfigTestCase(UserTestCaseMixin):
    def test_default_config(self):
        default_suit_config = default_config()
        self.assertEqual(VERSION, default_suit_config['VERSION'])

    def test_suit_config_when_not_defined(self):
        try:
            del settings.SUIT_CONFIG
        except AttributeError:
            pass
        default_suit_config = default_config()
        self.assertEqual(get_config('ADMIN_NAME'),
                         default_suit_config['ADMIN_NAME'])

        # Defined as None, should also use fallback
        admin_name = None
        settings.SUIT_CONFIG = {
            'ADMIN_NAME': admin_name
        }
        self.assertEqual(get_config('ADMIN_NAME'),
                         default_suit_config['ADMIN_NAME'])

    def test_suit_config_when_defined_but_no_key(self):
        settings.SUIT_CONFIG = {
            'RANDOM_KEY': 123
        }
        default_suit_config = default_config()
        self.assertEqual(get_config('ADMIN_NAME'),
                         default_suit_config['ADMIN_NAME'])
        # Defined as empty, should stay empty
        admin_name = ''
        settings.SUIT_CONFIG = {
            'ADMIN_NAME': admin_name
        }
        self.assertEqual(get_config('ADMIN_NAME'), admin_name)

    def test_suit_config_when_defined(self):
        admin_name = 'Custom Name'
        settings.SUIT_CONFIG = {
            'ADMIN_NAME': admin_name
        }
        self.assertEqual(get_config('ADMIN_NAME'), admin_name)

    def test_django_modeladmin_overrides(self):
        self.assertEqual(ModelAdmin.actions_on_top, False)
        self.assertEqual(ModelAdmin.actions_on_bottom, True)
        self.assertEqual(ModelAdmin.list_per_page, get_config('LIST_PER_PAGE'))

    @override_settings(
        SUIT_CONFIG={'ADMIN_NAME': 'Internal'},
        SUIT_CONFIG_DEALER={'ADMIN_NAME': 'Dealer'},
    )
    def test_admin_site_can_select_its_own_config(self):
        class DealerSite(AdminSite):
            settings_name = 'SUIT_CONFIG_DEALER'

        view = lambda request: None
        view.admin_site = DealerSite(name='dealer')
        request = SimpleNamespace(
            resolver_match=SimpleNamespace(func=view, namespace='dealer'),
        )

        self.assertEqual(get_config_name(request), 'SUIT_CONFIG_DEALER')
        self.assertEqual(get_config('ADMIN_NAME', request=request), 'Dealer')

    @override_settings(
        SUIT_CONFIG={'ADMIN_NAME': 'Internal'},
        SUIT_CONFIG_DEALER={'ADMIN_NAME': 'Legacy dealer'},
    )
    def test_admin_namespace_supports_legacy_config_name(self):
        request = SimpleNamespace(
            resolver_match=SimpleNamespace(func=lambda request: None, namespace='dealer'),
        )

        self.assertEqual(get_config_name(request), 'SUIT_CONFIG_DEALER')
        self.assertEqual(get_config('ADMIN_NAME', request=request), 'Legacy dealer')


class ConfigWithModelsTestCase(ModelsTestCaseMixin, UserTestCaseMixin):

    def create_book(self):
        book = Book(pk=2, name='Some book')
        book.save()
        return book

    def test_confirm_unsaved_changes(self):
        self.login_superuser()
        settings.SUIT_CONFIG['CONFIRM_UNSAVED_CHANGES'] = True
        book = self.create_book()

        response = self.client.get(admin_url(book))
        content_if_true = 'confirmExitIfModified'
        self.assertContains(response, content_if_true)

        # Test without unsaved changes
        settings.SUIT_CONFIG['CONFIRM_UNSAVED_CHANGES'] = False
        response = self.client.get(admin_url(book))
        self.assertNotContains(response, content_if_true)

    def test_show_required_asterisk(self):
        self.login_superuser()
        settings.SUIT_CONFIG['SHOW_REQUIRED_ASTERISK'] = True
        book = self.create_book()

        response = self.client.get(admin_url(book))
        content_if_true = ".required:after { content: '*';"
        self.assertContains(response, content_if_true)

        # Test without confirm
        settings.SUIT_CONFIG['SHOW_REQUIRED_ASTERISK'] = False
        response = self.client.get(admin_url(book))
        self.assertNotContains(response, content_if_true)
