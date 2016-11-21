from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.indexLimbo, name='indexLimbo'),
	url(r'^logout/$', views.logoutLimbo, name='logoutLimbo'),
	url(r'^index/$', views.indexLimbo, name='indexLimbo'),
	url(r'^index$', views.indexLimbo, name='indexLimbo'),
	url(r'^index.html$', views.indexLimbo, name='indexLimbo'),
	url(r'^users.html$', views.editUsers, name='editUsers'),
	url(r'^index/logout/$', views.logoutLimbo, name='logoutLimbo'),
	url(r'^methods.html$', views.editMethods, name='editMethods'),
	url(r'^equipment.html$', views.editEquipment, name='editEqiupment'),
	url(r'^method$', views.goToMethod, name='goToMethod'),
	url(r'^method/(?P<methodId>\d+)/$', views.editMethod, name='editMethod'),
	url(r'^equipment/instrument$', views.gotoInstrument, name='gotoInstrument'),
	url(r'^equipment/instrument(?P<pk>\d+)/$', views.editInstrument, name='editInstrument'),
	url(r'^equipment/types$', views.editInstrTypes, name='editInstrTypes'),
	url(r'^server.html$', views.editServer, name='editServer'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
