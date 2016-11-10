from rest_framework import serializers
from django.conf import settings
from django.contrib import auth
from limbo.models import *

class serverConfigSerializer(serializers.ModelSerializer):
	class Meta:
		model = serverConfig
		fields = '__all__'
	
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = auth.get_user_model()
		#fields = '__all__'
		exclude = ('password',)
		
class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	#user = serializers.serialize(settings.AUTH_USER_MODEL, read_only=True)
	class Meta:
		model = UserProfile
		#fields = ('last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')
		fields = '__all__'
		#excludes = ('password',)
	
class InstrTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = InstrType
		fields = '__all__'

class MethodSerializer(serializers.ModelSerializer):
	description = serializers.ReadOnlyField(source='descripton')
	class Meta:
		model = Method
		fields = ('id', 'name', 'description')

class VersionSerializer(serializers.ModelSerializer):
	method = MethodSerializer(read_only=True)
	#Instr_Version = Instr_VersionSerializer(source='Instr_Version_set', many=True, read_only=True)
	class Meta:
		model = Version
		fields = ('id', 'method')#, 'version_number', 'cmd_line_script', 'SOP')

class Instr_to_VersionSerializer(serializers.ModelSerializer):
	#version = VersionSerializer(source='self.FK_version', read_only=True, many=False)
	#validator = UserProfileSerializer(source='self.validating_user', read_only=True)
	#validator = serializers.ReadOnlyField(source='self.validating_user.user.email')
	version_name = serializers.ReadOnlyField(source='version_number')
	cmd_line_script = serializers.ReadOnlyField()
	SOP = serializers.ReadOnlyField()
	method = MethodSerializer(source='FK_method',read_only=True) 
	Time_Validated = serializers.ReadOnlyField(source= 'timestamp')
	
	class Meta:
		model = Instr_Version
		fields = '__all__'
		#fields = ('id', 'timestamp', 'validator', 'version', 'method', 'version_name', 'cmd_line_script', 'SOP')


class InstrumentSerializer(serializers.ModelSerializer):
	instr_type = InstrTypeSerializer(source='FK_instr_type', read_only=True)
	Validated_Versions = Instr_to_VersionSerializer(source='VersionsFromInstrument', many=True, read_only=True)
	
	class Meta:
		model = Instrument
		fields = ('id', 'asset_number', 'serial_number', 'name', 'checksum_string', 'instr_type', 'Validated_Versions')
		
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

