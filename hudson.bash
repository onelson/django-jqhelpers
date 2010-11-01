python bootstrap.py
bin/buildout
bin/django test --with-xunit --with-coverage --cover-erase
bin/coverage xml --include="src/*"
python setup.py build
python setup.py sdist
python setup.py bdist
