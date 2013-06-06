# -*- coding: utf-8 -*-
from django.conf import settings

def media(context):
    return {'MEDIA_URL': settings.MEDIA_URL}


