from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader
from limboLogic import *

def index(request):
	return render(request, 'index.html')


def editUsers(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = usersForm(request.POST)
		# check whether it's valid:
		# process the data in form.cleaned_data as required
		# redirect to a new URL:
		name = json.dumps(form.data['user_name'])
		request.session['editUserName'] = name
		
		# call out to limboLogic.py to update values
		
		test = name
		return redirect('limbo.views.users', name )
	# if a GET (or any other method) we'll create a blank form
	else:
		return redirect('limbo.views.users')

from .forms import usersForm

def users(request, name):
	form = usersForm(initial=limboLogic.GetUserInfo(name))
	return render(request, 'limboHtml/UserManagement.html', {'form': form})

def users(request):
	# create a blank form
	form = usersForm()
	return render(request, 'limboHtml/UserManagement.html', {'form': form})
		
def editEquipment(request):
	return HttpHttpResponse("This capability isn't built yet, please go back")
from .forms import equipmentForm
def equipment(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = equipmentForm(request.POST)
                # check whether it's valid:
                # process the data in form.cleaned_data as required
                # redirect to a new URL:
                name = json.dumps(form.data['manuf_email'])
                request.session['name'] = name
                return redirect('/equipment' )

        # if a GET (or any other method) we'll create a blank form
        else:
                form = equipmentForm()
        return render(request, 'limboHtml/EquipmentManagement.html', {'form': form})
		
def editServer(request):
	return HttpHttpResponse("This capability isn't built yet, please go back")
from .forms import serverForm
def server(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = serverForm(request.POST)
                # check whether it's valid:
                # process the data in form.cleaned_data as required
                # redirect to a new URL:
                name = json.dumps(form.data['bool_field'])
                request.session['name'] = name
                return redirect('/server' )

        # if a GET (or any other method) we'll create a blank form
        else:
                form = serverForm()
        return render(request, 'limboHtml/ServerConfiguration.html', {'form': form})
