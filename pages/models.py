from django.db import models

# This model refers to contact us page in the site
class CoachingContact(models.Model):
    username = models.CharField(max_length=100, unique=True, blank=False, default='')
    address = models.CharField(max_length=500, default='')
    city = models.CharField(max_length=500, default='')
    email = models.EmailField(max_length=70, default='')
    phone = models.IntegerField(default=0)
    message = models.CharField(max_length=500, default='')
    header = models.CharField(max_length=200, default='')

# This model refers to course page in the site
class CoachingCourse(models.Model):
    username = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=500, default='')
    chapterid = models.CharField(max_length=50, default='')
    courseid = models.IntegerField(default=0)
    chapter = models.CharField(max_length=1000, default='')

# This model refers to course page in the site
class CoursePrice(models.Model):
    username = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=500, default='')
    price = models.IntegerField(default=0)

# This model refers to contact us page in the site
class StudentEnquiry(models.Model):
    username = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=500, default='')
    email = models.EmailField(max_length=70, default='')
    mobile = models.IntegerField(default=0)
    message = models.CharField(max_length=1000, default='')
    subject = models.CharField(max_length=500, default='')
    created_at = models.DateTimeField(auto_now_add=True)

# This model refers to contact us page in the site
class CoachingAboutus(models.Model):
    username = models.CharField(max_length=100, default='')
    aboutus = models.CharField(max_length=5000, default='')
    aboutteam = models.CharField(max_length=5000, default='')

class CoachingAchievements(models.Model):
    username = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=500, default='')
    achievements = models.CharField(max_length=5000, default='')

class CoachingTeam(models.Model):
    username = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    designation = models.CharField(max_length=500, default='')
    description = models.CharField(max_length=1000, default='')

class CoachingNews(models.Model):
    username = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=100, default='')
    message = models.CharField(max_length=5000, default='')

class CoachingHome(models.Model):
    username = models.CharField(max_length=100, default='')
    image_txt_1 = models.CharField(max_length=100, default='')
    image_txt_2 = models.CharField(max_length=100, default='')
    courses = models.CharField(max_length=100, default='')
    our_staff = models.CharField(max_length=100, default='')
    latest_updates = models.CharField(max_length=100, default='')
    placements = models.CharField(max_length=100, default='')

class NewCourses(models.Model):
    username = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=100, default='')
    message = models.CharField(max_length=500, default='')

class Teachers(models.Model):
    username = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    contact = models.IntegerField(default=0)
    email = models.EmailField(max_length=70, default='')
    description = models.CharField(max_length=1000, default='')