from django import forms
from django.forms import ModelForm
from limbo.models import *

class index (forms.Form):
	index_val = forms.CharField(label='Your Limbo name', max_length=10)

class usersForm(forms.Form):
	user_name = forms.CharField(label='New User\'s  name', max_length=100)
	user_email = forms.EmailField(label='User\'s email', max_length=100)
	user_active = forms.BooleanField(label='User active')
	
	user_active.initial = True

class equipmentForm(forms.Form):
	manuf_email = forms.EmailField(label='Manufacturer\'s email', max_length=100)

class serverForm(ModelForm)
	class Meta:
		model = serverConfig
		fields = ['ClientMustVerify', 'Auditing']
	
# class serverForm(forms.Form):
#	int_field = forms.IntegerField(label='How many?')
