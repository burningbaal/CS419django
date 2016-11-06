from rest_framework import serializers

class serverConfigSerializer(serializers.ModelSerializer):
	class Meta:
		model = serverConfig
		fields = ('config_key', 'config_value')
	
class UserProfileSerializer(serializers.ModelSerializer):
    #user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	class Meta:
		model = UserProfile.user
		fields = ('last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')
	
class InstrTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = InstrType
		fields = ('make', 'model', 'service_email', 'servie_website')

class MethodSerializer(serializers.ModelSerializer):
	class Meta:
		model = Method
		fields = ('name', 'descriton')

class VersionSerializer(serializers.ModelSerializer):
	method = MethodSerializer(read_only=True)
	class Meta:
		model = Version
		fields = ('version_number', 'cmd_line_script', 'SOP', 'method')
	
	#class Meta:
		#unique_together = ('version_number', 'FK_method')

class Instr_VersionSerializer(serializers.ModelSerializer):
	version = VersionSerializer(read_only=True)
	instrument = InstrumentSerializer(read_only=True)
	validating_user = UserProfileSerializer(read_only=True)
	
	class Meta:
		model = Instr_Version
		fields = ('version', 'instrument', 'validating_user', 'timestamp')
		
class InstrumentSerializer(serializers.ModelSerializer):
	instr_type = InstrTypeSerializer(read_only=True)
	Instr_Version = InstrTypeSerializer(many=True, read_only=True)
	
	class Meta:
		model = Instrument
		fields = ('serial_number', 'asset_number', 'name', 'checksum', 'instr_type', 'Instr_Version')


class User_VersionSerializer(serializers.ModelSerializer):
	FK_version = models.ForeignKey(Version, on_delete=models.CASCADE)
	FK_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	authorizing_user = models.ForeignKey(UserProfile, related_name='+', on_delete=models.PROTECT)
	timestamp = models.DateField(auto_now_add=True)

	class Meta:
		unique_together = ('FK_version', 'FK_user')

class UsageHistorySerializer(serializers.ModelSerializer):
	FK_user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
	FK_version = models.ForeignKey(Version, on_delete=models.PROTECT)
	FK_instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
	timestamp = models.DateTimeField(default=datetime.now, blank=True) 

