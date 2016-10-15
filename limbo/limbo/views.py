from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader

def index(request):
	return render(request, 'index.html')
#	template = loader.get_template('index.html')
#	return HttpResponse(template.render(context, request))

