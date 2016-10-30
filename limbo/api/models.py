from django.db import models

class usageHistory(models.Model):
	
	fk_employee_number = models.CharField(max_length=63)
	fk_version = models.CharField(max_length=63)
	fk_instrument = models.CharField(max_length=63)
	timestamp = models.date(max_length=63)
