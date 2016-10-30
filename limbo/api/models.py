from django.db import models

class usageHistory(models.Model):
	
	fk_employee_number = models.BigIntegerField()
	fk_version = models.BigIntegerField()
	fk_instrument = models.BigIntegerField()
	timestamp = models.dateTimeField(auto_now=False, auto_now_add=False)
