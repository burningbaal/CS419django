from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader
from limboLogic import *		
from limbo.models import *
from django.forms import modelformset_factory
from django.forms import formset_factory

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
	formSet = modelformset_factory(Instrument, exclude=('Instr_Version', 'checksum_string',), extra=1)
	
		
	if request.method == 'POST':
		postFormset = formSet(request.POST, request.FILES)
		if postFormset.is_valid():
			for form in postFormset:
				form.save()
			# call out to limboLogic.py to update values, add them to the session
			message = 'The values have been updated.'
			return render(request, 'limboHtml/EquipmentManagement.html', {'formSet': finalFormSet, 'SubmitMessage': message})
		else:
			message = 'The equipment has NOT been updated.' + '\n'
			message += ', '.join("%s=%r" % (key,val) for (key,val) in postFormset.errors.iteritems()) + '\n' 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in postFormset.non_field_errors.iteritems()) + '\n' 
			return render(request, 'limboHtml/EquipmentManagement.html', {'formSet': postFormset, 'SubmitMessage': message})
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['editEquipId']
	except KeyError:
		pass
	#form = GeneralEquipmentForm()
	return render(request, 'limboHtml/EquipmentManagement.html', {'formSet': formSet, 'SubmitMessage': 'testing: 123'})


def editServer(request):
	result = serverConfig.objects.values()
	myConfigs = [entry for entry in result]
	
	finalFormSet = modelformset_factory(serverConfig, exclude=('id',), extra=0)
	
	if request.method == 'POST':
		formset = finalFormSet(request.POST, request.FILES)
		if formset.is_valid():
			for form in formset:
				form.save()
			
			# call out to limboLogic.py to update values, add them to the session
			message = 'The values have been updated.'
			return render(request, 'limboHtml/ServerConfiguration.html', {'formset': finalFormSet, 'SubmitMessage': '', 'CurrentConfigs': myConfigs})
		else:
			message = 'The server configuration has NOT been updated.' + '\n'
			message += ', '.join("%s=%r" % (key,val) for (key,val) in formset.errors.iteritems()) + '\n' 
			message += '<br> ' + ", ".join("%s=%r" % (key,val) for(key,val) in formset.iteritems()) 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in formset.non_field_errors.iteritems()) + '\n' 
			return render(request, 'limboHtml/ServerConfiguration.html', {'form': finalFormSet, 'SubmitMessage': message, 'CurrentConfigs': myConfigs})
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['integer']
	except KeyError:
		pass
	
	return render(request, 'limboHtml/ServerConfiguration.html', {'formset': finalFormSet, 'SubmitMessage': '', 'CurrentConfigs': myConfigs})

