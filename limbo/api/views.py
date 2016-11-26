from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers as coreSerializers
import json
from django.http import QueryDict
from django.template import loader
from django.conf import settings
from django.contrib.auth import authenticate, login

from forms import *
from limbo.models import *
from limbo.serializers import *
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication 
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

@csrf_exempt
@api_view(['GET', 'POST'])
def addUsageHistory(request):	
	userResponse = ''
	response = ''
	
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)
	user = None
	user = authenticate(username=username, password=password)
	if user is None:
		return HttpResponse('{"Error":"Must log in with valid \'username\' and \'password\'"}', status=401) 
	#serial = UserProfileSerializer(user)
	#userResponse = JSONRenderer().render(serial.data)
	
	if request.method == 'POST':
		form = usageHistoryForm(request.POST)
		if form.is_valid():
			newUse = form.save()
			message = ('{"Added":{"user":' + \
			coreSerializers.serialize('json', [newUse.FK_user.user, ]) +  ',"version":' + \
			coreSerializers.serialize('json', [newUse.FK_version, ]) +  ',"instrument":' + \
			coreSerializers.serialize('json', [newUse.FK_instrument, ]) +  ',"timestamp":' + \
			'"' + str(newUse.timestamp) + '"' +  \
			'}}')
			return HttpResponse(message, status=201)
		else:
			message = '{"Error": ["Message":"The use history has NOT been added.",' + '\n'
			message += '"Details":"' + ', '.join("%s=%r" % (key,val) for (key,val) in form.errors.iteritems()) + '"]}' 
			return HttpResponse(message, status=400)
	message = '{"Error":"Data must be POSTed},"Method":"' + request.method + '"}'
	return HttpResponse(message, status=201)


@csrf_exempt
@api_view(['GET', 'POST'])
def getUsageHistory(request):
	numberRequested = 10 # default number
	message = ''
	counter = 0
	userResponse = ''
	response = ''
	
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)
	user = None
	user = authenticate(username=username, password=password)
	if user is None:
		return HttpResponse('{"Error":"Must log in with valid \'username\' and \'password\'"}', status=401) 
	#login(request, user))
	#serial = UserProfileSerializer(user)
	#userResponse = JSONRenderer().render(serial.data)
	
	if request.method == 'POST':
		numberRequested = request.POST.get('number_histories', numberRequested)
	elif request.method == 'GET':
		numberRequested = request.GET.get('number_histories', numberRequested)
	#print out numberRequested entries (most recent first)
	uses = UsageHistory.objects.order_by('timestamp')[:numberRequested]
	message += '{"uses": ['
	
	for curUse in uses:
		if (counter > 0):
			message += ','
		counter += 1
		curUser = curUse.FK_user
		serial = UserProfileSerializer(curUser)
		user = JSONRenderer().render(serial.data)
		#coreSerializers.serialize('json', [curUse.FK_user.user, ]) +  ',"version":' + \
		message += '{"number":' + str(counter) + ',"data":{"user":' + \
		user + ',"version":' + \
		coreSerializers.serialize('json', [curUse.FK_version, ]) +  ',"instrument":' + \
		coreSerializers.serialize('json', [curUse.FK_instrument, ]) +  ',"timestamp":' + \
		'"' + str(curUse.timestamp) + '"' +  \
		'}}'
	message += ']}'
	return HttpResponse(message, status=200)
	
	
@csrf_exempt
@api_view(['GET', 'POST'])
def getInstrument(request):
	assetNum = ''
	strInstrument = ''
	userResponse = ''
	response = ''
	
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)
	user = None
	user = authenticate(username=username, password=password)
	if user is None:
		return HttpResponse('{"Error":"Must log in with valid \'username\' and \'password\'"}', status=401) 
	serial = UserProfileSerializer(user)
	userResponse = JSONRenderer().render(serial.data)
	
	if request.method == 'POST':
		assetNum = request.POST.get('asset_number', None)
	if assetNum is None:
		return HttpResponse('{"Error":"Must POST or GET \'asset_number\'"}', status=406)
	try:
		instrumentObj = Instrument.objects.get(asset_number=assetNum)
	except:
		return HttpResponse('{"Error":"asset_number \'' + assetNum + '\' does not exist"}', status=204)
	asset_number = instrumentObj.asset_number
	
	serial = InstrumentSerializer(instrumentObj)#, context={'request': request})
	strInstrument = strInstrument + JSONRenderer().render(serial.data)
	from limbo import checksum
	cs = checksum.setChecksum(instrumentObj)
	strInstrument = '{"checksum":"' + instrumentObj.checksum_string + '",instrument":' + strInstrument + '}'
	response = '{ "user":' + userResponse + '},{' + str(strInstrument) + '}'
	return HttpResponse(strInstrument)
	
	
@api_view(['GET', 'POST'])
@csrf_exempt
def getMethod(request):
	
	strMethod = ''
	userResponse = ''
	response = ''
	
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)
	user = None
	user = authenticate(username=username, password=password)
	if user is None:
		return HttpResponse('{"Error":"Must log in with valid \'username\' and \'password\'"}', status=401) 
		
	serial = UserSerializer(user)
	userResponse = JSONRenderer().render(serial.data)
	
	if request.method == 'POST':
		method = request.POST.get('method', None)
	if method is None:
		return HttpResponse('{"Error":"Must POST or GET \'method\'"}', status=406)
	try:
		methodObj = Method.objects.get(pk=method)
	except:
		return HttpResponse('{"Error":"method \'' + method + '\' does not exist"}', status=204)
	methodName = methodObj.name
	
	serial = MethodVersionSerializer(methodObj)#, context={'request': request})
	strMethod = strMethod + JSONRenderer().render(serial.data)
	response = '{ "user":' + userResponse + ',"Method":' + str(strMethod) + '}'
	return HttpResponse(response)
	
	
	