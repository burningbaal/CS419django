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
	fk_name = 'FK_userProfile'
	verbose_name_plural = 'Trained versions'
	def save_model(self, request, obj, form, change):
		obj.authorizing_user = request.user.profile
		obj.save()

class UserInline(admin.TabularInline):
	model = User
	fields = '__all__'
	can_delete = False
	

@admin.register(UserProfile)
class ProfileInline(admin.ModelAdmin):
	inlines = [UserProfileVersionInline, UserInline]
	list_display = ('get_last_name', 'get_first_name', 'title', 'get_username', 'get_email', )
	
	def get_email(self, obj):
		return obj.user.email
	def get_last_name(self, obj):
		return obj.user.last_name
	def get_first_name(self, obj):
		return obj.user.first_name
	def get_username(self, obj):
		return obj.user.username
	#filter_horizontal =('trained',)
	

class CustomUserAdmin(UserAdmin):
	
	#inlines = [ProfileInline, UserProfileVersionInline,]
	
	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

@admin.register(UsageHistory)
class UsageHistoryAdmin(admin.ModelAdmin):
	verbose_name_plural = 'Usage History Logs'

class InstrumentInline(admin.TabularInline):
	model = Instrument

@admin.register(InstrType)
class InstrTypeAdmin(admin.ModelAdmin):
	inlines = [InstrumentInline,]
	list_display = ('make', 'model', 'service_email', 'service_website',)
	

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
	list_display = ( 'name', 'asset_number', 'FK_instr_type', 'serial_number', )

class VersionInline(admin.TabularInline):
	model = Version
	
@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
	inlines = [VersionInline,]
	list_display = ('name', 'description',)

	
# @admin.register(UserProfile)
#class UserProfile(admin.ModelAdmin):
#	form = UserProfileForm
#	filter_horizontal = ('trained',)
	
	
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)