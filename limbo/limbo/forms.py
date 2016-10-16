from django import forms

class index (forms.Form):
	index_val = forms.CharField(label='Your Limbo name', max_length=10)

class usersForm(forms.Form):
	user_name = forms.CharField(label='New User\'s  name', max_length=100)

class equipmentForm(forms.Form):
	manuf_email = forms.EmailField(label='Manufacturer\'s email', max_length=100)
	
class serverForm(forms.Form):
	bool_field = forms.BooleanField(label='Is it true?')
