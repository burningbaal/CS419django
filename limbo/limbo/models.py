from django.db import models

class serverConfig(models.Model):
	
	config_key = models.CharField(max_length=63)
	config_value = models.CharField(max_length=63)

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

# class User(models.Model):
	# first_name = models.CharField(max_length=50)
	# last_name = models.CharField(max_length=50)
	# email = models.CharField(max_length=50, unique=True)
	# active = models.BooleanField(default=True)
	# User_Version = models.ManyToManyField(
						# Version, 
						# through='User_Version', 
						# related_name='User_Version', 
						# through_fields=('FK_user', 'FK_version'),
					# )
	# User_Permission = models.ManyToManyField(
						# Permission, 
						# through='User_Permission', 
						# related_name='User_Permission', 
						# through_fields=('FK_user', 'FK_permission'),
					# )

# class Role(models.Model):
	# title = models.CharField(max_length=50, unique=True)
	# Role_Permission = models.ManyToManyField(
						# Permission, 
						# through='Role_Permission', 
						# related_name = 'Role_Permission',
					# )

# class Permission(models.Model):
	# name = models.CharField(max_length=50, unique=True)

class Instr_Version(models.Model):
	FK_version = models.ForeignKey(Version, on_delete=models.CASCADE)
	FK_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
	validating_user = models.ForeignKey(auth_user, on_delete=models.models.PROTECT)
	timestamp = models.DateField(auto_now_add=True)

	class Meta:
		unique_together = ('FK_version', 'FK_instrument')

class User_Version(models.Model):
	FK_version = models.ForeignKey(Version, on_delete=models.CASCADE)
	FK_user = models.ForeignKey(auth_user, on_delete=models.CASCADE)
	validating_user = models.ForeignKey(auth_user, on_delete=models.PROTECT)
	timestamp = models.DateField(auto_now_add=True)

	class Meta:
		unique_together = ('FK_version', 'FK_user')

# class User_Permission(models.Model):
	# FK_user = models.ForeignKey(auth_user, on_delete=models.CASCADE)
	# FK_permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
	# validating_user = models.ForeignKey(auth_user, on_delete=models.PROTECT)
	# timestamp = models.DateField(auto_now_add=True)
	
	# class Meta:
		# unique_together = ('FK_user', 'FK_permission')

# class Role_Permission(models.Model):
	# FK_role = ForeignKey(Role, on_delete=models.CASCADE)
	# FK_permission = ForeignKey(Permission, on_delete=models.CASCADE)

	# class Meta:
		# unique_together = ('FK_role', 'FK_permission')

class UsageHistory(models.Model):
	FK_user = models.ForeignKey(auth_user, on_delete=models.PROTECT)
	FK_version = models.ForeignKey(Version, on_delete=models.PROTECT)
	FK_instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
	timestamp = models.DateField(auto_now_add=True)