from django import template
from django.utils.safestring import mark_safe
register = template.Library()
import jqhelpers.conf

INLINES = 'jq_inline'

@register.simple_tag
def jquery():
    return mark_safe('''<script type="text/javascript" src="{url}"></script>
       <script type="text/javascript">
       var django = {{jQuery: jQuery.noConflict(true)}};
       </script>'''.format(url=jqhelpers.conf.JQHELPERS_JQUERY_SRC))

@register.simple_tag
def jquery_css(): return ''

@register.tag
def jq_add_inline(parser, token):
    nodelist = parser.parse(('endjq_add_inline',))
    parser.delete_first_token()
    return JQAddInline(nodelist)

class JQAddInline(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        script = self.nodelist.render(context)
        context[INLINES].append(script)
        return ''

@register.tag
def jq_inline(parser, token):
    return JQInline()

class JQInline(template.Node):
    def render(self, context):
        if not context[INLINES]: return ''
        script = '\n'.join(context[INLINES])
        return mark_safe('''
        <script type="text/javascript">
        (function(jQuery){{
            (function($){{
                {script}
            }})(jQuery);
        }})(django.jQuery);
        </script>'''.format(script=script))
