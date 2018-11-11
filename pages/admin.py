from django.contrib import admin
from pages.models import *


# Register your models here.
admin.site.register(CoachingContact)
admin.site.register(CoachingCourse)
admin.site.register(CoursePrice)
admin.site.register(StudentEnquiry)

#These tables belongs to about us page
admin.site.register(CoachingAboutus)
admin.site.register(CoachingAchievements)
admin.site.register(CoachingTeam)
admin.site.register(CoachingNews)

#These tables belongs to home page
admin.site.register(CoachingHome)
admin.site.register(NewCourses)