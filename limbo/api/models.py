from django.db import models
from datetime import datetime    

class usageHistory(models.Model):
	
	fk_employee_number = models.BigIntegerField()
	fk_version = models.BigIntegerField()
	fk_instrument = models.BigIntegerField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
