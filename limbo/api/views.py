from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader

from forms import *
from limbo.models import *
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication 
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['GET', 'POST'])
def addUsageHistory(request):
	# authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	#result = usageHistory.objects.create(pk=id)
	#myConfigs = [entry for entry in result]
	
	if request.method == 'POST':
		form = usageHistoryForm(request.POST)
		if form.is_valid():
			FK_usr = form.cleaned_data['FK_user']
			FK_ver = form.cleaned_data['FK_version']
			FK_isntr = form.cleaned_data['FK_instrument']
			time = form.cleaned_data['timestamp']
			message = HttpResponse(serializers.serialize("json", usageHistory.objects.filter(pk=usageHistory.Id)))
			HttpResponse(message)
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

