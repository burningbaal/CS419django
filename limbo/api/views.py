from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
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
	if request.method == 'POST':
		form = usageHistoryForm(request.POST)
		if form.is_valid():
			newUse = form.save()
			message = HttpResponse('{"Added":{"user":' + \
			serializers.serialize('json', [newUse.FK_user.user, ]) +  ',"version":' + \
			serializers.serialize('json', [newUse.FK_version, ]) +  ',"instrument":' + \
			serializers.serialize('json', [newUse.FK_instrument, ]) +  ',"timestamp":' + \
			'"' + str(newUse.timestamp) + '"' +  \
			'}}')
			return HttpResponse(message)
		else:
			message = '{"Error": ["Message":"The use history has NOT been added.",' + '\n'
			message += '"Details":"' + ', '.join("%s=%r" % (key,val) for (key,val) in form.errors.iteritems()) + '"]}' 
			return HttpResponse(message)
	message = '{"Error":"Data must be POSTed},"Method":"' + request.method + '"}'
	return HttpResponse(message)


@csrf_exempt
@api_view(['GET', 'POST'])
def getUsageHistory(request):
	numberRequested = 10 # default number
	if request.method == 'POST':
		numberRequested = request.POST.get('number_histories', numberRequested)
	elif request.method == 'GET':
		numberRequested = request.GET.get('number_histories', numberRequested)
	#print out numberRequested entries (most recent first)
	uses = UsageHistory.objects.order_by('timestamp')[:5]
	message = '{"uses": ['
	counter = 0
	for curUse in uses:
		if (counter > 0):
			message += ','
		counter += 1
		message += '{"Added":{"user":' + \
		serializers.serialize('json', [curUse.FK_user.user, ]) +  ',"version":' + \
		serializers.serialize('json', [curUse.FK_version, ]) +  ',"instrument":' + \
		serializers.serialize('json', [curUse.FK_instrument, ]) +  ',"timestamp":' + \
		'"' + str(curUse.timestamp) + '"' +  \
		'}}'
	message += ']}'
	return HttpResponse(message)
	
	