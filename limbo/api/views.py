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

def addUsageHistory(request):
	result = usageHistory.objects.values()
	myConfigs = [entry for entry in result]
	
	finalFormSet = modelformset_factory(usageHistory, exclude=('none'), extra=0) # intentionally not a tuple
	if request.method == 'POST':
		formset = finalFormSet(request.POST, request.FILES)
		if formset.is_valid():
			for form in formset:
				form.save()
			
			message = HttpResponse(serializers.serialize("json", usageHistory.objects.filter(pk=usageHistory.Id)))
			HttpResponse(message)
			#return render(request, 'limboHtml/ServerConfiguration.html', {'formset': finalFormSet, 'SubmitMessage': '', 'CurrentConfigs': myConfigs})
		else:
			message = '{"Error": ["Message":"The server configuration has NOT been updated.",' + '\n'
			message += '"Details":"' + ', '.join("%s=%r" % (key,val) for (key,val) in form.errors.iteritems()) + '"]}' 
			#message += '<br> ' + ", ".join("%s=%r" % (key,val) for(key,val) in form.iteritems()) 
			HttpResponse(message)
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['integer']
	except KeyError:
		pass
	message = '{"Error":"Data must be POSTed"}'
	return HttpResponse(message)

