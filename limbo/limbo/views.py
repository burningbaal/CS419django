from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader
from limboLogic import *

def indexLimbo(request, mystery):
	# request.session.flush()
	temp = mystery
	return render(request, 'index.html')


from .forms import *
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
			
			return render(request, 'limboHtml/UserManagement.html', {'form': form, 'SubmitMessage': 'The user \'' + name + '\' has been updated.'})
		else:
			message = 'The user has NOT been updated.' + '\n'
			message += ', '.join("%s=%r" % (key,val) for (key,val) in form.errors.iteritems()) + '\n' 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in form.non_field_errors.iteritems()) + '\n' 
			return render(request, 'limboHtml/UserManagement.html', {'form': form, 'SubmitMessage': message})
		
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['editUserName']
	except KeyError:
		pass
	form = usersForm()
	return render(request, 'limboHtml/UserManagement.html', {'form': form, 'SubmitMessage': ''})

def editEquipment(request):
	if request.method == 'POST':
		form = equipmentForm(request.POST)
		if form.is_valid():
			manuf_email = form.cleaned_data['manuf_email']
			request.session['editEquipId'] = 'jim@billy.com' #manuf_email
			
			# call out to limboLogic.py to update values, add them to the session
			message = 'The equipment \'' + manuf_email + '\' has been updated.'
			return render(request, 'limboHtml/EquipmentManagement.html', {'form': form, 'SubmitMessage': message})
		else:
			message = 'The equipment has NOT been updated.' + '\n'
			message += ', '.join("%s=%r" % (key,val) for (key,val) in form.errors.iteritems()) + '\n' 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in form.non_field_errors.iteritems()) + '\n' 
			return render(request, 'limboHtml/EquipmentManagement.html', {'form': form, 'SubmitMessage': message})
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['editEquipId']
	except KeyError:
		pass
	form = equipmentForm()
	return render(request, 'limboHtml/EquipmentManagement.html', {'form': form, 'SubmitMessage': ''})
		
from .models import serverConfig
def editServer(request):
	myConfigs = serverConfig.objects.all()
	configHtml = ""
	# for item in myConfigs #serverConfig.objects.values()
	#	configHtml += item.config_key + "\t" + item.config_value + "\n"
	
	if request.method == 'POST':
		form = serverForm(request.POST)
		if form.is_valid():
			integer = form.cleaned_data['int_field']
			request.session['integer'] = integer
			
			# call out to limboLogic.py to update values, add them to the session
			message = 'The value \'' + str(integer) + '\' has been updated.'
			return render(request, 'limboHtml/ServerConfiguration.html', {'form': form, 'SubmitMessage': message, 'CurrentConfigs': myConfigs})
		else:
			message = 'The server configuration has NOT been updated.' + '\n'
			message += ', '.join("%s=%r" % (key,val) for (key,val) in form.errors.iteritems()) + '\n' 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in form.non_field_errors.iteritems()) + '\n' 
			return render(request, 'limboHtml/ServerConfiguration.html', {'form': form, 'SubmitMessage': message, 'CurrentConfigs': myConfigs})
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['integer']
	except KeyError:
		pass
	form = serverForm()
	return render(request, 'limboHtml/ServerConfiguration.html', {'form': form, 'SubmitMessage': '', 'CurrentConfigs': configs})
