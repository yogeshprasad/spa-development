from django.shortcuts import render, redirect

# Create your views here.
def login_redirect(request):
	return redirect('/account/login')

# Create your views here.
def home(request):
	numbers = [1,2,3,4,5,6]
	name = "ram"
	args = {'name': name, 'numbers': numbers}
	if request.user.is_authenticated:
		return redirect('/account/coachingprofile')
	else:
		return render(request, 'accounts/dashboard.html', args)

def profile(request, *args, **kwargs):
	return render(request, 'accounts/dashboard.html', {})