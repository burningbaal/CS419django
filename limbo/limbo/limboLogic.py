from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader
from rest_framework import serializers
from models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile.user
        exclude = (
            'password', 'is_staff', 'groups', 'user_permissions'
        )


def removePasswordObj(data):
	# borrowed from http://stackoverflow.com/a/3405772/4664804
	for key in data:
		try:
			del dict_del[key]
		except KeyError:
			pass
	for child in data.values():
		if isinstance(child, dict):
			removePasswordObj(child, data)
	return data

def removePasswordJson(inputJSON):
	data = json.loads(inputJSON)
	inputJSON = json.dumps(removePasswordObj(data))
	return inputJSON