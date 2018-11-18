from django.shortcuts import render, redirect

# Create your views here.
def login_redirect(request):
	return redirect('/account/login')

# Create your views here.
def home(request):
	if request.user.is_authenticated:
		return redirect('/account/coachingprofile')
	else:
		return render(request, 'accounts/home.html')
