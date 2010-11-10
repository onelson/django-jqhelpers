from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^$', 'django.views.generic.simple.direct_to_template',
     {'template':'jqhelpers/demo.html'}),
)
