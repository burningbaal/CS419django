from limbo.models import *
from limbo.forms import *
from django.contrib import admin

#admin.site.register(UserProfile)
#class UserProfileInline(admin.ModelAdmin):
	# model = UserProfile
	# can_delete = True
	# verbose_name_plural = 'profiles'
	# filter_horizontal = ('authorized_MethodVersions',)
	
@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
	form = UserProfileForm
	filter_horizontal = ('authorized_MethodVersions',)