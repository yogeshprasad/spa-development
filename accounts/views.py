import datetime

from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from edu.models import CoachingProfile
from accounts.account_forms.coaching_registeration import CoachingRegisterationForm
from accounts.account_forms.contactus import CoachingContactForm
from pages.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required

def redirect_to_login():
	return redirect(reverse('accounts:login'))

# Create your views here.
def home(request):
	if request.user.is_authenticated:
		# Get All data name
		user_exits = CoachingProfile.objects.filter(username=request.user)
		if not user_exits:
			form = CoachingRegisterationForm()
			return render(request, 'accounts/register_coaching.html', {'form': form, 'coaching_profile':1})
		return redirect(reverse('accounts:coachingprofile'))
	else:
		return render(request, 'accounts/home.html')

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('accounts:login'))
		else:
			args = {'form': form}
			return render(request, 'accounts/reg_form.html', args)
	else:
		form = RegistrationForm()

		args = {'form': form}
		return render(request, 'accounts/reg_form.html', args)

@login_required(login_url='/account/login/')
def profile(request):
	profile = CoachingProfile.objects.get(username=request.user)

	if request.method == 'POST':
		up = UserProfile.objects.get(user=request.user)
		up.description = request.POST.get('description')
		up.city = request.POST.get('city')
		up.phone = request.POST.get('contact')
		if request.FILES:
			up.image = request.FILES['profilepic']
		up.save()

	return render(request, 'accounts/user.html',{'coaching_name': profile.name})

@login_required(login_url='/account/login/')
def change_password(request):
	profile = CoachingProfile.objects.get(username=request.user)
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			args = {'form': PasswordChangeForm(user=request.user), 'coaching_name': profile.name, 'result':{'status':'success', 'message': "Password updated successfully."}}
			return render(request, 'accounts/change_password.html', args)
		else:
			args = {'form': form}
			return render(request, 'accounts/change_password.html', args)
	else:
		form = PasswordChangeForm(user=request.user)
		args = {'form': form, 'coaching_name': profile.name}
		return render(request, 'accounts/change_password.html', args)

@login_required(login_url='/account/login/')
def registerNewCoaching(request):

	form = CoachingRegisterationForm(request.POST)
	if form.is_valid():
		c_profile = CoachingProfile.objects.filter(username=request.user).values()
		if c_profile:
			if c_profile[0].get('url') != form.cleaned_data['unique_url']:
				result = CoachingProfile.objects.filter(url=form.cleaned_data['unique_url']).values()
				if result:
					return render(request, 'accounts/coaching_profile.html', {'form': form, 'result':{'status':'warn', 'message': "Entered url is not available, Please enter new url."}})

			CoachingProfile.objects.filter(username=request.user).update(name=form.cleaned_data['coaching_name'], url=form.cleaned_data['unique_url'])
		else:
			result = CoachingProfile.objects.filter(url=form.cleaned_data['unique_url']).values()
			if result:
				return render(request, 'accounts/register_coaching.html', {'form': form, 'result':{'status':'warn', 'message': "Entered url is not available, Please enter new url."}})

			newc = CoachingProfile(username=request.user, name=form.cleaned_data['coaching_name'], url=form.cleaned_data['unique_url'])
			newc.save()
		return getCoachingProfile(request)
	else:
		return render(request, 'accounts/register_coaching.html', {'form': form})

@login_required(login_url='/account/login/')
def getCoachingProfile(request):
	try:
		profile = CoachingProfile.objects.get(username=request.user)
	except ObjectDoesNotExist as e:
		print(str(request.user) + " Error: Coaching registration not complated yet")
		return redirect(reverse('accounts:home'))

	form = CoachingRegisterationForm(initial={'coaching_name':profile.name,'unique_url':profile.url})
	return render(request, 'accounts/coaching_profile.html', {'form': form, 'coaching_name': profile.name, 'page_name':"Coaching Profile"})
	
@login_required(login_url='/account/login/')
def edit_contactus(request):
	contactUsInfo = CoachingContact.objects.filter(username=request.user).values()
	try:
		profile = CoachingProfile.objects.get(username=request.user)
	except ObjectDoesNotExist as e:
		print(str(request.user) + " Error: Coaching registration not complated yet")
		return redirect(reverse('accounts:home'))

	if request.method == "GET":
		form = CoachingContactForm()
		if contactUsInfo and contactUsInfo[0]:
			contactUsInfo = contactUsInfo[0]
			form.fields['email'].initial = contactUsInfo.get('email')
			form.fields['address'].initial = contactUsInfo.get('address')
			form.fields['mobile'].initial = contactUsInfo.get('phone')
			form.fields['message'].initial = contactUsInfo.get('message')
			form.fields['header'].initial = contactUsInfo.get('header')
			form.fields['city'].initial = contactUsInfo.get('city')
		return render(request, 'accounts/edit_contactus.html', {'form': form, 'page_name':"Edit Contact Us", 'coaching_name': profile.name})
	elif request.method == "POST":
		form = CoachingContactForm(request.POST)
		if form.is_valid():
			if contactUsInfo and contactUsInfo[0]:
				contactUsInfo = contactUsInfo[0]
				CoachingContact.objects.filter(username=request.user).update(
					email=form.cleaned_data['email'],
					phone=form.cleaned_data['mobile'],
					message=form.cleaned_data['message'],
					header=form.cleaned_data['header'],
					address=form.cleaned_data['address'],
					city=form.cleaned_data['city']
				)
			else:
				contactusinfo = CoachingContact(username=request.user,
					email=form.cleaned_data['email'],
					phone=form.cleaned_data['mobile'],
					message=form.cleaned_data['message'],
					header=form.cleaned_data['header'],
					address=form.cleaned_data['address'],
					city=form.cleaned_data['city'])

				contactusinfo.save()

			return render(request, 'accounts/success_page.html', {'coaching_name': profile.name})
		else:
			return render(request, 'accounts/edit_contactus.html', {'form': form, 'page_name':"Edit Contact Us", 'coaching_name': profile.name})

@login_required(login_url='/account/login/')
def edit_courses(request):
	try:
		profile = CoachingProfile.objects.get(username=request.user)
	except ObjectDoesNotExist as e:
		print(str(request.user) + " Error: Coaching registration not complated yet")
		return redirect(reverse('accounts:home'))

	datatoedit = []
	gettitle = None
	if request.method == "POST":
		title = request.POST.get("title")
		action = request.POST.get("action")
		if action == "delete":
			CoachingCourse.objects.filter(username=request.user).filter(title=title).delete()
		return HttpResponseRedirect(reverse("accounts:ecourses"))

	if request.method == "GET":
		gettitle = request.GET.get("title")
		action = request.GET.get("action")
		editdata = list(CoachingCourse.objects.filter(username=request.user).filter(title=gettitle).values())
		for data in editdata:
			datatoedit.append(data.get('chapter'))

	course_titles = CoachingCourse.objects.filter(username=request.user).values('title').distinct()
	response = []
	for titleDict in course_titles:
		response.append(titleDict.get('title'))

	return render(request, 'accounts/edit_courses.html',{'data':response, 'chapters': datatoedit, 'title': gettitle, 'page_name':"Edit Courses", 'coaching_name': profile.name})

@login_required(login_url='/account/login/')
def save_new_course(request):
	try:
		profile = CoachingProfile.objects.get(username=request.user)
	except ObjectDoesNotExist as e:
		print(str(request.user) + " Error: Coaching registration not complated yet")
		return redirect(reverse('accounts:home'))

	if request.method == "POST":
		course_title = request.POST.get('course_title')
		chapters = request.POST.getlist('chapter')

		# Check if same course exists, if exists delete it and save from new
		CoachingCourse.objects.filter(username=request.user).filter(title=course_title).delete()

		#Get supported courses by this user
		course_count = len(CoachingCourse.objects.filter(username=request.user).values('courseid').distinct()) + 1

		count = 1
		for chapter in chapters:
			courseinfo = CoachingCourse(username=request.user, title=course_title, chapterid="chapter-" + str(count), chapter=chapter, courseid=course_count)
			courseinfo.save()
			count = count + 1

		return HttpResponseRedirect(reverse("accounts:savenewcourse"))

	course_titles = CoachingCourse.objects.filter(username=request.user).values('title').distinct()
	response = []
	for titleDict in course_titles:
		response.append(titleDict.get('title'))

	return render(request, 'accounts/edit_courses.html',{'data':response, 'page_name':"Edit Courses", 'coaching_name': profile.name})

@login_required(login_url='/account/login/')
def edit_price(request):
	try:
		profile = CoachingProfile.objects.get(username=request.user)
	except ObjectDoesNotExist as e:
		print(str(request.user) + " Error: Coaching registration not complated yet")
		return redirect(reverse('accounts:home'))

	priceInfo = {}
	if request.method == 'POST':
		for key in request.POST.keys():
			if key == 'csrfmiddlewaretoken': continue
			price_info = CoursePrice.objects.filter(username=request.user).filter(title=key).values()
			if price_info:
				CoursePrice.objects.filter(username=request.user).filter(title=key).update(price=request.POST.get(key))
			else:
				CoursePrice(username=request.user, title=key, price=request.POST.get(key)).save()
			
			priceInfo[key] = request.POST.get(key)

		return HttpResponseRedirect(reverse("accounts:eprice"))

	course_titles = CoachingCourse.objects.filter(username=request.user).values('title').distinct()
	price_info = CoursePrice.objects.filter(username=request.user).values()
	for data in course_titles:
		price_info = CoursePrice.objects.filter(username=request.user).filter(title=data.get('title')).values('price')
		if price_info:
			priceInfo[data.get('title')] = price_info[0].get('price')
		else:
			priceInfo[data.get('title')] = 0

	return render(request, 'accounts/edit_price.html', {'result': priceInfo, 'page_name':"Edit Price", 'coaching_name': profile.name})

@csrf_exempt
def enquiry(request):
	if request.method == "POST":
		try:
			# Get Coaching Profile Id
			c_url = request.POST.get('domurl')
			url = c_url.split("/")[3]
			# Get Profile Info
			c_profile = CoachingProfile.objects.filter(url=url)
			# Get User name for which this coaching belongs To
			username = c_profile[0].username
			name = request.POST.get('name', '')
			email = request.POST.get('email', '')
			mobile = request.POST.get('mobile')
			message = request.POST.get('message', '')
			subject = request.POST.get('subject', '')
			StudentEnquiry(username=username, name=name, email=email, mobile=mobile, message=message, subject=subject).save()
		except Exception as e:
			print(str(e))
			return JsonResponse(status=500)
		return JsonResponse({})
	elif request.method == "GET":
		if not request.user.is_authenticated:
			return redirect_to_login()
		try:
			profile = CoachingProfile.objects.get(username=request.user)
		except ObjectDoesNotExist as e:
			print(str(request.user) + " Error: Coaching registration not complated yet")
			return redirect(reverse('accounts:home'))

		data = list(StudentEnquiry.objects.filter(username=request.user).order_by('-created_at').values())
		return render(request, 'accounts/enquiry.html', {'data':data, 'page_name':"Enquiry", 'coaching_name': profile.name})
			
@login_required(login_url='/account/login/')
def edit_about(request):
	try:
		profile = CoachingProfile.objects.get(username=request.user)
	except ObjectDoesNotExist as e:
		print(str(request.user) + " Error: Coaching registration not complated yet")
		return redirect(reverse('accounts:home'))

	responseObj = {}
	if request.method == "POST":
		action = request.POST.get("action")
		if action == "aboutus":
			message = request.POST.get("message")
			aboutteam = request.POST.get("aboutteam")
			data = list(CoachingAboutus.objects.filter(username=request.user).values())
			if not data:
				CoachingAboutus(username=request.user, aboutus=message, aboutteam=aboutteam).save()
			else:
				CoachingAboutus.objects.filter(username=request.user).update(aboutus=message, aboutteam=aboutteam)
		if action == "achievements":
			message = request.POST.get("message")
			title = request.POST.get("title")
			task = request.POST.get("task")
			id = request.POST.get("id")
			if task and task == "delete":
				CoachingAchievements.objects.filter(username=request.user).filter(id=id).delete()
			else:
				data = list(CoachingAchievements.objects.filter(username=request.user).filter(id=id).values())
				if not data:
					CoachingAchievements(username=request.user, title=title, achievements=message).save()
				else:
					CoachingAchievements.objects.filter(username=request.user).filter(id=id).update(achievements=message,title=title)

		if action == "news":
			message = request.POST.get("message")
			title = request.POST.get("title")
			task = request.POST.get("task")
			id = request.POST.get("id")
			if task and task == "delete":
				CoachingNews.objects.filter(username=request.user).filter(id=id).delete()
			else:
				data = list(CoachingNews.objects.filter(username=request.user).filter(id=id).values())
				if not data:
					CoachingNews(username=request.user, title=title, message=message).save()
				else:
					CoachingNews.objects.filter(username=request.user).filter(id=id).update(title=title, message=message)

		if action == "team":
			name = request.POST.get("name")
			designation = request.POST.get("designation")
			description = request.POST.get("description")
			task = request.POST.get("task")
			id=request.POST.get("id")
			if task and task == "delete":
				CoachingTeam.objects.filter(username=request.user).filter(id=id).delete()
			else:
				data = list(CoachingTeam.objects.filter(username=request.user).filter(id=id).values())
				if not data:
					CoachingTeam(username=request.user, name=name, designation=designation, description=description).save()
				else:
					CoachingTeam.objects.filter(username=request.user).filter(id=id).update(name=name, designation=designation, description=description)

		return HttpResponseRedirect(reverse("accounts:eabout"))

	if request.method == "GET":
		action = request.GET.get("action")
		id = request.GET.get("id")
		if action == "achievements":
			editachievement = list(CoachingAchievements.objects.filter(username=request.user).filter(id=id).values())
			if editachievement:
				responseObj.update({"editachievement": editachievement[0]})
		elif action == "news":
			news = list(CoachingNews.objects.filter(username=request.user).filter(id=id).values())
			if news:
				responseObj.update({"editnews": news[0]})
		elif action == "team":
			team = list(CoachingTeam.objects.filter(username=request.user).filter(id=id).values())
			if team:
				responseObj.update({"editmem": team[0]})

	# Prepare response objetc
	aboutusmsg = list(CoachingAboutus.objects.filter(username=request.user).values())
	if aboutusmsg:
		responseObj.update({'about':aboutusmsg[0]})
		
	achievements = list(CoachingAchievements.objects.filter(username=request.user).values())

	if achievements:
		responseObj.update({'achievements': achievements})

	news = list(CoachingNews.objects.filter(username=request.user).values())
	if news:
		responseObj.update({'news': news})

	team = list(CoachingTeam.objects.filter(username=request.user).values())
	if team:
		responseObj.update({'team': team})
	return render(request, 'accounts/edit_about.html', {'data':responseObj, 'page_name':"Edit About Us", 'coaching_name': profile.name})

@login_required(login_url='/account/login/')
def edit_home(request):
	try:
		profile = CoachingProfile.objects.get(username=request.user)
	except ObjectDoesNotExist as e:
		print(str(request.user) + " Error: Coaching registration not complated yet")
		return redirect(reverse('accounts:home'))

	responseObj = {}
	if request.method == "POST":
		action = request.POST.get("action")
		if action == "homegeneral":
			imagetxt1 = request.POST.get("imageovertxt1")
			imagetxt2 = request.POST.get("imageovertxt2")
			courses = request.POST.get("coursesinfo")
			our_staff = request.POST.get("staffinfo")
			latest_updates = request.POST.get("news")
			placements = request.POST.get("placementinfo")
			home_id = request.POST.get("id")

			hdata = list(CoachingHome.objects.filter(username=request.user).filter(id=home_id).values())
			if not hdata:
				CoachingHome(username=request.user,
				image_txt_1=imagetxt1,
				image_txt_2=imagetxt2,
				courses=courses,
				our_staff=our_staff,
				latest_updates=latest_updates,
				placements=placements).save()
			else:
				CoachingHome.objects.filter(username=request.user).update(
				image_txt_1=imagetxt1,
				image_txt_2=imagetxt2,
				courses=courses,
				our_staff=our_staff,
				latest_updates=latest_updates,
				placements=placements)

		elif action == "homecourse":
			course_title = request.POST.get("ctitle")
			course_msg = request.POST.get("cmsg")
			course_id = request.POST.get("id")
			task = request.POST.get("task")
			if task and task == "delete":
				NewCourses.objects.filter(username=request.user).filter(id=course_id).delete()
			else:

				cdata = list(NewCourses.objects.filter(username=request.user).filter(id=course_id).values())
				if not cdata:
					NewCourses(username=request.user,
					title=course_title,
					message=course_msg).save()
				else:
					NewCourses.objects.filter(username=request.user).filter(id=course_id).update(
					title=course_title,
					message=course_msg)
		return HttpResponseRedirect(reverse("accounts:ehome"))

	if request.method == "GET":
		action = request.GET.get("action")
		if action and action == "homecourse":
			course_id = request.GET.get("id")
			editcourse = list(NewCourses.objects.filter(username=request.user).filter(id=course_id).values())
			if editcourse:
				responseObj.update({'editcourse': editcourse[0]})
		

	home = list(CoachingHome.objects.filter(username=request.user).values())
	if home:
		responseObj.update({'home': home[0]})
	
	courses = list(NewCourses.objects.filter(username=request.user).values())
	if home:
		responseObj.update({'courses': courses})
	return render(request, 'accounts/edit_home.html', {'data':responseObj, 'page_name':"Edit Home", 'coaching_name': profile.name})