from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^(edit/)*(?:index\.?[html]{,4})?$', views.indexLimbo, name='indexLimbo'),
	url(r'^(?:users\.?[html]{,4})?$', views.editServer, name='editServer'),
	url(r'^(?:equipment\.?[html]{,4})?$', views.editEquipment, name='editEquipment'),
	url(r'^(?:server\.?[html]{,4})?$', views.editServer, name='editServer'),
	url(r'^edit/users.html$', views.editUsers, name='editUsers'),
	url(r'^edit/equipment.html$', views.editEquipment, name='editEqiupment'),
	url(r'^edit/server.html$', views.editServer, name='editServer'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
