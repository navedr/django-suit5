from copy import copy
from inspect import getfullargspec
from django import VERSION as DJANGO_VERSION, template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.contrib.admin.templatetags.admin_list import pagination as admin_pagination, result_list
from django.contrib.admin.views.main import ALL_VAR, PAGE_VAR
from django.utils.html import escape
from suit5.compat import tpl_context_class

try:
    # Python 3.
    from urllib.parse import parse_qs
except ImportError:
    # Python 2.5+
    from urlparse import urlparse

    try:
        # Python 2.6+
        from urlparse import parse_qs
    except ImportError:
        # Python <=2.5
        from cgi import parse_qs

register = template.Library()

DOT = '.'
# Django 3.2 changed admin changelists from zero-based to one-based pages.
PAGE_NUMBER_OFFSET = 1 if DJANGO_VERSION < (3, 2) else 0


@register.simple_tag
def paginator_number(cl, i):
    """
    Generates an individual page index link in a paginated list.
    """
    if i == DOT:
        return mark_safe(
                '<li class="disabled"><a href="#" onclick="return false;">..'
                '.</a></li>')
    elif i == cl.page_num:
        return mark_safe(
            '<li class="active"><a href="">%d</a></li> ' % (i + PAGE_NUMBER_OFFSET))
    else:
        return mark_safe('<li><a href="%s"%s>%d</a></li> ' % (
            escape(cl.get_query_string({PAGE_VAR: i})),
            (i + PAGE_NUMBER_OFFSET == cl.paginator.num_pages and ' class="end"' or ''),
            i + PAGE_NUMBER_OFFSET))


@register.simple_tag
def paginator_info(cl):
    paginator = cl.paginator

    # If we show all rows of list (without pagination)
    if cl.show_all and cl.can_show_all:
        entries_from = 1 if paginator.count > 0 else 0
        entries_to = paginator.count
    else:
        entries_from = (
            (paginator.per_page * (cl.page_num + PAGE_NUMBER_OFFSET - 1)) + 1
        ) if paginator.count > 0 else 0
        entries_to = entries_from - 1 + paginator.per_page
        if paginator.count < entries_to:
            entries_to = paginator.count

    return '%s - %s' % (entries_from, entries_to)


@register.inclusion_tag('admin/pagination.html')
def pagination(cl):
    """
    Generates the series of links to the pages in a paginated list.
    """
    if DJANGO_VERSION < (3, 2):
        # Older Django has no get_elided_page_range(); use its native range
        # generation, which also preserves zero-based query-string values.
        return admin_pagination(cl)

    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) \
        and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        page_range = [
            DOT if page == paginator.ELLIPSIS else page
            for page in paginator.get_elided_page_range(
                page_num,
                on_each_side=3,
                on_ends=2,
            )
        ]

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string(
            {ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
    }


@register.simple_tag
def suit_list_filter_select(cl, spec):
    choices = list(spec.choices(cl))
    form_based = any('form' in choice and 'query_string' not in choice for choice in choices)
    tpl = get_template('admin/filter_form.html' if form_based else spec.template)
    field_key = spec.field_path if hasattr(spec, 'field_path') else \
        spec.parameter_name
    matched_key = field_key
    for choice in choices:
        # Third-party filters can render a bound form instead of Django's
        # query-string choice dictionaries (django-unfold is one example).
        if 'query_string' not in choice:
            continue
        query_string = choice['query_string'][1:]
        query_parts = parse_qs(query_string)

        value = ''
        matches = {}
        for key in query_parts.keys():
            if key == field_key:
                value = query_parts[key][0]
                matched_key = key
            elif key.startswith(
                            field_key + '__') or '__' + field_key + '__' in key:
                value = query_parts[key][0]
                matched_key = key

            if value:
                matches[matched_key] = value

        # Iterate matches, use first as actual values, additional for hidden
        i = 0
        for key, value in matches.items():
            if i == 0:
                choice['name'] = key
                choice['val'] = value
            else:
                choice['additional'] = '%s=%s' % (key, value)
            i += 1

    return tpl.render(tpl_context_class({
        'field_name': field_key,
        'title': spec.title,
        'choices': choices,
        'spec': spec,
    }))


@register.filter
def headers_handler(result_headers, cl):
    """
    Adds field name to css class, so we can style specific columns
    """
    # field = cl.list_display.get()
    attrib_key = 'class_attrib'
    for i, header in enumerate(result_headers):
        field_name = cl.list_display[i]
        if field_name == 'action_checkbox':
            continue
        if not attrib_key in header:
            header[attrib_key] = mark_safe(' class=""')

        pattern = 'class="'
        if pattern in header[attrib_key]:
            replacement = '%s%s-column ' % (pattern, field_name)
            header[attrib_key] = mark_safe(
                header[attrib_key].replace(pattern, replacement))

    return result_headers


def dict_to_attrs(attrs):
    return mark_safe(' ' + ' '.join(['%s="%s"' % (k, v)
                                     for k, v in attrs.items()]))


@register.inclusion_tag('admin/change_list_results.html', takes_context=True)
def result_list_with_context(context, cl):
    """
    Wraps Djangos default result_list to ammend the context with the request.

    This gives us access to the request in change_list_results.
    """
    res = result_list(cl)
    res['request'] = context['request']
    return res


@register.simple_tag(takes_context=True)
def result_row_attrs(context, cl, row_index):
    """
    Returns row attributes based on object instance
    """
    row_index -= 1
    attrs = {
        'class': 'row1' if row_index % 2 == 0 else 'row2'
    }
    suit_row_attributes = getattr(cl.model_admin, 'suit_row_attributes', None)
    if not suit_row_attributes:
        return dict_to_attrs(attrs)

    instance = cl.result_list[row_index]

    # Backwards compatibility for suit_row_attributes without request argument
    args = getfullargspec(suit_row_attributes)
    if 'request' in args[0]:
        new_attrs = suit_row_attributes(instance, context['request'])
    else:
        new_attrs = suit_row_attributes(instance)

    if not new_attrs:
        return dict_to_attrs(attrs)

    # Validate
    if not isinstance(new_attrs, dict):
        raise TypeError('"suit_row_attributes" must return dict. Got: %s: %s' %
                        (new_attrs.__class__.__name__, new_attrs))

    # Merge 'class' attribute
    if 'class' in new_attrs:
        attrs['class'] += ' ' + new_attrs.pop('class')

    attrs.update(new_attrs)
    return dict_to_attrs(attrs)


@register.filter
def cells_handler(results, cl):
    """
    Changes result cell attributes based on object instance and field name
    """
    suit_cell_attributes = getattr(cl.model_admin, 'suit_cell_attributes', None)
    if not suit_cell_attributes:
        return results

    class_pattern = 'class="'
    td_pattern = '<td'
    th_pattern = '<th'
    for row, result in enumerate(results):
        instance = cl.result_list[row]
        for col, item in enumerate(result):
            field_name = cl.list_display[col]
            attrs = copy(suit_cell_attributes(instance, field_name))
            if not attrs:
                continue

            # Validate
            if not isinstance(attrs, dict):
                raise TypeError('"suit_cell_attributes" must return dict. '
                                'Got: %s: %s' % (
                                    attrs.__class__.__name__, attrs))

            # Merge 'class' attribute
            if class_pattern in item.split('>')[0] and 'class' in attrs:
                css_class = attrs.pop('class')
                replacement = '%s%s ' % (class_pattern, css_class)
                result[col] = mark_safe(
                    item.replace(class_pattern, replacement))

            # Add rest of attributes if any left
            if attrs:
                cell_pattern = td_pattern if item.startswith(
                    td_pattern) else th_pattern

                result[col] = mark_safe(
                    result[col].replace(cell_pattern,
                                 td_pattern + dict_to_attrs(attrs)))

    return results
