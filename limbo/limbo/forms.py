from django import forms

class index (forms.Form):
	index_val = forms.CharField(label='Your Limbo name', max_length=10)
