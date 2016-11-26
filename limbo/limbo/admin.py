from limbo.models import *
from limbo.forms import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

#admin.site.register(UserProfile)
#class UserProfileInline(admin.ModelAdmin):
	# model = UserProfile
	# can_delete = True
	# verbose_name_plural = 'profiles'
	# filter_horizontal = ('authorized_MethodVersions',)
	
"""
Resource: https://simpleisbetterthancomplex.com/tutorial/2016/11/23/how-to-add-user-profile-to-django-admin.html
"""
#@admin.register(UserProfile_Version)
class UserProfileVersionInline(admin.StackedInline):
	model = UserProfile_Version
	#fields = ('FK_version',)
	exclude = ('authorizing_user', )
	fk_name = 'userProfile'
	verbose_name_plural = 'Trained versions'
	def save_model(self, request, obj, form, change):
		obj.authorizing_user = request.user.profile
		obj.save()

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
	inlines = [UserProfileVersionInline,]
	list_display  = ('Last_name', 'First_name', 'title', 'user_link')
	search_fields = ('user__last_name', 'user__first_name', 'title',)
		
	def Last_name(self, obj):
		return obj.user.last_name
	def First_name(self, obj):
		return obj.user.first_name
	
#class ProfileInline(admin.TabularInline):
	

class CustomUserAdmin(UserAdmin):
	
	#inlines = [ProfileInline, UserProfileVersionInline,]
	
	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

@admin.register(UsageHistory)
class UsageHistoryAdmin(admin.ModelAdmin):
	verbose_name_plural = 'Usage History Logs'
	list_display = ('User', 'Instrument','Method', 'Time',)
	search_fields = ('FK_instrument__name','FK_instrument__asset_number','FK_version__version_number',)
	
	def Time(self, obj):
		return obj.timestamp
	def User(self, obj):
		return obj.FK_user
	def Instrument(self, obj):
		return obj.FK_instrument
	def Method(self, obj):
		return obj.FK_version

class InstrumentInline(admin.TabularInline):
	model = Instrument

@admin.register(InstrType)
class InstrTypeAdmin(admin.ModelAdmin):
	inlines = [InstrumentInline,]
	list_display  = ('make', 'model', 'service_email', 'service_website',)
	search_fields = ('make', 'model', 'service_email', 'service_website',)
	

class Instr_VersionInline(admin.TabularInline):
	model = Instr_Version
	exclude = ('validating_user',)
	#filter_horizontal = ('FK_version',)
	def save_model(self, request, obj, form, change):
		obj.validating_user = request.user.profile
		obj.save()
	
@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
	inlines = [Instr_VersionInline,]
	list_display  = ('name', 'asset_number', 'Instrument_type', 'serial_number', )
	search_fields = ('name', 'asset_number', 'FK_instr_type__make', 'FK_instr_type__model', 'serial_number', )
	
	def Instrument_type(self, obj):
		return obj.FK_instr_type

class VersionInline(admin.TabularInline):
	model = Version
	
@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
	inlines = [VersionInline,]
	list_display  = ('name', 'description',)
	search_fields = ('name', 'description',)
	

	
# @admin.register(UserProfile)
#class UserProfile(admin.ModelAdmin):
#	form = UserProfileForm
#	filter_horizontal = ('trained',)
	
	
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)