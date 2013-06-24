# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, Context
import json
from models import Person, HttpStoredQuery
from forms import PersonForm


def index(request):
    try:
        info = Person.objects.get(pk=1)
    except Person.DoesNotExist:
        info = None
    return render(request, 'index.html', {'info': info})


def storedRequests(request):
    try:
        req = HttpStoredQuery.objects.all().order_by('date_with_time')[:10]
    except HttpStoredQuery.DoesNotExist:
        req = []
    return render(request, 'requests.html', {'request_list': req})


def create_new_account(request, itemId=None):
    """
    View for saving new Person entry
    :param itemId:
    :param request:
    :return:
    """
    entry = None
    try:
        itemId = request.path.strip().split('/')[2:3][0]
        entry = Person.objects.get(id=int(itemId))
    except ValueError:
        pass

    if request.is_ajax():
        form = PersonForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            if request.FILES:
                form.cleaned_data['photo'] = request.FILES['photo']
            form.save()
            return HttpResponse(json.dumps(dict(status=0, redirect=reverse('persons'))))
        else:
            errors = form.errors
            return HttpResponse(json.dumps({'status': 1, 'errors': errors}))
    else:
        form = PersonForm(instance=entry)
        return render(request, 'edit.html', locals())


def persons_lists(request):
    """
    Render page with 10 entries of Person Model
    :param request:
    :return:
    """
    try:
        req = Person.objects.all().order_by('-id')[:10]
    except Person.DoesNotExist:
        req = []
    return render(request, 'persons_list.html', {'list_info': req})