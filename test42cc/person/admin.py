# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *


class PersonAdmin(admin.ModelAdmin):
    pass

class HttpStoredQueryAdmin(admin.ModelAdmin):
    list_display = ['path', 'method','user','date_with_time']

class ModelsActionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)
admin.site.register(HttpStoredQuery, HttpStoredQueryAdmin)
admin.site.register(ModelsActions, ModelsActionsAdmin)