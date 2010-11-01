python bootstrap.py
bin/buildout
bin/django test --with-xunit --with-coverage --cover-erase --cover-package=jqhelpers
bin/coverage xml --include="src"
python setup.py build
python setup.py sdist
python setup.py bdist
