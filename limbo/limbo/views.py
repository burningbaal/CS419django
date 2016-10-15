from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse

def index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render(context, request))

from .forms import formTest
def testForm(request):
	if request.method == 'POST':
		form = formTest(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/polls/thanks/')
	else:
		form = formTest()
	return render(request, 'polls/formTest', {'form': form})
