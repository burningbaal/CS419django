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

class ProfileInline(admin.StackedInline):
	model = UserProfile
	filter_horizontal =('trained',)
	can_delete = False
	verbose_name_plural ='Profile'
	fk_name = 'user'

class CustomUserAdmin(UserAdmin):
	
	inlines = (ProfileInline, )
	
	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.register(UsageHistory)
admin.site.register(Instrument)


class VersionInline(admin.StackedInline):
	model = Version
	
@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
	inlines = [VersionInline,]

	
# @admin.register(UserProfile)
#class UserProfile(admin.ModelAdmin):
#	form = UserProfileForm
#	filter_horizontal = ('trained',)
	
	
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)