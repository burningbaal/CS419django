from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
from datetime import datetime
from django.http import QueryDict
from django.http import HttpResponse
from django.template import loader
from serializers import *
from limbo.models import *
from django.forms import modelformset_factory
from django.forms import formset_factory
from django.core import serializers as coreSerializers
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth import views as djangoViews
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .forms import *
from rest_framework.renderers import JSONRenderer

#####################################
# TODO:
# restrict editing to just permitted users
#	let others view?
# do something with server configs
# find a way to widen the fields in the forms
# build checksums and move where it is in the getInstrument response
# TEST!!!!
#####################

def logoutLimbo(request):
	logout(request)
	return redirect(
		indexLimbo, 
	)

def indexLimbo(request, message='Welcome, please log in'):
	form = loginForm()
	if request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
		else: 
			message += 'Username or password incorrect, try again'
			return render(
				request, 
				'index.html',
				{
					'form': form,
					'message': message,
				}
			)
	if request.user.is_authenticated:
		form = None
		message += 'Welcome, ' 
		if request.user.get_short_name() == '':
			message += request.user.get_username() + ', to the Limbo server interface!'
		else:
			message += request.user.get_short_name() + ', to the Limbo server interface!'
		return render(
			request, 
			'index.html',
			{
				'form': form,
				'message': message,
			}
		)
	else:
		return render(
				request, 
				'index.html',
				{
					'form': form,
					'message': message,
				}
			)
	
def editUsers(request):
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	return redirect('/admin/auth/user/', request)
	message = 'This is just your own profile<br>\nFirst visit'
	form = UserCreationForm()
	formset = modelformset_factory(UserProfile.user, exclude=('id', 'password',), extra = 0)
	helper = usersFormSetHelper()
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserChangeForm(request.POST)
		# check whether it's valid:
		# process the data in form.cleaned_data as required
		# redirect to a new URL:
		if form.is_valid():
			message = 'form would save now'
			# call out to limboLogic.py to update values, add them to the session
			
			return render(
				request, 
				'limboHtml/UserManagement.html', 
				{
					'form': form, 
					'formSet': formset, 
					'SubmitMessage': message,
					'helper': helper,
				}
			)
		else:
			message = 'The would NOT have been updated.' + '\n'
			message += ', '.join("%s=%r" % (key,val) for (key,val) in form.errors.iteritems()) + '\n' 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in form.non_field_errors.iteritems()) + '\n' 
			return render(
				request, 
				'limboHtml/UserManagement.html', 
				{
					'form': form, 
					'formSet': formset, 
					'SubmitMessage': message,
					'helper': helper,
				}
			)
		
	# if a GET (or any other method) we'll create a blank form
	return render(
		request, 
		'limboHtml/UserManagement.html', 
		{
			'form': form, 
					'formSet': formset, 
			'SubmitMessage': message,
			'helper': helper,
		}
	)

def goToMethod(request):
	message = ''
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	if not request.user.has_perm('change_Version') or not request.user.has_perm('change_Method'):
		return redirect(indexLimbo, message='Sorry, you do not have permission to edit Methods.  \n')
	methodID = int(request.POST.get('methodId', None))
	return redirect(editMethod, methodId=methodID)
	
def editMethod(request, methodId):
	message = ''
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	if not request.user.has_perm('change_Version') or not request.user.has_perm('change_Method'):
		return redirect(indexLimbo, message='Sorry, you do not have permission to edit Methods.  \n')
	method = get_object_or_404(Method, pk=methodId )
	name = request.POST.get('name', None)
	formSet = inlineformset_factory(
		Method,
		Version,
		exclude=('FK_method',), 
		can_delete=True,
		extra=1,
	)
	#message += ' '.join((str(x) + str(y)) for (x, y) in request.POST)
	
	if request.method == 'POST':
		postFormset = formSet(request.POST, request.FILES, instance=method)
		formsetValid = False
		try:
			if postFormset.is_valid():
				message += 'postFormset is valid'
				postFormset.save()
				formSet = postFormset
				formsetValid = True
			else:
				message += 'postFormset is NOT valid ' + '\n'.join(str(x) for x in postFormset.errors) + ' ' + postFormset.non_form_errors()
		except:
			pass
		#time = datetime.now()
		#####################THIS NEXT LINE IS TEMPORARY ONLY!!!!!###############################
		#curUser = UserProfile.objects.get(user='1') # CHANGE LATER, THIS IS JUST FOR TESTING/DEV#
		#####################CHANGE THE LINE ABOVE SOON!!!!######################################
		#for vers in postFormset:
			#curVersion = Version.objects.get(pk=int(vers))
			#message += '\nNext vers'
			
			#validation, created = Instr_Version.objects.get_or_create(FK_instrument=asset, FK_version=curVersion, timestamp=datetime.now(), validating_user=curUser)
			#validation.save()
			#methodID = asset.id
		
	else:
		formSet = formSet(instance=method )
	if not method:
		formSet = modelformset_factory(Method, exclude=('id',), extra=1)
		helper = MethodFormSetHelper()
		helper.add_input(Submit("submit", "Save"))
		
		form = MethodDropDown()
		return render(
			request, 
			'limboHtml/Methods.html', 
			{
				'formSet': formSet, 
				'SubmitMessage': message + '\nERROR:  cannot edit method without ID',
				'helper': helper,
				'form': form
			}
		)
	form = MethodForm(instance=method)
	formSet = inlineformset_factory(
		Method, 
		Version, 
		exclude=('FK_method',), 
		can_delete=True,
		extra=1,
	)
	formSet = formSet(instance=method)
	helper = MethodVersionFormSetHelper()
	helper.add_input(Submit("submit", "Save"))
	return render(
		request, 
		'limboHtml/MethodEdit.html', 
		{
			'form': form, 
			'formSet': formSet, 
			'method': method, 
			'helper': helper,
			'SubmitMessage': message,
		}
	)
	
def editMethods(request):
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	if not request.user.has_perm('change_Method'):
		return redirect(indexLimbo, message='Sorry, you do not have permission to edit Methods.  \n')
	formSet = modelformset_factory(Method, exclude=('id',), extra=1)
	helper = MethodFormSetHelper()
	helper.add_input(Submit("submit", "Save"))
	
	form = MethodDropDown()
	
	if request.method =='POST':
		postFormset = formSet(request.POST, request.FILES)
		if postFormset.is_valid():
			for form in postFormset:
				if form.is_valid(): # and not form.empty_permitted:
					form.save()
			# call out to limboLogic.py to update values, add them to the session
			message = 'The values have been updated.'
			return render(
				request, 
				'limboHtml/Methods.html', 
				{
					'formSet': postFormset, 
					'SubmitMessage': message,
					'helper': helper,
					'form': form
				}
			)
	return render(
		request, 
		'limboHtml/Methods.html', 
		{
			'formSet': formSet, 
			'SubmitMessage': '',
			'helper': helper,
			'form': form
		}
	)
	
def editInstrTypes(request):
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	if not request.user.has_perm('change_Instrument'):
		return redirect(indexLimbo, message='Sorry, you do not have permission to edit equipment.  \n')
	message = ''
	formSet = modelformset_factory(
			InstrType, 
			fields= '__all__', 
			extra=1,
			can_order=True,
			can_delete=True,
		)
	try:
		postFormset = formSet(request.POST, request.FILES)
		if postFormset.is_valid():
			postFormset.save()
			message += 'The values have been updated'
		else:
			message += 'The values could not be updated\n' + postFormset.errors
	except:
		message += 'No values have been updated'
	
	helper = InstrTypeFormSetHelper()
	helper.add_input(Submit("submit", "Update", css_class='btn-default'))
	helper.add_input(Button('cancel', 'Cancel', css_class='btn-default', onclick="window.history.back()"))
	return render(
		request, 
		'limboHtml/EquipmentTypeManagement.html',
		{
			'formSet': formSet, 
			'SubmitMessage': message,
			'helper': helper,
		}
	)

def gotoInstrument(request):
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	if not request.user.has_perm('change_Instrument'):
		return redirect(indexLimbo, message='Sorry, you do not have permission to edit Equipment.  \n')
	message = ''
	instrId = int(request.POST.get('instrument', None))
	return redirect(editInstrument, pk=instrId)
	
def editInstrument(request, pk):
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	if not request.user.has_perm('change_Instrument'):
		return redirect(indexLimbo, message='Sorry, you do not have permission to edit Equipment.  \n')
	curUser = request.user
	assetId = pk
	message = ''
	try:
		update = request.POST.getlist('VersionsFromInstrument')
	except:
		pass
	if request.method == 'POST' and update:
		asset = Instrument.objects.get(pk=assetId)
		time = datetime.now()
		postedVersions = request.POST.getlist('VersionsFromInstrument')
		message += 'Vers are: ' + ' & '.join(str(x) for x in postedVersions) + '\n'
		for vers in Instr_Version.objects.all():
			if str(vers.FK_version.id) in postedVersions:
				message += 'Checking version #' + str(vers.FK_version) + '\n'
				if not Instr_Version.objects.filter(FK_instrument=assetId, FK_version=vers.FK_version).exists():
					message += 'version #' + str(vers.FK_version.id) + ' is going to be added to validVersions\n'
					curUser = UserProfile.objects.get(user=curUser) 
					validation, created = Instr_Version.objects.get_or_create(FK_instrument=asset, FK_version=vers.FK_version, timestamp=datetime.now(), validating_user=curUser)
				else:
					message += ' version #' + str(vers.FK_version.id) + ' already listed\n'
			else:
				# version should be removed if it currently exists
				if Instr_Version.objects.filter(FK_instrument=asset, FK_version=vers.FK_version).exists():
					toRemove = Instr_Version.objects.filter(FK_instrument=assetId, FK_version=vers.FK_version)
					message += 'going to remove: ' + ', '.join(str(x) for x in toRemove) + '\n'
					for entry in toRemove:
						entry.delete()
				else:
					message += 'version #' + str(vers.FK_version.id) + ' already not listed\n'
		#for vers in postedVersions:
		#	curVersion = Version.objects.get(pk=int(vers))
		#	if not Instr_Version.objects.filter(FK_instrument=asset, FK_version=curVersion).exists():
				
				#####################THIS NEXT LINE IS TEMPORARY ONLY!!!!!###############################
		#		curUser = UserProfile.objects.get(user='1') # CHANGE LATER, THIS IS JUST FOR TESTING/DEV#
				#####################CHANGE THE LINE ABOVE SOON!!!!######################################
				
		#		validation, created = Instr_Version.objects.get_or_create(FK_instrument=asset, FK_version=curVersion, timestamp=datetime.now(), validating_user=curUser)
				#validation.save()
		#	else:
		#		pass
	if assetId is None:
		formSet = modelformset_factory(
			Instrument, 
			exclude=('VersionsFromInstrument', 'checksum_string',), 
			extra=1
		)
		return render(
			request, 
			'limboHtml/EquipmentManagement.html', 
			{
				'formSet': formSet, 
				'SubmitMessage': 'ERROR: Cannot edit an instrument without a "asset_number" parameter.'
			}
		)
	instr = get_object_or_404(Instrument, pk=assetId ) 
	form = SpecificEquipmentForm(instance=instr)
	#serial = InstrumentSerializer(instr)
	#strInstrument = JSONRenderer().render(serial.data)
	return render(
		request, 
		'limboHtml/InstrumentManagement.html',
		{
			'form': form, 
			'instrument': instr,
			'SubmitMessage': message,
		}
	) 
	
def editEquipment(request):
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	if not request.user.has_perm('change_Instrument'):
		return redirect(indexLimbo, message='Sorry, you do not have permission to edit Equipment.  \n')
	formSet = modelformset_factory(Instrument, exclude=('VersionsFromInstrument', 'checksum_string',), extra=1)
	helper = EquipmentFormSetHelper()
	helper.add_input(Submit("submit", "Save"))
	form = EquipmentDropDown()
	if request.method == 'POST':
		postFormset = formSet(request.POST, request.FILES)
		if postFormset.is_valid():
			postFormset.save()
			# call out to limboLogic.py to update values, add them to the session
			message = 'The values have been updated.'
			return render(
				request, 
				'limboHtml/EquipmentManagement.html', 
				{
					'formSet': postFormset, 
					'SubmitMessage': message,
					'helper': helper,
					'form': form,
				}
			)
		else:
			message = 'The equipment has NOT been updated.' + '\n'
			for dict in postFormset.errors:
				message = coreSerializers.serialize('json', [dict,])
				#message += ', '.join("%s=%r" % (key,val) for (key,val) in dict) + '\n'
			#message += ', '.join("%s=%r" % (key,val) for (key,val) in postFormset.errors.dict.values) + '\n' 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in postFormset.non_form_errors) + '\n' 
			#message += str(postFormset.non_form_errors)
			return render(
				request, 
				'limboHtml/EquipmentManagement.html', 
				{
					'formSet': postFormset, 
					'SubmitMessage': message,
					'helper': helper,
					'form': form
				}
			)
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['editEquipId']
	except KeyError:
		pass
	#form = GeneralEquipmentForm()
	return render(
		request, 
		'limboHtml/EquipmentManagement.html', 
		{
			'formSet': formSet, 
			'SubmitMessage': '',
			'helper': helper,
			'form': form
		}
	)

def editServer(request):
	if not request.user.is_authenticated:
		return redirect(logoutLimbo)
	if not request.user.has_perm('change_serverConfig'):
		return redirect(indexLimbo, message='Sorry, you do not have permission to edit Server Configurations.  \n')
	result = serverConfig.objects.values()
	myConfigs = [entry for entry in result]
	
	finalFormSet = modelformset_factory(serverConfig, exclude=('id',), extra=0)
	
	if request.method == 'POST':
		formset = finalFormSet(request.POST, request.FILES)
		if formset.is_valid():
			for form in formset:
				form.save()
			
			# call out to limboLogic.py to update values, add them to the session
			message = 'The values have been updated.'
			return render(request, 'limboHtml/ServerConfiguration.html', {'formset': finalFormSet, 'SubmitMessage': '', 'CurrentConfigs': myConfigs})
		else:
			message = 'The server configuration has NOT been updated.' + '\n'
			message += ', '.join("%s=%r" % (key,val) for (key,val) in formset.errors.iteritems()) + '\n' 
			message += '<br> ' + ", ".join("%s=%r" % (key,val) for(key,val) in formset.iteritems()) 
			# message += ', '.join("%s=%r" % (key,val) for (key,val) in formset.non_field_errors.iteritems()) + '\n' 
			return render(request, 'limboHtml/ServerConfiguration.html', {'form': finalFormSet, 'SubmitMessage': message, 'CurrentConfigs': myConfigs})
	# if a GET (or any other method) we'll create a blank form
	try:
		del request.session['integer']
	except KeyError:
		pass
	
	return render(request, 'limboHtml/ServerConfiguration.html', {'formset': finalFormSet, 'SubmitMessage': '', 'CurrentConfigs': myConfigs})

