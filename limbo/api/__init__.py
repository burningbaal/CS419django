from django.contrib.auth import authenticate, login

def getUser(username, password)
	user = None
	user = authenticate(username=username, password=password)
	return user