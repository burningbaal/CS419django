from django.db import models

class serverConfig(models.Model):
	
	config_key = models.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	config_value = models.CharField(max_length=63)
