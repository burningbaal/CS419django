from django import forms
from django.forms import ModelForm
from .models import *
from django.views.generic import CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Row


class index (forms.Form):
	index_val = forms.CharField(label='Your Limbo name', max_length=10)
	
class MethodForm(ModelForm):
	class Meta:
		model = Method
		fields = ('name', 'description',)
		widgets = {'id': forms.HiddenInput()}
	def __init__(self, *args, **kwargs):
		super(MethodForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Div('name', css_class='col-md-3'),
				Div('description', css_class='col-md-9'),
			),
			ButtonHolder(
				Submit('submit', 'Submit', css_class='button white')
			),
		)
			
class MethodVersionFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(MethodVersionFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Row(
				Div('version_number', css_class='col-md-2'),
				Div('cmd_line_script', css_class='col-md-5'),
				Div('SOP', css_class='col-md-5'),
			),
        )
        self.render_required_fields = True

class usersForm(forms.Form):
	user_name = forms.CharField(label='New User\'s  name', max_length=100)
	user_email = forms.EmailField(label='User\'s email', max_length=100)
	user_active = forms.BooleanField(label='User active')
	
	user_active.initial = True

class GeneralEquipmentForm(ModelForm):
	class Meta:
		model = Instrument
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(Instrument, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		self.fields['FK_instr_type'].label = 'Instrument Type'
		#self.fields['VersionsFromInstrument'].label = 'Valid Versions'
		#if instance and instance.pk:
			#self.fields['config_key'].widget.attrs['readonly'] = True
			#self.fields['config_key'].widget.attrs['disabled'] = True
	#manuf_email = forms.EmailField(label='Manufacturer\'s email', max_length=100)
	
class Instr_VersionCreate(CreateView):
	model = Instr_Version
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		#for version in form.cleaned_data['VersionsFromInstrument']:
		

class SpecificEquipmentForm(ModelForm):
	class Meta:
		model = Instrument
		exclude = ('checksum_string',)
		widgets = {'id': forms.HiddenInput()}
		#include way to validate versions (and useres?)
	def __init__(self, *args, **kwargs):
		super(SpecificEquipmentForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		self.fields['FK_instr_type'].label = 'Instrument Type'
		self.fields['VersionsFromInstrument'].label = 'Valid Versions'

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
			