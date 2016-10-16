from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader

def index(request):
	return render(request, 'index.html')

from .forms import usersForm
def users(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = NameForm(request.POST)
                # check whether it's valid:
                # process the data in form.cleaned_data as required
                # redirect to a new URL:
                name = json.dumps(form.data['user_name'])
                request.session['name'] = name
                return redirect('/users' )

        # if a GET (or any other method) we'll create a blank form
        else:
                form = NameForm()
        return render(request, 'users', {'form': form})
		
from .forms import equipmentForm
def equipment(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = NameForm(request.POST)
                # check whether it's valid:
                # process the data in form.cleaned_data as required
                # redirect to a new URL:
                name = json.dumps(form.data['manuf_email'])
                request.session['name'] = name
                return redirect('/equipment' )

        # if a GET (or any other method) we'll create a blank form
        else:
                form = NameForm()
        return render(request, 'equipment', {'form': form})
		
from .forms import serverForm
def server(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = NameForm(request.POST)
                # check whether it's valid:
                # process the data in form.cleaned_data as required
                # redirect to a new URL:
                name = json.dumps(form.data['bool_field'])
                request.session['name'] = name
                return redirect('/server' )

        # if a GET (or any other method) we'll create a blank form
        else:
                form = NameForm()
        return render(request, 'server', {'form': form})
