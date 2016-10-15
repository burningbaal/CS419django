from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^(?:index\.?[html]{,4})?$', views.index, name='index'),
#	url(r'^index$', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
