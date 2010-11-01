bin/django test --with-xunit --with-coverage --cover-package=jqhelpers --cover-erase
bin/coverage xml --omit="parts,eggs,downloads,mysite"
