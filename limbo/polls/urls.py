from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^index.html$', views.index, name='index'),
	url(r'^formTest$', views.testForm, name='testForm'),
	url(r'^name-test.html$', views.get_name, name='getName'),
	url(r'^testFormResults/',
		# <string>[\w\-]+)/$',
		views.testFormResults,
		name='showFormResults'),
#        url(r'^static/$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT},
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

