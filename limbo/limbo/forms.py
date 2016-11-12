from django import forms
from django.forms import ModelForm
from .models import *

class index (forms.Form):
	index_val = forms.CharField(label='Your Limbo name', max_length=10)

class usersForm(forms.Form):
	user_name = forms.CharField(label='New User\'s  name', max_length=100)
	user_email = forms.EmailField(label='User\'s email', max_length=100)
	user_active = forms.BooleanField(label='User active')
	
	user_active.initial = True

class GeneralEquipmentForm(forms.Form):
	class Meta:
		model = Instrument
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(Instrument, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		#if instance and instance.pk:
			#self.fields['config_key'].widget.attrs['readonly'] = True
			#self.fields['config_key'].widget.attrs['disabled'] = True
	#manuf_email = forms.EmailField(label='Manufacturer\'s email', max_length=100)

class SpecificEquipmentForm(forms.Form):
	class Meta:
		model = Instrument
		fields = '__all__'
		#include way to validate versions (and useres?)
	def __init__(self, *args, **kwargs):
		super(Instrument, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)	

class serverForm(ModelForm):
	class Meta:
		model = serverConfig
		fields = ['config_value']
		readonly_fields = ['config_key']
	def __init__(self, *args, **kwargs):
		super(serverForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			self.fields['config_key'].widget.attrs['readonly'] = True
			self.fields['config_key'].widget.attrs['disabled'] = True
			