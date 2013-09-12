from django.forms.widgets import Media
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe


__all__ = ('CSS', 'JS')


class EmbeddedMedia(object):
    """
    Base class for adding embedded CSS and JS to a Media class.
    """
    def __init__(self, content, **attrs):
        self.content = content
        self.attrs = attrs

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.content == other.content
        )

    def build_attrs(self):
        attrs = [(k, conditional_escape(v)) for k, v in self.attrs.iteritems()]
        attrs = ' '.join(['{0}="{1}"'.format(*x) for x in attrs])
        return attrs


class CSS(EmbeddedMedia):
    def render(self, medium=None):
        medium = medium or 'all'
        attrs = self.build_attrs()
        html = '<style type="text/css" media="{{0}}" {0}>{{1}}</style>'.format(attrs)
        return format_html(html, medium, mark_safe(self.content))


class JS(EmbeddedMedia):
    def render(self):
        attrs = self.build_attrs()
        html = '<script type="text/javascript" {0}>{{0}}</script>'.format(attrs)
        return format_html(html, mark_safe(self.content))


def render_css(self):
    # To keep rendering order consistent, we can't just iterate over items().
    # We need to sort the keys, and iterate over the sorted list.
    html = []
    media = sorted(self._css.keys())
    for medium in media:
        for style in self._css[medium]:
            if hasattr(style, 'render'):
                html.append(style.render(medium))
            else:
                html.append(format_html('<link href="{0}" type="text/css" media="{1}" rel="stylesheet" />', self.absolute_path(style), medium))
    return html

Media.render_css = render_css


def render_js(self):
    html = []
    for script in self._js:
        if hasattr(script, 'render'):
            html.append(script.render())
        else:
            html.append(format_html('<script type="text/javascript" src="{0}"></script>', self.absolute_path(script)))
    return html

Media.render_js = render_js
