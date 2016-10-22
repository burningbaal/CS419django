from django.db import models

class serverConfig(models.Model):
	ClientMustVerify = models.NullBooleanField()
	Auditing = models.BooleanField()
