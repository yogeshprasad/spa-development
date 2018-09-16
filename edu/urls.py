"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    re_path(r'^edu/(?P<profileid>[\w\-]+)/$', views.profile_home, name='profile_home'),
    re_path(r'^edu/(?P<profileid>[\w\-]+)/about/$', views.about, name='about'),
]