from rest_framework import serializers
from limbo.models import *

class serverConfigSerializer(serializers.ModelSerializer):
	class Meta:
		model = serverConfig
		fields = '__all__'
	
class UserProfileSerializer(serializers.ModelSerializer):
    #user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	class Meta:
		model = UserProfile.user
		#fields = ('last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')
		excludes = ('password',)
	
class InstrTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = InstrType
		fields = '__all__'

class MethodSerializer(serializers.ModelSerializer):
	class Meta:
		model = Method
		fields = '__all__'

class Instr_VersionSerializer(serializers.ModelSerializer):
	version = serializers.Field(source='FK_version.version_number')
	method = serializers.Field(source='FK_version.method')
	#instr_name = serializers.Field(source='FK_instrument.name')
	instr_asset_number = serializers.Field(source='FK_instrument.asset_number')
	#instr_checksum = serializers.Field(source='FK_instrument.checksum')
	
	class Meta:
		model = Instr_Version
		#fields = ('method', 'version', 'instr_name', 'instr_asset_number', 'instr_checksum', 'validating_user', 'timestamp')
		fields = ('method', 'version', 'instr_asset_number', 'validating_user', 'timestamp')

class VersionSerializer(serializers.ModelSerializer):
	method = MethodSerializer(read_only=True)
	Instr_Version = Instr_VersionSerializer(source='Instr_Version_set', many=True, read_only=True)
	class Meta:
		model = Version
		fields = ('version_number', 'cmd_line_script', 'SOP', 'method', 'Instr_Version')


class InstrumentSerializer(serializers.ModelSerializer):
	instr_type = InstrTypeSerializer(source='FK_instr_type', read_only=True)
	#Instr_Version = Instr_VersionSerializer(source='Instr_Version_set', many=True, read_only=True)
	
	class Meta:
		model = Instrument
		fields = ('id', 'asset_number', 'serial_number', 'name', 'checksum_string', 'instr_type')
			#{
			#'self': ('id', 'asset_number', 'serial_number', 'name', 'checksum_string'),
			#'FK_instr_type': ('make', 'model'),
			#'Instr_Version': ('FK_version', 'validating_user', 'timestamp')
			#}
		
#class User_VersionSerializer(serializers.ModelSerializer):
	# FK_version = models.ForeignKey(Version, on_delete=models.CASCADE)
	# FK_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	# authorizing_user = models.ForeignKey(UserProfile, related_name='+', on_delete=models.PROTECT)
	# timestamp = models.DateField(auto_now_add=True)

	# class Meta:
		# unique_together = ('FK_version', 'FK_user')

#class UsageHistorySerializer(serializers.ModelSerializer):
	# FK_user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
	# FK_version = models.ForeignKey(Version, on_delete=models.PROTECT)
	# FK_instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
	# timestamp = models.DateTimeField(default=datetime.now, blank=True) 

