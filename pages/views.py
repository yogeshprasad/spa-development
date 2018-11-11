from django.shortcuts import render, redirect, reverse
from pages.models import CoachingContact

def edit_page(request, *args, **kwargs):
    pageid = kwargs.get('pageid')

    if pageid in ['contact']:
        return render(request, 'pages/'+pageid+'.html')
    else:
        return render(request, 'pages/error-404.html')
	