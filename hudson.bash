bin/django test --with-xunit --with-coverage --cover-package=jqhelpers --cover-erase mysite.demo
bin/coverage xml --omit="parts,eggs,downloads,mysite"
