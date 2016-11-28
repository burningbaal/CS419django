from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy

# Text to put at the end of each page's <title>.
admin.site.site_title = ugettext_lazy('Limbo')

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = ugettext_lazy('Limbo Equipment Management')

# Text to put at the top of the admin index page.
admin.site.index_title = ugettext_lazy('Limbo Home')
	
urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^api/', include('api.urls')),
	url(r'^polls/', include('polls.urls')),
	#url(r'edit/', include('limbo.urls')),
	url(r'^$', lambda _: redirect('admin:index')),
	#url(r'$', include('limbo.urls')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

