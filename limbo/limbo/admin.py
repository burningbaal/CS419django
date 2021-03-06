from limbo.models import *
from limbo.forms import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserProfileVersionInline(admin.StackedInline):
	model = UserProfile_Version
	#fields = ('FK_version',)
	exclude = ('authorizing_user', )
	fk_name = 'userProfile'
	verbose_name_plural = 'Trained versions'
	# def save_model(self, request, obj, form, change):
		# obj.authorizing_user = request.user.profile
		# obj.save()

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
	inlines = [UserProfileVersionInline,]
	list_display  = ('Last_name', 'First_name', 'title', 'user_link',)
	search_fields = ('user__last_name', 'user__first_name', 'title',)
	readonly_fields = ('user',)
		
	def Last_name(self, obj):
		return obj.user.last_name
	def First_name(self, obj):
		return obj.user.first_name
	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for instance in instances:
			instance.authorizing_user = request.user.profile
			instance.save()


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
	search_fields = ('instrument__name','instrument__asset_number','version__version_number',)
	list_filter = ('user','instrument__name','instrument__asset_number', 'version')
	
	def Time(self, obj):
		return obj.timestamp
	def User(self, obj):
		return obj.user
	def Instrument(self, obj):
		return obj.instrument
	def Method(self, obj):
		return obj.version

class InstrumentInline(admin.TabularInline):
	model = Instrument

@admin.register(InstrType)
class InstrTypeAdmin(admin.ModelAdmin):
	inlines = [InstrumentInline,]
	list_display  = ('make', 'model', 'service_email', 'service_website',)
	search_fields = ('make', 'model', 'service_email', 'service_website',)
	list_filter = ('make', 'model',)
	

class Instr_VersionInline(admin.TabularInline):
	model = Instr_Version
	exclude = ('validating_user',)
	#filter_horizontal = ('FK_version',)
	# def save_model(self, request, obj, form, change):
		# obj.validating_user = request.user.profile
		# obj.save()
	
@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
	inlines = [Instr_VersionInline,]
	list_display  = ('name', 'asset_number', 'Instrument_type', 'serial_number', )
	search_fields = ('name', 'asset_number', 'FK_instr_type__make', 'FK_instr_type__model', 'serial_number', )
	readonly_fields = ('checksum_string',)
	list_filter = ('name', 'asset_number','FK_instr_type__make', 'FK_instr_type__model',)
	
	def Instrument_type(self, obj):
		return obj.FK_instr_type
	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for instance in instances:
			instance.validating_user = request.user.profile
			instance.save()

class VersionInline(admin.TabularInline):
	model = Version
	formfield_overrides = {
		models.TextField: {
							'widget': Textarea(
							attrs={'rows': 10,
							'cols': 40,
							'style': 'height: 10em;'})
							},
	}
	
@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
	inlines = [VersionInline,]
	list_display  = ('name', 'description',)
	search_fields = ('name', 'description',)
	
	
class ReadOnlyModelAdmin(admin.ModelAdmin):
    actions = None
    list_display_links = None
    # more stuff here

    def has_add_permission(self, request):
        return False
	def has_delete_permission(self, request):
		return False
	
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)