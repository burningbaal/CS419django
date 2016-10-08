from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.http import QueryDict
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello, world. You're at Limbo's polls index.")

from .forms import formTest
def testForm(request):
	if request.method == 'POST':
		form = formTest(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/polls/thanks/')
	else:
		form = formTest()
	return render(request, 'polls/formTest', {'form': form})
def testFormResults(request):
	text = "request: " + request.method
	text = text + '\n' + request.session.get('name')
	# name=kwargs['name']
	# text = text + name
	# text = text + '\r'.join('{}: {}'.format(k,v) for k, v in request.headers.items())
	return HttpResponse(text)
from .forms import NameForm
def get_name(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		# process the data in form.cleaned_data as required
		# redirect to a new URL:
		name = json.dumps(form.data['your_name'])
		request.session['name'] = name
		return redirect('/polls/testFormResults' )
		# return HttpResponseRedirect(reverse('/polls/testFormResults', kwargs={'name': name}))
	
	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()
	return render(request, 'name.html', {'form': form})
