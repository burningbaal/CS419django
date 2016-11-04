from django.db import models
from datetime import datetime    
from django.conf import settings
from limbo.limbo import UserProfile

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
class usageHistory(models.Model):
	
	fk_employee_number = models.BigIntegerField()
	fk_version = models.BigIntegerField()
	fk_instrument = models.BigIntegerField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)

	
# remove this after first compile, it's just to create the already-existing set of users' tokens

for user in UserProfile.objects.all():
    Token.objects.get_or_create(user=user)