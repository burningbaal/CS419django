from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader

def GetUserInfo():
	userInfo = []
	userPermissions = []
	userInfo['userName'] = 'John Doe'
	userInfo['userEmali'] = 'JDoe@acme.net'
	
	userPermissions['operator'] = True
	userPermissions['editUsers'] = True
	userPermissions['editEquipment'] = True
	
	userInfo['userPermissions'] = userPermissions
	
	return userInfo