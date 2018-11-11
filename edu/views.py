from django.shortcuts import render, redirect, reverse
from edu.models import CoachingProfile
from pages.models import *

def getProfileId(url):
	return url.split("/")[2]

def profile_home(request, *args, **kwargs):
	c_url = kwargs.get('profileid')
	url_exists = CoachingProfile.objects.filter(url=c_url)
	if url_exists:
		ask = request.GET.get("ask")
		if not ask:
			ask = 'index'

		#Get Page Specific Data

		result = eval(ask)(request, *args, **kwargs) 
		
		return render(request, 'edu/'+ask+'.html', {'page':ask,'result':result})
	else:
		return render(request, 'edu/error-404.html')

# Create your views here.
def index(request, *args, **kwargs):

	# Get Coaching Profile Id
	c_url = kwargs.get('profileid')

	# Get Profile Info
	c_profile = CoachingProfile.objects.filter(url=c_url)
	user = c_profile[0].username
	
	data = {'coaching_name':c_profile[0].name}

	home = list(CoachingHome.objects.filter(username=user).values())
	if home:
		data.update({'home': home[0]})
	
	courses = list(NewCourses.objects.filter(username=user).values())
	if home:
		data.update({'courses': courses})

	aboutusmsg = list(CoachingAboutus.objects.filter(username=user).values())
	if aboutusmsg:
		data.update(aboutusmsg[0])

	news = list(CoachingNews.objects.filter(username=user).values())
	if news:
		data.update({'news': news})

	return data

def contact(request, *args, **kwargs):
	# Get Coaching Profile Id
	c_url = kwargs.get('profileid')

	# Get Profile Info
	c_profile = CoachingProfile.objects.filter(url=c_url)

	# Get User name for which this coaching belongs To
	user = c_profile[0].username

	#Get ContactUs information for this coaching

	contactus_info = CoachingContact.objects.filter(username=user).values()[0]
	contactus_info['coaching_name'] = c_profile[0].name
	return contactus_info

#def videos(request, *args, **kwargs):
#	pass
def price(request, *args, **kwargs):
	# Get Coaching Profile Id
	c_url = kwargs.get('profileid')

	# Get Profile Info
	c_profile = CoachingProfile.objects.filter(url=c_url)

	# Get User name for which this coaching belongs To
	user = c_profile[0].username

	course_titles = CoachingCourse.objects.filter(username=user).values('title').distinct()
	price_info = CoursePrice.objects.filter(username=user).values()
	result = {'coaching_name':c_profile[0].name}
	dataDetails = {}
	for data in course_titles:
		price_info = CoursePrice.objects.filter(username=user).filter(title=data.get('title')).values('price')
		if price_info:
			dataDetails[data.get('title')] = price_info[0].get('price')
		else:
			dataDetails[data.get('title')] = 0

	result['price'] = dataDetails
	return  result

def courses(request, *args, **kwargs):
	# Get Coaching Profile Id
	c_url = kwargs.get('profileid')

	# Get Profile Info
	c_profile = CoachingProfile.objects.filter(url=c_url)

	# Get User name for which this coaching belongs To
	user = c_profile[0].username
	course_titles = CoachingCourse.objects.filter(username=request.user).values('title').distinct()
	#print(course_titles)
	responseData = {}
	for titleDict in course_titles:
		title = titleDict.get('title')
		chepters = CoachingCourse.objects.filter(username=request.user).filter(title=title).values('chapter')
		chepters = [d['chapter'] for d in chepters]	
		responseData[title] = chepters
	data = {"courses": responseData, 'coaching_name':c_profile[0].name}
	return data

def about(request, *args, **kwargs):
	# Prepare response objetc
	# Get Coaching Profile Id
	c_url = kwargs.get('profileid')

	# Get Profile Info
	c_profile = CoachingProfile.objects.filter(url=c_url)

	# Get User name for which this coaching belongs To
	user = c_profile[0].username
	responseObj = {'coaching_name':c_profile[0].name}
	aboutusmsg = list(CoachingAboutus.objects.filter(username=user).values())
	if aboutusmsg:
		responseObj.update(aboutusmsg[0])
		
	achievements = list(CoachingAchievements.objects.filter(username=user).values())

	if achievements:
		responseObj.update({'achievements': achievements})

	news = list(CoachingNews.objects.filter(username=user).values())
	if news:
		responseObj.update({'news': news})

	team = list(CoachingTeam.objects.filter(username=user).values())
	if team:
		responseObj.update({'team': team})

	return responseObj
	
