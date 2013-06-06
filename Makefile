clean:
	-rm *~*
	-find . -name '*.pyc' -exec rm {} \;

runserver:
	PYTHONPATH=$(PYTHONPATH) python manage.py runserver

test:
	PYTHONPATH=$(PYTHONPATH) python manage.py test person

syncdb:
	PYTHONPATH=$(PYTHONPATH) python manage.py syncdb --no-input
