from django import forms

class formTest (forms.Form):
	testName = forms.CharField(label='Your Limbo name', max_length=10)
class NameForm(forms.Form):
	your_name = forms.CharField(label='Your Awesome  name', max_length=100)
