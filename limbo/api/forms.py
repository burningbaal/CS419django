from django import forms
from django.forms import ModelForm
from .models import *

class usageHistoryForm(ModelForm):
	class Meta:
		model = usageHistory
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(usageHistory, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)