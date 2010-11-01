from django import template
from django.utils.safestring import mark_safe
from jqhelpers.utils import unique_list
import jqhelpers.conf
from django.conf import settings

register = template.Library()

PLUGIN_CONTEXT_KEY = 'jq_plugins'
SCRIPT_CONTEXT_KEY = 'jq_scripts'
SCRIPT_INLINE_CONTEXT_KEY = 'jq_script_inline'

__initial_context__ = {
    PLUGIN_CONTEXT_KEY: [],
    SCRIPT_CONTEXT_KEY: [],
    SCRIPT_INLINE_CONTEXT_KEY: [],
}

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
        context[SCRIPT_INLINE_CONTEXT_KEY].append(script)
        return ''

@register.tag
def jq_inline(parser, token):
    return JQInline()

class JQInline(template.Node):
    def render(self, context):
        if not context[SCRIPT_INLINE_CONTEXT_KEY]: return ''
        script = '\n'.join(context[SCRIPT_INLINE_CONTEXT_KEY])
        return mark_safe('''
        <script type="text/javascript">
        (function(jQuery){{
            (function($){{
                {script}
            }})(jQuery);
        }})(django.jQuery);
        </script>'''.format(script=script))

class RenderContextList(template.Node):
    """
    Takes an already existing list of strings stored in the current context,
    and formats each using self.wrapper, then concatenates them together.
    """
    context_key = None
    wrapper = '{}'
    glue = '\n'
    
    def __init__(self, context_key=None, wrapper=None, glue=None):
        if context_key:
            self.context_key = context_key
        if wrapper: 
            self.wrapper = wrapper
        if glue:
            self.glue = glue
    
    def render(self, context):
        if not context[self.context_key]: return ''
        items = self.glue.join([self.wrapper.format(i) for i in unique_list(context[self.context_key])])
        return mark_safe(items)

class ContextListAdd(template.Node):
    """
    Appends the arg `item` to a list of items in the current context.
    """
    context_key = None
    
    def __init__(self, item):
        if not self.context_key: raise NotImplementedError
        self.item = str(item)
    
    def render(self, context):
        context[self.context_key].append(settings.STATICFILES_URL+self.item)
        return ''

class AddPlugin(ContextListAdd):
    context_key = PLUGIN_CONTEXT_KEY

class AddScript(ContextListAdd):
    context_key = SCRIPT_CONTEXT_KEY

@register.tag
def jq_scripts(parser, token):
    return RenderContextList(context_key=SCRIPT_CONTEXT_KEY, 
                             wrapper='<script type="text/javascript" src="{0}"></script>')
@register.tag
def jq_plugins(parser, token):
    return RenderContextList(context_key=PLUGIN_CONTEXT_KEY, 
                             wrapper='<script type="text/javascript" src="{0}"></script>')

@register.tag
def jq_add_script(parser, token):
    try:
        tag_name, src = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (src[0] == src[-1] and src[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return AddScript(src[1:-1])

@register.tag
def jq_add_plugin(parser, token):
    try:
        tag_name, src = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (src[0] == src[-1] and src[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return AddPlugin(src[1:-1])

@register.simple_tag
def jquery():
    return mark_safe('''<script type="text/javascript" src="{jquery}"></script>
       <script type="text/javascript">
       var django = {{jQuery: jQuery.noConflict(true)}};
       </script>'''.format(jquery=jqhelpers.conf.JQHELPERS_JQUERY_SRC))

@register.simple_tag
def jquery_ui():
    return mark_safe('''<script type="text/javascript" src="{jquery}"></script>
    <script type="text/javascript" src="{jquery_ui}"></script>
    <script type="text/javascript">
    var django = {{jQuery: jQuery.noConflict(true)}};
    </script>'''.format(jquery=jqhelpers.conf.JQHELPERS_JQUERY_SRC,
                        jquery_ui=jqhelpers.conf.JQHELPERS_JQUERY_UI_SRC))

@register.simple_tag
def jquery_ui_theme():
    return mark_safe('''<link href="{0}" rel="stylesheet" type="text/css" />'''.format(jqhelpers.conf.JQHELPERS_JQUERY_UI_THEME))