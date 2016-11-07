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
		fields = ('id', 'name', 'description', 'version_set')

class VersionSerializer(serializers.ModelSerializer):
	method = MethodSerializer(read_only=True)
	#Instr_Version = Instr_VersionSerializer(source='Instr_Version_set', many=True, read_only=True)
	class Meta:
		model = Version
		fields = ('id', 'method', 'version_number', 'cmd_line_script', 'SOP')

class Instr_to_VersionSerializer(serializers.ModelSerializer):
	version = VersionSerializer(source='FK_version_id', read_only=True, many=False)
	validator = UserProfileSerializer(source='UserProfileSerializer', read_only=True)
	
	class Meta:
		model = Instr_Version
		fields = ('id', 'version', 'version_number', 'validator', 'timestamp')


class InstrumentSerializer(serializers.ModelSerializer):
	instr_type = InstrTypeSerializer(source='FK_instr_type', read_only=True)
	Instr_Version = Instr_to_VersionSerializer(many=True, read_only=True)
	
	class Meta:
		model = Instrument
		fields = ('id', 'asset_number', 'serial_number', 'name', 'checksum_string', 'instr_type', 'Instr_Version')
		
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

