from django.conf import settings
from django.forms import ModelForm, Textarea
from django.utils.safestring import mark_safe
from models import Person
from django import forms


class DatePickerWidget(forms.DateInput):
    class Media:
        css = {
            'all': ('http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css',)
        }
        js = (
            'http://code.jquery.com/jquery-1.9.1.js',
            'http://code.jquery.com/ui/1.10.3/jquery-ui.js',
        )

    def __init__(self, params='', attrs=None):
        self.params = params
        super(DatePickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(DatePickerWidget, self).render(name, value, attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').datepicker({%s});
            </script>'''%(name, self.params,))


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'bio' : Textarea({'cols':40, 'rows':10}),
            'other_contacts' : Textarea({'cols':40, 'rows':10}),
            'birth_date':DatePickerWidget(params="dateFormat: 'dd.mm.yy', changeYear: true"),
                   }


    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
