from django import template

register = template.Library()


@register.filter
def get_item(mapping, key):
    if not mapping:
        return ''
    return mapping.get(key, '')


@register.filter
def file_url(file_obj):
    if not file_obj:
        return ''
    try:
        return file_obj.url
    except Exception:
        return ''


def _feature_value(feature, *keys):
    if isinstance(feature, dict):
        for key in keys:
            value = feature.get(key)
            if value:
                return str(value).strip()
        return ''
    if isinstance(feature, str):
        return ''
    for key in keys:
        value = getattr(feature, key, '')
        if value and not callable(value):
            return str(value).strip()
    return ''


def _normalized(value):
    return ' '.join(str(value).strip().lower().split())


@register.filter
def feature_title(feature):
    if isinstance(feature, str):
        return feature.strip()
    title = _feature_value(feature, 'title', 'name', 'text')
    return title or str(feature).strip()


@register.filter
def feature_description(feature):
    title = feature_title(feature)
    description = _feature_value(feature, 'description', 'text')
    if not description or _normalized(description) == _normalized(title):
        return ''
    return description


@register.filter
def feature_icon(feature):
    return _feature_value(feature, 'icon')
