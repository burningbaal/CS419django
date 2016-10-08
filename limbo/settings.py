STATIC_ROOT = os.path.join("/var/www/html")

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
