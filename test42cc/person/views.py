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


@login_required()
def edit(request):
    try:
        info = Person.objects.get(pk=1)
    except Person.DoesNotExist:
        return render(request, 'index.html', {'info': None})

    if request.is_ajax():#submit ajax form
        form = PersonForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            if request.FILES:
                form.cleaned_data['photo'] = request.FILES['photo']
            form.save()
            return render(request, 'edit.html', locals()) # Redirect after POST

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            if request.FILES:
                form.cleaned_data['photo'] = request.FILES['photo']
            form.save()
            return HttpResponseRedirect(reverse(index)) # Redirect after POST
    else:
        form = PersonForm(instance=info)
        return render(request, 'edit.html', locals())


def storedRequests(request):
    try:
        req = HttpStoredQuery.objects.all().order_by('date_with_time')[:10]
    except HttpStoredQuery.DoesNotExist:
        req = []
    return render(request, 'requests.html', {'request_list': req})


def create_new_account(request):
    """
    View for saving new Person entry
    :param request:
    :return:
    """
    if request.is_ajax():
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                form.cleaned_data['photo'] = request.FILES['photo']
            form.save()
            return HttpResponse(json.dumps({'status': 0}))
        else:
            errors = form.errors
            print errors
            #print locals()
            return HttpResponse(json.dumps({'status': 1, 'errors': errors}))
        #return render(request, 'edit.html', {'errors': errors})
    else:
        form = PersonForm()
        return render(request, 'edit.html', locals())