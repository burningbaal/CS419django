from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from myproject.admin import admin_site


urlpatterns = [
	url(r'^admin/', admin_site.site.urls),
	url(r'^api/', include('api.urls')),
	url(r'^polls/', include('polls.urls')),
	#url(r'edit/', include('limbo.urls')),
	url(r'^$', lambda _: redirect('admin_site:index')),
	#url(r'$', include('limbo.urls')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

