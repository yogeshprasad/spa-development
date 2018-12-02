from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from edu.models import CoachingProfile
from accounts.account_forms.contactus import CoachingContactForm
from pages.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login/')
def teachers_info(request):
    profile = CoachingProfile.objects.get(username=request.user)
    data = Teachers.objects.filter(username=request.user).values()

    return render(request, 'accounts/edit_teachers.html',{'data':data, 'page_name':"Teachers", 'coaching_name': profile.name})

@login_required(login_url='/account/login/')
def new_teacher(request):
    try:
        profile = CoachingProfile.objects.get(username=request.user)
    except ObjectDoesNotExist as e:
        print(str(request.user) + " Error: Coaching registration not complated yet")
        return redirect(reverse('accounts:home'))

    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        description = request.POST.get('description')
        if id:
            Teachers.objects.filter(username=request.user).filter(id=id).update(name=name, contact=contact, email=email, description=description)
        else:
            Teachers(username=request.user, name=name, contact=contact, email=email, description=description).save()

    return HttpResponseRedirect(reverse("accounts:teachers"))

@login_required(login_url='/account/login/')
def remove_teacher(request):
    try:
        profile = CoachingProfile.objects.get(username=request.user)
    except ObjectDoesNotExist as e:
        print(str(request.user) + " Error: Coaching registration not complated yet")
        return redirect(reverse('accounts:home'))

    if request.method == "POST":
        id = request.POST.get('id')
        Teachers.objects.filter(username=request.user).filter(id=id).delete()

    return HttpResponseRedirect(reverse("accounts:teachers"))

@login_required(login_url='/account/login/')
def get_teacher(request):
    try:
        profile = CoachingProfile.objects.get(username=request.user)
    except ObjectDoesNotExist as e:
        print(str(request.user) + " Error: Coaching registration not complated yet")
        return redirect(reverse('accounts:home'))

    if request.method == "GET":
        id = request.GET.get('id')
        teacher =  Teachers.objects.filter(username=request.user).filter(id=id).values()[0]

        data = Teachers.objects.filter(username=request.user).values()
        return render(request, 'accounts/edit_teachers.html',{'data':data, 'teacher':teacher, 'page_name':"Teachers", 'coaching_name': profile.name})
