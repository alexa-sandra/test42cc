# -*- coding: utf-8 -*-
from StringIO import StringIO
import sys
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template import Template, Context, RequestContext
from django.test.client import Client

from django.utils import unittest
from middleware import HttpStoredQueryMiddleware
from models import Person, HttpStoredQuery
from templatetags.edit_link import edit_link_in_admin


class PersonTestCase(unittest.TestCase):
    """
    Test for model Person and main page
    """
    fixtures = ['data.json']

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        person = Person.objects.get(pk=1)
        self.assertEqual(str(person.first_name), 'Alexandra')
        self.assertEqual(str(person.last_name), 'Mikhailjuk')
        self.assertEqual(str(person.birth_date.strftime("%d.%m.%Y")), '13.06.2013')
        self.assertEqual(str(person.bio), 'bio')
        self.assertEqual(str(person.email), 'a@mail.ru')
        self.assertEqual(str(person.jabber), 'a@mail.ru')
        self.assertEqual(str(person.skype), 'alexa_sandra_')


class HttpStoredQueryMiddlewareTest(unittest.TestCase):
    """
    Test middleware
    """
    def setUp(self):
        self.client = Client()

    def test_request(self):
        response = self.client.get(reverse('edit'))
        req = HttpStoredQuery.objects.latest('id')
        self.assertEqual(reverse('edit'), req.path)


class ContextProcessorTest(unittest.TestCase):
    """
    Test contextProcessor
    """
    def test_settings_in_context(self):
        #default_context = RequestContext(HttpRequest())
        #self.assertTrue(default_context.has_key('SETTINGS'))
        pass


class TestEditForm(unittest.TestCase):
    """
    Test edit form
    """
    def setUp(self):
        self.client = Client()
        self.admin = Client()
        self.admin.login(username='admin', password='admin')

    def test_login(self):
        response = self.admin.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_edit_form(self):
        user = User.objects.get(pk=1)
        # User not logged in
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username=user.username, password='admin')

        # Valid user
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)

        #Form
        new_data = Person.objects.values().get(id=1)
        new_data['birth_date'] = '1987-12-13'

        self.client.post('edit', data=new_data)
        response = self.client.get(reverse('edit'))
        self.assertTrue('<!DOCTYPE HTML>' in response.content)


class EditLinkTagTest(unittest.TestCase):
    """
    Test for template tag for edit object from template in admin site
    """
    
    def setUp(self):
        self.obj = Person.objects.get(pk=1)
        self.client = Client()

    def testEditLinkObject(self):
        link = '/admin/person/person/1/'
        t = Template('{% load edit_link %}{% admin_link obj %}')
        self.client.login(username="admin", password="admin")
        c = Context({"obj": self.obj})
        result = t.render(c)
        self.assertEqual(link, result)


class ModelsListCommandTest(unittest.TestCase):

    def test_command(self):
        from django.db.models import get_models

        output = sys.stdout = StringIO()
        call_command('appmodelslist', 'person')
        sys.stdout = sys.__stdout__
        for model in get_models('person'):
            self.assertEqual(output.getvalue().find(model.__name__), 0)

