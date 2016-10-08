from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^index.html$', views.index, name='index'),
	url(r'^formTest$', views.testForm, name='testForm'),
	url(r'^name-test.html$', views.get_name, name='getName'),
	url(r'^testFormResults/',
		# <string>[\w\-]+)/$',
		views.testFormResults,
		name='showFormResults'),
]

