from django import forms
from django.forms import ModelForm
from .models import *
from django.views.generic import CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Row, Button


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
			Div(
				Div('name', css_class='col-md-3'),
				Div('description', css_class='col-md-9'),
				css_class='row well well-lg',
			),
			ButtonHolder(
				Submit('submit', 'Submit', css_class='button white')
			),
		)

class MethodDropDown(forms.Form):
	method = forms.ChoiceField(
		choices=[(o.id, str(o)) for o in Method.objects.all()], 
		label='Edit details of: '
	)
	
class EquipmentDropDown(forms.Form):
	instrument = forms.ChoiceField(
		choices=[(o.id, str(o)) for o in Instrument.objects.all()], 
		label='Edit details of: '
	)
	
class MethodFormSetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(MethodFormSetHelper, self).__init__(*args, **kwargs)
		self.form_method = 'post'
		self.layout = Layout(
			Div(
				Div('name', css_class='col-md-3'),
				Div('description', css_class='col-md-9'),
				css_class='row well well-lg',
			),
		)
		self.render_required_fields = True
				
class InstrTypeFormSetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(InstrTypeFormSetHelper, self).__init__(*args, **kwargs)
		self.form_method = 'post'
		self.layout = Layout(
			Div(
				Div('make', css_class='col-md-3'),
				Div('model', css_class='col-md-3'),
				Div('service_email', css_class='col-md-3'),
				Div('service_website', css_class='col-md-3'),
				css_class='row well well-lg',
			),
		)
		self.render_required_fields = True
		
			
class MethodVersionFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(MethodVersionFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Div(
				Row( Div('version_number', css_class='col-md-12') ),
				Row( 
					Div('cmd_line_script', css_class='col-md-6'),
					Div('SOP', css_class='col-md-6')
				),
				css_class='row well well-lg',
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
		
class EquipmentFormSetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(EquipmentFormSetHelper, self).__init__(*args, **kwargs)
		self.form_method = 'post'
		self.layout = Layout(
			Div(
				Div('serial_number', css_class='col-md-3'),
				Div('asset_number', css_class='col-md-3'),
				Div('name', css_class='col-md-3'),
				Div('FK_instr_type', css_class='col-md-3'),
				css_class='row well well-lg',
			),
		)
		self.render_required_fields = True
			
	
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
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Div(
				Div('serial_number', css_class='col-md-2'),
				Div('asset_number', css_class='col-md-2'),
				Div('name', css_class='col-md-2'),
				Div('FK_instr_type', css_class='col-md-3'),
				Div('VersionsFromInstrument', css_class='col-md-3'),
				css_class='row well well-lg',
			),
			ButtonHolder(
				Submit('submit', 'Submit', css_class='button white')
			),
		)

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
			