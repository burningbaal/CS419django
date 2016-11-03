from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include('api.urls')),
	url(r'^index', include('limbo.urls')),
	#url(r'^polls/', include('polls.urls')),
	# url(r'^limbo/', include('limbo.urls')),
	url(r'edit/', include('limbo.urls')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

