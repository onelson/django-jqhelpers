from django.conf import settings
JQHELPERS_JQUERY_SRC = getattr(settings, 'JQHELPERS_JQUERY_SRC', 'http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js')
JQHELPERS_JQUERY_UI_SRC = getattr(settings, 'JQHELPERS_JQUERY_UI_SRC', 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js')
