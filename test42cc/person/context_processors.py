# -*- coding: utf-8 *-*
from django.conf import settings

def SettingsToContext(request):
    return {'SETTINGS':settings}
