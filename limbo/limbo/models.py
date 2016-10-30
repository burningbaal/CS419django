from django.db import models

class serverConfig(models.Model):
	
	config_key = models.CharField(max_length=63, editable = False)
	config_value = models.CharField(max_length=63)
