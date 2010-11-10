export VE=/tmp/ve/jqhelpers
source $VE/bin/activate
pip install -Ur pip/requirements.txt 
export PYTHONPATH=.:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=test_settings
django-admin.py test
coverage xml --include="jqhelpers/*"
python setup.py sdist
