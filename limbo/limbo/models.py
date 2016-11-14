from django.db import models
from django.conf import settings
from datetime import datetime 

class serverConfig(models.Model):
	
	config_key = models.CharField(max_length=63)
	config_value = models.CharField(max_length=63)
	
class UserProfile(models.Model):
	def __str__(self):
		return user.last_name + ', ' + user.first_name
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	
	
class InstrType(models.Model):
	def __str__(self):
		return self.make + ' ' + self.model
	make = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	service_email = models.CharField(max_length=50, null=True)
	service_website = models.CharField(max_length=50, null=True)

class Method(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=50, unique=True)
	descripton = models.TextField(null=False)

class Version(models.Model):
	def __str__(self):
		return self.FK_method.name + ' ' + self.version_number
	version_number = models.CharField(max_length=50)
	cmd_line_script = models.TextField(null=False)
	SOP = models.TextField(null=False)
	FK_method = models.ForeignKey(Method, on_delete=models.CASCADE)
	
	class Meta:
		unique_together = ('version_number', 'FK_method')

class Instrument(models.Model):
	def __str__(self):
		return self.asset_number + ': ' + self.name
	serial_number = models.CharField(max_length=50, unique=True)
	asset_number = models.CharField(max_length=50, unique=True)
	name = models.CharField(max_length=50)
	checksum_string = models.CharField(max_length=128, null=True)
	FK_instr_type = models.ForeignKey(InstrType, related_name='installations', on_delete=models.PROTECT)
	VersionsFromInstrument = models.ManyToManyField(
						Version, 
						through='Instr_Version', 
						related_name = 'InstrumentsFromVersion',
					)

class Instr_Version(models.Model):
	FK_version = models.ForeignKey(Version, related_name='versions', on_delete=models.CASCADE)
	FK_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
	validating_user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
	timestamp = models.DateField(auto_now_add=True)

	class Meta:
		unique_together = ('FK_version', 'FK_instrument')

class User_Version(models.Model):
	FK_version = models.ForeignKey(Version, on_delete=models.CASCADE)
	FK_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	authorizing_user = models.ForeignKey(UserProfile, related_name='+', on_delete=models.PROTECT)
	timestamp = models.DateField(auto_now_add=True)

	class Meta:
		unique_together = ('FK_version', 'FK_user')

# class Role_Permission(models.Model):
	# FK_role = ForeignKey(Role, on_delete=models.CASCADE)
	# FK_permission = ForeignKey(Permission, on_delete=models.CASCADE)

	# class Meta:
		# unique_together = ('FK_role', 'FK_permission')

class UsageHistory(models.Model):
	FK_user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
	FK_version = models.ForeignKey(Version, on_delete=models.PROTECT)
	FK_instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
	timestamp = models.DateTimeField(default=datetime.now, blank=True) 

