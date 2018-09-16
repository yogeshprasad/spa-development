from django.shortcuts import render, redirect, reverse

# Create your views here.
# Create your views here.
def home(request):
	numbers = [1,2,3,4,5,6]
	name = "ram"
	args = {'name': name, 'numbers': numbers}
	return render(request, 'edu/home.html', args)

def getProfileId(url):
	return url.split("/")[2]

def profile_home(request, *args, **kwargs):
	print(request.GET.get("ask"))
	print(args)
	print(kwargs)

	ask = request.GET.get("ask")
	if not ask:
		ask = 'index'
	
	return render(request, 'edu/'+ask+'.html', {'page':ask})

def about(request, *args, **kwargs):
	return redirect('/edu/'+getProfileId(request.path) + '?ask=about')

def about(request, *args, **kwargs):
	return redirect('/edu/'+getProfileId(request.path) + '?ask=about')
	