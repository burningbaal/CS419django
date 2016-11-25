from limbo.models import *
from django.contrib import admin

@admin.register(Author)
class UserProfileInline(ModelAdmin.StackedInline):
	model = UserProfile
	can_delete = True
	verbose_name_plural = 'profiles'
	filter_horizontal = ('authorized_MethodVersions',)