from django import forms
from django.forms import ModelForm
from limbo.models import *

class usageHistoryForm(ModelForm):
	class Meta:
		model = UsageHistory
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(usageHistoryForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)

class getUsageForm(forms.Form):
	number_histories = forms.IntegerField(required=False)
	