from django.conf.urls import include, url
from django.contrib import admin
from . import api, polls

urlpatterns = [
	url(r'^api/', include('api.urls')),
	url(r'^index$', include('limbo.urls')),
	url(r'^polls/', include('polls.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^limbo/', include('limbo.limbo.urls')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

