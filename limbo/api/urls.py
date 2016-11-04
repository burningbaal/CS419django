from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from rest_framework.authtoken import views

urlpatterns = [
	url(r'^addUse.html$', views.addUsageHistory, name='addUsageHistory'),
	url(r'^api-token-auth/', views.obtain_auth_token),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
