# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, Context
from models import Person
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
        return render(request,'index.html',{'info':None})

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                form.cleaned_data['photo'] = request.FILES['photo']
            form.save()
            return HttpResponseRedirect(reverse(index)) # Redirect after POST
    else:
        form = PersonForm(instance=info)
        return render(request, 'edit.html', locals())