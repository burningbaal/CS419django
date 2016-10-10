STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = [
#	"/home/ec2-user/limbo/limbo/static/",
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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)