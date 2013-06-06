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
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        person = Person.objects.latest('id')
        self.find(str(person.first_name))
        self.find(str(person.last_name))
        self.find(str(person.birth_date.strftime("%d.%m.%Y")))
        self.find(str(person.bio))
        self.find(str(person.email))
        self.find(str(person.jabber))
        self.find(str(person.skype))
        

