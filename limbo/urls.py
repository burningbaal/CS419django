from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^polls/', include('polls.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^index.html$', include('polls.urls'))
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

