MANAGE=django-admin.py
PROJECT=test42cc

clean:
	-rm *~*
	-find . -name '*.pyc' -exec rm {} \;

runserver:
	PYTHONPATH=$(PYTHONPATH) python manage.py runserver

test:
	PYTHONPATH=$(PYTHONPATH) python manage.py test person

syncdb:
	PYTHONPATH= $(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) syncdb --noinput --no-initial-data --migrate
	PYTHONPATH= $(PYTHONPATH) python manage.py loaddata data.json

