from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^api/', include('api.urls')),
	url(r'^polls/', include('polls.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^(edit/)*(?:index\.?[html]{,4})?$', views.indexLimbo, name='indexLimbo'),
	url(r'^edit/users.html$', views.editUsers, name='editUsers'),
	url(r'^edit/equipment.html$', views.editEquipment, name='editEqiupment'),
	url(r'^edit/server.html$', views.editServer, name='editServer'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
