STATIC_ROOT = os.path.join("/var/www/html/")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
	"/home/ec2-user/limbo/limbo/static/",
]

STATICFILES_FINDERS = [	
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			'/var/www/html'],
			'/var/www/html/polls/']
		'APP_DIRS': True,
		'OPTIONS': {
			# ...
		},
	},
]
