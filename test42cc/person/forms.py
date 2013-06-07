from django.conf import settings
from django.forms import ModelForm, Textarea
from django.utils.safestring import mark_safe
from models import Person
from django import forms


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'bio' : Textarea({'cols':40, 'rows':10}),
            'other_contacts' : Textarea({'cols':40, 'rows':10}),
                   }


    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
