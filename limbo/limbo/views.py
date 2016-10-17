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
	# request.session.flush()
	return render(request, 'index.html')


def editUsers(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = usersForm(request.POST)
		# check whether it's valid:
		# process the data in form.cleaned_data as required
		# redirect to a new URL:
		if form.is_valid():
			name = form.cleaned_data['user_name']
			request.session['editUserName'] = name
			
			# call out to limboLogic.py to update values, add them to the session
			
			return redirect('../users')
	# if a GET (or any other method) we'll create a blank form
	request.session.flush()
	return redirect('../users')

from .forms import *

def users(request):
	form = None
	if 'editUserName' not in request.session:
		# create a blank form
		form = usersForm()
	else:
		form = usersForm(initial={'user_name':request.session['editUserName']}, auto_id=False) #limboLogic.GetUserInfo(name))
	return render(request, 'limboHtml/UserManagement.html', {'form': form})
		
def editEquipment(request):
	if request.method == 'POST':
		form = equipmentForm(request.POST)
		if form.is_valid():
			manuf_email = form.cleaned_data['manuf_email']
			request.session['editEquipId'] = manuf_email
			
			# call out to limboLogic.py to update values, add them to the session
			
			return redirect('../equipment')
	# if a GET (or any other method) we'll create a blank form
	return redirect('../equipment')

def equipment(request):
	form = None
	if 'editEquipId' not in request.session:
		# create a blank form
		form = equipmentForm()
	else:
		form = equipmentForm(initial={'manuf_email':request.session['editEquipId']}, auto_id=False) #limboLogic.GetUserInfo(name))
	return render(request, 'limboHtml/EquipmentManagement.html', {'form': form})
	
		
def editServer(request):
	if request.method == 'POST':
		form = serverForm(request.POST)
		if form.is_valid():
			bool = form.cleaned_data['bool']
			request.session['editEquipId'] = bool
			
			# call out to limboLogic.py to update values, add them to the session
			
			return redirect('../server')
	# if a GET (or any other method) we'll create a blank form
	return redirect('../server')

def server(request):
	form = None
	if 'editEquipId' not in request.session:
		# create a blank form
		form = serverForm()
	else:
		form = serverForm(initial={'bool_field':request.session['bool']}, auto_id=False) #limboLogic.GetUserInfo(name))
	return render(request, 'limboHtml/serverConfiguration.html', {'form': form})
	