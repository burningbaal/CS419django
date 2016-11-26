from django.db import models
from django.conf import settings
from datetime import datetime 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import escape
from django.core.urlresolvers import reverse

class serverConfig(models.Model):
	
	config_key = models.CharField(max_length=63)
	config_value = models.CharField(max_length=63)
	
class InstrType(models.Model):
	def __str__(self):
		return self.make + ' ' + self.model
	make = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	service_email = models.CharField(max_length=50, null=True)
	service_website = models.CharField(max_length=50, null=True)

	class Meta:
		permissions = (
			("view_InstrType", "Can view instr type"),
		)
		verbose_name_plural = 'Instrument Types'

class Method(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=False)

	class Meta:
		permissions = (
			("view_Method", "Can view method"),
		)

class Version(models.Model):
	def __str__(self):
		return self.FK_method.name + ' ' + self.version_number
	version_number = models.CharField(max_length=50)
	cmd_line_script = models.TextField(null=False, verbose_name='Command Line Script')
	SOP = models.TextField(null=False, verbose_name='Standard Operating Procedure')
	FK_method = models.ForeignKey(Method, on_delete=models.CASCADE)
	#authorized_users = models.ManyToManyField(UserProfile, through='UserProfile_Version', through_fields=('FK_version', 'FK_userProfile',), related_name='authorized_MethodVersions', )
	
	class Meta:
		unique_together = ('version_number', 'FK_method')
		permissions = (
			("view_Version", "Can view version"),
		)

class UserProfile(models.Model):
	def __str__(self):
		try:
			return self.user.last_name + ', ' + self.user.first_name
		except:
			return self.user.username
	
	NEW_HIRE = 1
	ASSOCIATE = 2
	ASSISTANT = 3
	TITLE_CHOICES = (
		(NEW_HIRE, 'New Hire'),
		(ASSOCIATE, 'Associate'),
		(ASSISTANT, 'Assistant'),
	)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	title = models.CharField(max_length=50, choices=TITLE_CHOICES, default=NEW_HIRE, null=False, blank=False)
	trained = models.ManyToManyField(Version, through='UserProfile_Version', through_fields=('userProfile', 'version',),)
	
	def user_link(self):
		return '<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(self.user.id,)) , escape(self.user))
	user_link.allow_tags = True
	user_link.short_description = "Edit User"
	
	def username(self):
		return self.user.username
	def first_name(self):
		return self.user.first_name
	def last_name(self):
		return self.user.last_name
	
	class Meta:
		permissions = (
			("view_UserProfile", "Can view user profile"),
		)
		verbose_name_plural = 'User Profiles'
	
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
	try:
		instance.UserProfile.save()
	except:
		pass #UserProfile.objects.create(user=instance)

from limbo import checksum
class Instrument(models.Model):
	def __str__(self):
		return self.asset_number + ': ' + self.name
	serial_number = models.CharField(max_length=50, unique=True)
	asset_number = models.CharField(max_length=50, unique=True)
	name = models.CharField(max_length=50)
	checksum_string = models.CharField(max_length=128, null=True, verbose_name='Checksum')
	FK_instr_type = models.ForeignKey(InstrType, related_name='installations', on_delete=models.PROTECT, verbose_name='Instrument Type')
	VersionsFromInstrument = models.ManyToManyField(
						Version, 
						through='Instr_Version', 
						related_name = 'InstrumentsFromVersion',
					)
	
	def save(self, force_insert=False, force_update=False):
		super(Instrument, self).save(*args, **kwargs) 
		try:
			checksum = setChecksum(self)
		except:
			pass
		
	class Meta:
		permissions = (
			("view_Instrument", "Can view instrument"),
		)

class Instr_Version(models.Model):
	FK_version = models.ForeignKey(Version, on_delete=models.CASCADE, verbose_name='Version')
	FK_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, verbose_name='Instrument')
	validating_user = models.ForeignKey(UserProfile, related_name='user_instruments_granted', on_delete=models.PROTECT)
	timestamp = models.DateField(auto_now_add=True)

	class Meta:
		unique_together = ('FK_version', 'FK_instrument')
		permissions = (
			("view_Instr_Version", "Can view instr_version"),
		)
		verbose_name = 'Validated Version'
		verbose_name_plural = 'Validated Versions'
		

class UserProfile_Version(models.Model):
	version = models.ForeignKey(Version, on_delete=models.CASCADE)
	userProfile = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
	authorizing_user = models.ForeignKey(UserProfile, related_name='userProfile_versions_granted', on_delete=models.PROTECT)
	timestamp = models.DateField(auto_now_add=True)
	
	def __str__(self):
		return str(self.userProfile) + ' is trained on ' + str(self.version)

	class Meta:
		unique_together = ('version', 'userProfile')
		verbose_name ='Authorized version'
		verbose_name_plural ='Authorized versions'

# class Role_Permission(models.Model):
	# FK_role = ForeignKey(Role, on_delete=models.CASCADE)
	# FK_permission = ForeignKey(Permission, on_delete=models.CASCADE)

	# class Meta:
		# unique_together = ('FK_role', 'FK_permission')

class UsageHistory(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
	version = models.ForeignKey(Version, on_delete=models.PROTECT)
	instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
	timestamp = models.DateTimeField(default=datetime.now, blank=True) 

	class Meta:
		permissions = (
			("view_UsageHistory", "Can view usage history"),
		)
		verbose_name_plural = 'Usage History Logs'

