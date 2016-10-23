from django.db import models

class serverConfig(models.Model):
	
	config_key = models.CharField(maxLength=63)
	config_value = models.CharField(maxLength=63)
