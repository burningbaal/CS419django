from limbo.models import *
from django.contrib import admin

admin.site.register(UserProfile)
#@admin.register(UserProfile)
# class UserProfileInline(admin.ModelAdmin):
	# model = UserProfile
	# can_delete = True
	# verbose_name_plural = 'profiles'
	# filter_horizontal = ('authorized_MethodVersions',)
	
# class UserProfile(admin.ModelAdmin):
	# inlines = [UserProfileInline,]