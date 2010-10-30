from django.conf import settings
JQHELPERS_JQUERY_SRC = getattr(settings, 'JQHELPERS_JQUERY_SRC', 'http://code.jquery.com/jquery-1.4.3.min.js')