from django.db import models
from django.conf import settings

class serverConfig(models.Model):
	
	config_key = models.CharField(max_length=63)
	config_value = models.CharField(max_length=63)
	
class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
	
class InstrType(models.Model):
	make = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	service_email = models.CharField(max_length=50, null=True)
	servie_website = models.CharField(max_length=50, null=True)

class Method(models.Model):
	name = models.CharField(max_length=50, unique=True)
	descriton = models.TextField(null=False)

class Version(models.Model):
	version_number = models.CharField(max_length=50)
	cmd_line_script = models.CharField(max_length=250, null=False)
	SOP = models.TextField(null=False)
	FK_method = models.ForeignKey(Method, on_delete=models.CASCADE)
	
	class Meta:
		unique_together = ('version_number', 'FK_method')

class Instrument(models.Model):
	serial_number = models.CharField(max_length=50, unique=True)
	asset_number = models.CharField(max_length=50, unique=True)
	name = models.CharField(max_length=50)
	checksum = models.BinaryField
	FK_instr_type = models.ForeignKey(InstrType, on_delete=models.PROTECT)
	Instr_Version = models.ManyToManyField(
						Version, 
						through='Instr_Version', 
						related_name = 'Instr_Version',
					)

class Instr_Version(models.Model):
	FK_version = models.ForeignKey(Version, on_delete=models.CASCADE)
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
	timestamp = models.DateField(auto_now_add=True)