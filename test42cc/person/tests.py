# -*- coding: utf-8 -*-
from StringIO import StringIO
import sys
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.template import Template, Context
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
        #self.client = Client()
        pass

    def test_index(self):
        response = self.client.get(reverse('/'))
        self.assertEqual(response.status_code, 200)
        person = Person.objects.latest('id')
        self.find(str(person.first_name))
        self.find(str(person.last_name))
        self.find(str(person.birth_date.strftime("%d.%m.%Y")))
        self.find(str(person.bio))
        self.find(str(person.email))
        self.find(str(person.jabber))
        self.find(str(person.skype))


class HttpStoredQueryMiddlewareTest(unittest.TestCase):

    def setUp(self):
        self.m = HttpStoredQueryMiddleware()
        self.request = HttpStoredQuery()

    def test_request(self):
        data = {'path': '/admin', 'method' : 'POST'}
        self.assertEqual(self.m.process_request(self.request), None)
        self.assertIsInstance(self.request.path, HttpStoredQuery)
        self.assertEqual(self.request.path, data['path'])

        
class ContextProcessorTest(unittest.TestCase):
    """
    Test contextProcessor
    """
    def test_settings_in_context(self):
        self.response = Client().get(reverse('/'))
        self.assertEqual(settings, self.response.context['settings'])
        self.assertTrue('settings' in self.response.context)


class TestEditForm(unittest.TestCase):
    """
    Test edit form
    """
    def setUp(self):
        self.client = Client()

    def test_login(self):
        response = self.client.get('login')
        self.assertEqual(response.status_code, 200)

    def test_edit_form(self):
        user = User.objects.get(pk=1)
        # User not logged in
        response = self.client.get('edit')
        self.assertEqual(response.status_code, 403)

        self.client.login(username=user.username, password='admin')

        # Valid user
        response = self.client.get('edit')
        self.assertEqual(response.status_code, 200)

        #Form
        new_data = Person.objects.values().get(id=1)
        new_data['birth_date'] = '1987-12-13'

        self.client.post('edit', data=new_data)
        response = self.client.get('edit')
        self.assertContains(response, '')


class EditLinkTagTest(unittest.TestCase):
    """
    Test for template tag for edit object from template in admin site
    """
    def setUp(self):
        self.obj = Person.objects.get(pk=1)
        self.client = Client()

    def testEditLinkObject(self):
        t = Template('{% load edit_link %}{% admin_link obj %}')
        self.client.login(username="admin", password="admin")
        admin_edit_link = edit_link_in_admin('',self.obj)
        c = Context({"obj": self.obj})
        result = t.render(c)
        self.assertEqual(admin_edit_link, result.lstrip())

class ModelsListCommandTest(unittest.TestCase):

    def test_command(self):
        from django.db.models import get_models

        output = sys.stdout = StringIO()
        call_command('appmodelslist person')
        sys.stdout = sys.__stdout__
        for model in get_models():
            self.assertNotEqual(output.getvalue().find(model._meta.object_name), 0)
