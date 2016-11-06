from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from rest_framework.authtoken import views as restFwViews

urlpatterns = [
	url(r'^addUse/', views.addUsageHistory, name='addUsageHistory'),
	url(r'^getUse/', views.getUsageHistory, name='getUsageHistory'),
	url(r'^getInstrument/', views.getInstrument, name='getInstrument'),
	url(r'^api-token-auth/', restFwViews.obtain_auth_token),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
