from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader
from limboLogic import *

from forms import *
from limbo.models import *
from django.forms import modelformset_factory
from django.forms import formset_factory

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
			message += ', '.join("%s=%r" % (key,val) for (key,val) in form.errors.iteritems()) + '\n' 
			message += '<br> ' + ", ".join("%s=%r" % (key,val) for(key,val) in form.iteritems()) 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in form.non_field_errors.iteritems()) + '\n' 
			return render(request, 'limboHtml/ServerConfiguration.html', {'form': form, 'SubmitMessage': message, 'CurrentConfigs': myConfigs})
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['integer']
	except KeyError:
		pass
	
	return render(request, 'limboHtml/ServerConfiguration.html', {'formset': finalFormSet, 'SubmitMessage': '', 'CurrentConfigs': myConfigs})

