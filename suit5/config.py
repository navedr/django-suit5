from django.contrib.admin import ModelAdmin
from django.conf import settings
from . import VERSION


DEFAULT_CONFIG_NAME = 'SUIT_CONFIG'


def default_config():
    return {
        'VERSION': VERSION,

        # configurable
        'ADMIN_NAME': 'Django Suit5',
        'HEADER_DATE_FORMAT': 'l, jS F Y',
        'HEADER_TIME_FORMAT': 'H:i',

        # form
        'SHOW_REQUIRED_ASTERISK': True,
        'CONFIRM_UNSAVED_CHANGES': True,

        # menu
        'SEARCH_URL': '/admin/auth/user/',
        'MENU_OPEN_FIRST_CHILD': True,
        'MENU_ICONS': {
            'auth': 'icon-lock',
            'sites': 'icon-leaf',
        },
        # 'MENU_EXCLUDE': ('auth.group',),
        # 'MENU': (
        #     'sites',
        #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
        #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
        #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
        # ),

        # misc
        'LIST_PER_PAGE': 20,
        'ALLOW_THEME_TOGGLE': True
    }


def get_config_name(request=None):
    """Return the settings key for the admin site handling ``request``.

    Custom ``AdminSite`` subclasses can set ``settings_name`` to use a separate
    Suit5 configuration. For backwards compatibility, a non-default admin
    namespace also falls back to ``SUIT_CONFIG_<NAMESPACE>`` when that setting
    exists.
    """
    resolver_match = getattr(request, 'resolver_match', None)
    if resolver_match is None:
        return DEFAULT_CONFIG_NAME

    view = resolver_match.func
    admin_site = getattr(view, 'admin_site', None)
    if admin_site is None:
        model_admin = getattr(view, 'model_admin', None)
        admin_site = getattr(model_admin, 'admin_site', None)

    settings_name = getattr(admin_site, 'settings_name', None)
    if settings_name:
        return settings_name

    namespace = resolver_match.namespace
    if namespace and namespace != 'admin':
        namespaced_config = '{}_{}'.format(DEFAULT_CONFIG_NAME, namespace.upper())
        if hasattr(settings, namespaced_config):
            return namespaced_config

    return DEFAULT_CONFIG_NAME


def get_config(param=None, request=None, config_key=None):
    config_key = config_key or get_config_name(request)
    config = getattr(settings, config_key, None) or default_config()
    if param:
        value = config.get(param)
        if value is None:
            value = default_config().get(param)
        return value
    return config

# Reverse default actions position
ModelAdmin.actions_on_top = False
ModelAdmin.actions_on_bottom = True

# Set global list_per_page
ModelAdmin.list_per_page = get_config('LIST_PER_PAGE')

def setup_filer():
    from suit5.widgets import AutosizedTextarea
    from filer.admin.imageadmin import ImageAdminForm
    from filer.admin.fileadmin import FileAdminChangeFrom
    from filer.admin import FolderAdmin

    def ensure_meta_widgets(meta_cls):
        if not hasattr(meta_cls, 'widgets'):
            meta_cls.widgets = {}

        meta_cls.widgets['description'] = AutosizedTextarea

    ensure_meta_widgets(ImageAdminForm.Meta)
    ensure_meta_widgets(FileAdminChangeFrom.Meta)
    FolderAdmin.actions_on_top = False
    FolderAdmin.actions_on_bottom = True


if 'filer' in settings.INSTALLED_APPS:
    setup_filer()
