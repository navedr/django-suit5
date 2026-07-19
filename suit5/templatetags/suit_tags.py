import itertools
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from suit5.config import get_config
from suit5 import utils

try:
    from django.core.urlresolvers import NoReverseMatch, reverse
except ImportError:
    from django.urls import NoReverseMatch, reverse

django_version = utils.django_major_version()

try:
    # Django 1.9
    from django.contrib.admin.utils import lookup_field
except ImportError:
    from django.contrib.admin.util import lookup_field

register = template.Library()

if django_version < (1, 9):
    simple_tag = register.assignment_tag
else:
    simple_tag = register.simple_tag


@register.filter(name='suit_conf')
def suit_conf(name):
    value = get_config(name)
    return mark_safe(value) if isinstance(value, str) else value


@register.simple_tag(takes_context=True)
def suit_conf_value(context, name):
    """Return a config value for the current admin site."""
    value = get_config(name, request=context.get('request'))
    return mark_safe(value) if isinstance(value, str) else value


class SuitNowNode(NowNode):
    def __init__(self, config_name):
        self.config_name = config_name

    def render(self, context):
        format_string = get_config(self.config_name, request=context.get('request'))
        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)
        return date_format(now, format_string, use_l10n=False)


@register.tag
def suit_date(parser, token):
    return SuitNowNode('HEADER_DATE_FORMAT')


@register.tag
def suit_time(parser, token):
    return SuitNowNode('HEADER_TIME_FORMAT')


@register.filter
def field_contents_foreign_linked(admin_field):
    """Return the .contents attribute of the admin_field, and if it
    is a foreign key, wrap it in a link to the admin page for that
    object.

    Use by replacing '{{ field.contents }}' in an admin template (e.g.
    fieldset.html) with '{{ field|field_contents_foreign_linked }}'.
    """
    fieldname = admin_field.field['field']
    displayed = admin_field.contents()
    obj = admin_field.form.instance

    if not hasattr(admin_field.model_admin,
                   'linked_readonly_fields') or fieldname not in admin_field \
            .model_admin \
            .linked_readonly_fields:
        return displayed

    try:
        fieldtype, attr, value = lookup_field(fieldname, obj,
                                              admin_field.model_admin)
    except ObjectDoesNotExist:
        fieldtype = None

    if isinstance(fieldtype, ForeignKey):
        try:
            url = admin_url(value)
        except NoReverseMatch:
            url = None
        if url:
            displayed = "<a href='%s'>%s</a>" % (url, displayed)
    return mark_safe(displayed)


@register.filter
def admin_url(obj):
    info = (obj._meta.app_label, obj._meta.object_name.lower())
    return reverse("admin:%s_%s_change" % info, args=[obj.pk])


@register.simple_tag
def suit_bc(*args):
    return utils.value_by_version(args)


@simple_tag
def suit_bc_value(*args):
    return utils.value_by_version(args)


@simple_tag
def admin_extra_filters(cl):
    """ Return the dict of used filters which is not included
    in list_filters form """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys()
                                             for s in cl.filter_specs)))
    return dict((k, v) for k, v in cl.params.items() if k not in used_parameters)


@register.simple_tag(takes_context=True)
def suit_dark_theme(context):
    return get_config('ALLOW_THEME_TOGGLE', request=context.get('request'))


@register.filter
def is_single_field(fields):
    return len(fields) == 1


@simple_tag
def suit_django_version():
    return django_version


@register.filter
def django_version_lt(string):
    return django_version < str_to_version(string)


@register.filter
def django_version_lte(string):
    return django_version <= str_to_version(string)


@register.filter
def django_version_gt(string):
    return django_version > str_to_version(string)


@register.filter
def django_version_gte(string):
    return django_version >= str_to_version(string)


def str_to_version(string):
    return tuple([int(s) for s in string.split('.')])


if django_version < (1, 9):
    # Add empty tags to avoid Django template errors if < Django 1.9
    @register.simple_tag
    def add_preserved_filters(*args, **kwargs):
        pass

if django_version < (1, 5):
    # Add admin_urlquote filter to support Django 1.4
    from django.contrib.admin.util import quote


    @register.filter
    def admin_urlquote(value):
        return quote(value)
